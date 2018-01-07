import logging
import logging.config
from config import load_configuration, elasticsearch_path, logging_config_path

logging.config.fileConfig(logging_config_path())

logger = logging.getLogger("main")

logger.info("Starting house-inspector")

configuration = load_configuration()
es_path = elasticsearch_path()
logger.info("Will write to [{}]".format(es_path))