from abc import ABCMeta, abstractmethod
from model import Transfer

class PropertyFetcher:
  __metaclass__ = ABCMeta
  @abstractmethod
  def crawl_search(self, search):
    pass

class Search(object):
  name = ""
  transfer_type = Transfer.PURCHASE
  min_price = 0
  max_price = 10000000000
  min_size = 0
  max_size = 9999999

  def __init__(self, name, transfer_type = Transfer.PURCHASE, min_price = 0, max_price = 10000000000, min_size = 0, max_size = 9999999):
    self.name = name
    self.min_price = min_price
    self.max_price = max_price
    self.min_size = min_size
    self.max_size = max_size