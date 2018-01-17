from elasticsearch import Elasticsearch
import logging.config
import sys
import traceback

class Persister(object):
  logger = logging.getLogger("persister")
  url = None
  index_name = None
  type_name = None

  def __init__(self, url, index_name="properties", type_name="property"):
    self.url = url
    self.index_name = index_name
    self.type_name = type_name

  def persist(self, property_dict):
    try:
      es = Elasticsearch([self.url])
      property = property_dict['property']
      doc = property.toJSON()
      self.logger.debug("about to persist document (index, id) = [({}, {}]".format(property.id, self.index_name))
      result = es.index(index=self.index_name, doc_type=self.type_name, id=property.id, body=doc)
      self.logger.info("Saved with result [{}]".format(result))
    except Exception, err:
      print 'print_exc():'
      traceback.print_exc(file=sys.stdout)
      print
      print 'print_exc(1):'
      traceback.print_exc(limit=1, file=sys.stdout)