import logging
from model import *
from property_fetcher import *
import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import traceback
from urlparse import *

logger = logging.getLogger(__name__)

class IdealistaFetcher(PropertyFetcher):
  persister = None

  def __init__(self, persister):
    self.persister = persister

  def crawl_search(self, search):
    logger.info("Starting to fetch properties for search [{}]".format(search))
    # TODO: make this configurable
    process = CrawlerProcess({
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36',
      'ITEM_PIPELINES': {
        'scrapping.elasticsearch_pipeline.ElasticsearchPipeline': 0
      },
      'AUTOTHROTTLE_ENABLED': True,
      'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
      'DOWNLOAD_DELAY': 1,
      'PERSISTER': self.persister
    })

    process.crawl(IdealistaSpider)
    process.start()
    return

class IdealistaSpider(scrapy.Spider):
  provider_name = "idealista"
  name = provider_name
  base_query = '//*[@id="main"]//*'
  main_info = '{}/div[contains(@class, "main-info__title")]'.format(base_query)

  def start_requests(self):
    # URL with filters: https://www.idealista.com/venta-viviendas/madrid-madrid/con-precio-hasta_300000,metros-cuadrados-mas-de_100,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,dos-banos,tres-banos-o-mas/
    urls = [
      'https://www.idealista.com/venta-viviendas/madrid-madrid/pagina-1.htm'
    ]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    logger.info("Starting to parse responses [{}]".format(response))
    links = response.xpath('//article/div[contains(@class, "item")]/*//a[contains(@class, "item-link")]/@href').extract()
    for link in links:
      try:
        logger.info("House [{}]".format(link))
        url = urljoin(response.url, link)
        yield scrapy.Request(url, callback=self.parse_property)
      except Exception, err:
        print 'print_exc():'
        traceback.print_exc(file=sys.stdout)
        print
        print 'print_exc(1):'
        traceback.print_exc(limit=1, file=sys.stdout)
        logger.warn("Error parsing response", err)

  def parse_property(self, response):
    try:
      provider_id = self.get_provider_id(response)
      title = self.clean_url(response.xpath('{}//span[contains(@class, "main-info__title-main")]/text()'.format(self.main_info)).extract_first())
      features = '{}/div[contains(@class, "info-features")]'.format(self.base_query)
      size = response.xpath('{}/span[1]/span/text()'.format(features)).extract_first()
      room_number= response.xpath('{}/span[2]/span/text()'.format(features)).extract_first()
      floor = response.xpath('{}/span[3]/span/text()'.format(features)).extract_first()
      info = '{}/section/*/div[contains(@class, "info-data")]'.format(self.base_query)
      price = response.xpath('{}/span[1]/span/text()'.format(info)).extract_first()
      comments = response.xpath('//*[@id="main-multimedia"]//*/div[contains(@class, "comment")]/div/text()').extract()
      year = None
      energy_efficiency = None
      community_expenses = None
      baths = None
      state = None
      elevator = None
      tags = None
      contact_info = None
      geo_information = self.get_geo_information(response)
      property = Property(provider_id, self.provider_name, title, size, price, room_number, baths, floor, state, elevator,
                          community_expenses, tags, comments, year, energy_efficiency, Transfer.PURCHASE, geo_information, contact_info)
      return dict(property=property)
    except Exception, err:
      print 'print_exc():'
      traceback.print_exc(file=sys.stdout)
      print
      print 'print_exc(1):'
      traceback.print_exc(limit=1, file=sys.stdout)
      logger.warn("Error parsing response", err)

  def get_geo_information(self, response):
    district = response.xpath('{}//span[contains(@class, "main-info__title-minor")]/text()'.format(self.main_info)).extract_first()
    geo_location = self.clean_url(response.xpath('//script[contains(.,"markerType")]/text()').extract_first())
    indication = "var mapConfig="
    geo_substring = geo_location[geo_location.find("var mapConfig=")::].replace(indication, "")
    json_geo = geo_substring[:geo_substring.find("}") + 1].replace("{", "{\"").replace(":", "\":").replace(",", ",\"")
    parsed = json.loads(json_geo)
    location = Coordinate(parsed["latitude"], parsed["longitude"])
    exact_location = geo_location.find("markerType:null") < 0

    return GeoInformation(exact_location, location, "Madrid", district)

  def clean_url(self, string_to_clean):
    return string_to_clean.encode('utf-8').strip()

  def get_provider_id(self, response):
    url = response.url
    chunks = url.split("/")
    if chunks[len(chunks) -1] == '':
      return chunks[len(chunks) -2]
    else:
      return chunks[len(chunks) -1]