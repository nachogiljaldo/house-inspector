from abc import ABCMeta, abstractmethod
from model import Transfer

class PropertyFetcher:
  __metaclass__ = ABCMeta
  @abstractmethod
  def crawl_search(self, search):
    pass

class Search(object):
  name = None
  transfer_type = Transfer.PURCHASE
  min_price = None
  max_price = None
  min_size = None
  max_size = None
  shape = None
  last_floors = None
  intermediate_floors = None
  ground_floors = None

  def __init__(self, name = None, transfer_type = Transfer.PURCHASE, min_price = None, max_price = None,
               min_size = None, max_size = None, shape = None, last_floorst = None, intermediate_floors = None,
               ground_floors = None):
    self.name = name
    self.transfer_type = transfer_type
    self.min_price = min_price
    self.max_price = max_price
    self.min_size = min_size
    self.max_size = max_size
    self.shape = shape
    self.last_floors = last_floorst
    self.intermediate_floors = intermediate_floors
    self.ground_floors = ground_floors