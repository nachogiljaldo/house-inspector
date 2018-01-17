import logging.config

from config import load_configuration, elasticsearch_path, logging_config_path
from property_fetcher import Search
from idealista.idealista import IdealistaFetcher
from persister import Persister

logging.config.fileConfig(logging_config_path())

logger = logging.getLogger("main")

logger.info("Starting house-inspector")

configuration = load_configuration()
es_path = elasticsearch_path()
logger.info("Will write to [{}]".format(es_path))

persister = Persister(es_path)

search = Search("a search", min_price=150000, max_price=350000, min_size=100)
fetcher = IdealistaFetcher(persister)
idealista_properties = fetcher.crawl_search(search)
logger.info("Received following properties: [{}]".format(idealista_properties))