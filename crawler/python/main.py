import logging.config

from config import load_configuration, elasticsearch_path, logging_config_path
from property_fetcher import Search
from idealista.idealista import IdealistaFetcher
from property_persister import PropertyPersister

logging.config.fileConfig(logging_config_path())

logger = logging.getLogger("main")

logger.info("Starting house-inspector")

configuration = load_configuration()
es_path = elasticsearch_path()
logger.info("Will write to [{}]".format(es_path))

persister = PropertyPersister(es_path)
persister.ensure_ready()

fetcher = IdealistaFetcher(persister)

# TODO: find a way of making this parameterized
#search = Search(min_price=150000, max_price=400000, min_size=90, shape='%28%28cf%7CuFdozUia%40cyAkmA~%5CuMa%7B%40wg%40%7DgAwZuaBzCu%7BCvy%40gCt%7DAk_AvjBoc%40%7Ct%40~MfdB%7BKtaCtcAln%40nr%40pRxeAoi%40hjBk%5Chp%40qExeAa%60C%3FgTxg%40wZhp%40qv%40vIgs%40lEwy%40vX%29%29')
#idealista_properties = fetcher.crawl_search(search)
other_search = Search(min_size=70, shape='%28%28cf%7CuFdozUia%40cyAkmA~%5CuMa%7B%40wg%40%7DgAwZuaBzCu%7BCvy%40gCt%7DAk_AvjBoc%40%7Ct%40~MfdB%7BKtaCtcAln%40nr%40pRxeAoi%40hjBk%5Chp%40qExeAa%60C%3FgTxg%40wZhp%40qv%40vIgs%40lEwy%40vX%29%29')
idealista_properties = fetcher.crawl_search(other_search)
logger.info("Received following properties: [{}]".format(idealista_properties))