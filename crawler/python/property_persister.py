from elasticsearch import Elasticsearch
import datetime
import logging.config
import sys
import traceback

class PropertyPersister(object):
  logger = logging.getLogger("property_persister")
  url = None
  index_pattern = None
  index_name = None
  type_name = None

  def __init__(self, url, index_pattern="properties", type_name="property"):
    self.url = url
    self.index_pattern = index_pattern
    self.index_name = "{}-{}".format(index_pattern, datetime.datetime.today().strftime('%Y-%m-%d'))
    self.type_name = type_name

  def es_client(self):
    return Elasticsearch([self.url])

  def ensure_ready(self):
    client = self.es_client()
    result = client.indices.put_template(name="{}-template".format(self.index_pattern), body={
      "index_patterns": ["{}-*".format(self.index_pattern)],
      "settings": {
        "number_of_shards": 5
      },
      "mappings": {
        self.type_name: {
          "_source": {
            "enabled": True
          },
          "properties": {
            "id": {
              "type": "keyword"
            },
            "title": {
              "type": "text"
            },
            "size": {
              "type": "integer"
            },
            "price": {
              "type": "double"
            },
            "price_per_size_unit": {
              "type": "double"
            },
            "rooms": {
              "type": "integer"
            },
            "baths": {
              "type": "integer"
            },
            "floor": {
              "type": "integer"
            },
            "floor_full": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword"
                }
              }
            },
            "state": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword"
                }
              }
            },
            "elevator": {
              "type": "boolean"
            },
            "community_expenses": {
              "type": "double"
            },
            "comment": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword"
                }
              }
            },
            "energy_efficiency": {
              "type": "keyword"
            },
            "transfer_type": {
              "type": "keyword"
            },
            "coordinates": {
              "type": "geo_point"
            },
            "exact_location": {
              "type": "boolean"
            },
            "city": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword"
                }
              }
            },
            "district": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword"
                }
              }
            },
            "last_modified": {
              "type": "date"
            }
          }
        }
      }
    }, create=False)
    self.logger.info("Created template [{}]".format(result))
    if not client.indices.exists(index=self.index_name):
      result = client.indices.create(index=self.index_name)
      self.logger.info("Created index [{}]".format(result))
    result = client.indices.put_alias(index="{}-*".format(self.index_pattern), name=self.index_pattern)
    self.logger.info("Created alias [{}]".format(result))

  def persist(self, property_dict):
    try:
      property = property_dict['property']
      doc = property.toJSON()
      self.logger.debug("about to persist document (index, id) = [({}, {}]".format(property.id, self.index_name))
      self.logger.debug("document to persist is [{}]".format(doc))
      result = self.es_client().index(index=self.index_name, doc_type=self.type_name, id=property.id, body=doc)
      self.logger.info("Saved with result [{}]".format(result))
    except Exception, err:
      print 'print_exc():'
      traceback.print_exc(file=sys.stdout)
      print
      print 'print_exc(1):'
      traceback.print_exc(limit=1, file=sys.stdout)