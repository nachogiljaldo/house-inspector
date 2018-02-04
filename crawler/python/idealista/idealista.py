# coding=utf-8
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
      'DOWNLOAD_DELAY': 5,
      'PERSISTER': self.persister,
      'SEARCH': search
    })

    process.crawl(IdealistaSpider)
    process.start()
    return

class IdealistaSpider(scrapy.Spider):
  provider_name = "idealista"
  name = provider_name
  base_query = '//*[@id="main"]//*'
  main_info = '{}/div[contains(@class, "main-info__title")]'.format(base_query)
  base_url = 'https://www.idealista.com/{}venta-viviendas/'
  pagination_pattern = 'pagina-{}{}'
  search = None

  def start_requests(self):
    self.search = self.settings['SEARCH']
    # URL with filters: https://www.idealista.com/venta-viviendas/madrid-madrid/con-precio-hasta_300000,metros-cuadrados-mas-de_100,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas,dos-banos,tres-banos-o-mas/
    url = self.build_url(1)
    urls = [
      url
    ]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def pagination_slug(self, page):
    if self.search.name:
      return self.pagination_pattern.format(page, '.htm')
    else:
      return self.pagination_pattern.format(page, '')

  def build_url(self, page_count):
    page = self.pagination_slug(page_count)
    if self.search.shape:
      first_part = self.base_url.format('areas/')
    else:
      first_part = self.base_url.format('/')
    params = self.search_params()
    query_string = self.build_query_string(self.search)
    url_to_use = '{}{}{}{}'.format(first_part, params, page, query_string)
    return url_to_use

  def build_query_string(self, search):
    return "?shape={}".format(search.shape)

  def search_params(self):
    search = self.search
    if search.name:
      prefix = search.name + "/"
    else:
      prefix = ""
    slugs = []
    if search.max_price:
      slugs.append("precio-hasta_{}".format(search.max_price))
    if search.min_price:
      slugs.append("precio-desde_{}".format(search.min_price))
    if search.min_size:
      slugs.append("metros-cuadrados-mas-de_{}".format(search.min_size))
    if search.max_size:
      slugs.append("metros-cuadrados-menos-de_{}".format(search.max_size))
    if search.ground_floors:
      slugs.append("solo-bajos")
    if search.intermediate_floors:
      slugs.append("plantas-intermedias")
    if search.last_floors:
      slugs.append("ultimas-plantas")
    if len(slugs) == 0:
      return prefix
    else:
      return prefix + "con-" + (",".join(slugs)) + "/"

  def parse(self, response):
    #next_page = self.find_next_page(response)
    next_page = None
    if next_page:
      yield scrapy.Request(next_page)
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

  def find_next_page(self, response):
    current_page = int(response.xpath('//*[@id="main-content"]/*//div[contains(@class, "pagination")]/*//li[contains(@class, "selected")]/span/text()').extract_first())
    url = self.build_url(current_page + 1)
    # if the current page contains pagina- and is the same indicated in the footer, we go on
    if "pagina-" not in response.url or self.pagination_slug(current_page) in response.url:
      return url
    else:
      return None

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
      geo_information = self.get_geo_information(response)
      url = response.url
      # FIXME: calculate real values
      tags = None
      contact_info = None
      property_features_query = '{}/div[contains(@class, "details-property_features")]/ul/li/text()'.format(self.base_query)
      property_features = response.xpath(property_features_query).extract()
      energy_efficiency = None
      elevator = None
      baths = None
      year = None
      state = "unknown"
      community_expenses = "unknown"
      for property_feature in property_features:
        clean_feature = self.clean_url(property_feature)
        print("property is [{}]".format(clean_feature))
        elevator = self.get_elevator(clean_feature, elevator)
        baths = self.get_baths(clean_feature, baths)
        year = self.get_year(clean_feature, year)
        state = self.get_state(clean_feature, state)
        energy_efficiency = self.get_energy_efficiency(clean_feature, energy_efficiency)
        
      property = Property(provider_id, self.provider_name, title, size, price, room_number, baths, floor, state, elevator,
                          community_expenses, tags, comments, year, energy_efficiency, Transfer.PURCHASE, geo_information,
                          contact_info, url)
      return dict(property=property)
    except Exception, err:
      print 'print_exc():'
      traceback.print_exc(file=sys.stdout)
      print
      print 'print_exc(1):'
      traceback.print_exc(limit=1, file=sys.stdout)
      logger.warn("Error parsing response", err)

  def get_elevator(self, to_analyse, current_value):
    if 'ascensor' in to_analyse:
      return 'con ' in to_analyse
    else:
      return current_value

  def get_energy_efficiency(self, to_analyse, current_value):
    literal = 'Certificación energética:'
    if literal in to_analyse:
      return to_analyse.replace(literal, "")
    else:
      return current_value

  def get_baths(self, to_analyse, current_value):
    if 'baño' in to_analyse:
      return int(cleanup_number(to_analyse))
    else:
      return current_value

  def get_year(self, to_analyse, current_value):
    if 'Construido en' in to_analyse:
      return int(cleanup_number(to_analyse))
    else:
      return current_value

  def get_state(self, to_analyse, current_value):
    if 'Segunda mano/' in to_analyse:
      if 'reforma' in to_analyse.lower():
        return 'renovate'
      else:
        return 'good'
    else:
      return current_value

  def get_geo_information(self, response):
    district = response.xpath('{}//span[contains(@class, "main-info__title-minor")]/text()'.format(self.main_info)).extract_first()
    geo_location = self.clean_url(response.xpath('//script[contains(.,"markerType")]/text()').extract_first())
    indication = "var mapConfig="
    geo_substring = geo_location[geo_location.find("var mapConfig=")::].replace(indication, "")
    json_geo = geo_substring[:geo_substring.find("}") + 1].replace("{", "{\"").replace(":", "\":").replace(",", ",\"")
    parsed = json.loads(json_geo)
    location = Coordinate(parsed["latitude"], parsed["longitude"])
    exact_location = geo_location.find("markerType:null") < 0

    # FIXME: remove hardcoded
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