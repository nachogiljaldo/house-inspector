import logging.config


class ElasticsearchPipeline(object):

  logger = logging.getLogger("elasticsearch-pipeline")
  persister = None

  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings['PERSISTER'])

  def __init__(self, persister):
    self.persister = persister

  def process_item(self, item, spider):
    self.persister.persist(item)
    return item