from datetime import datetime
from enum import Enum
import json
from json_helper import *
from utils import *

class Transfer(Enum):
  RENT="rent"
  PURCHASE="purchase"

# This class reflects a real state property such as a house or apartment
class Property(JsonObject):
  id = None
  title = None
  provider_id = None
  size = None
  price = None
  rooms = None
  baths = None
  floor = None
  floor_full = None
  state = None
  elevator = None
  community_expenses = None
  tags = []
  comment = None
  year = None
  energy_efficiency = None
  transfer_type = None
  contact_info = None
  url = None
  coordinates = None
  exact_location = None
  district = None
  last_modified = datetime.now()
  price_per_size_unit = None

  def __init__(self, id, provider_id, title, size, price, rooms, baths, floor, state, elevator,
               community_expenses, tags, comment, year, energy_efficiency, transfer_type, location, contact_info,
               url):
    self.id = id
    self.provider_id = provider_id
    self.title = title
    self.size = int_or_none(size)
    if price:
      self.price = float_or_none(cleanup_number(price))
    self.price_per_size_unit = self.price / self.size
    self.rooms = int_or_none(rooms)
    self.baths = int_or_none(baths)
    if floor:
      self.floor = int_or_none(only_digits(floor))
      self.floor_full = floor
    if location:
      self.coordinates = location.coordinates
      self.exact_location = location.exact_location
      self.city = location.city
      self.district = location.district

    self.state = state
    self.elevator = elevator
    self.community_expenses = float_or_none(community_expenses)
    self.tags = tags
    self.comment = comment
    self.year = int_or_none(year)
    self.energy_efficiency = energy_efficiency
    self.transfer_type = transfer_type.value
    self.contact_info = contact_info
    self.url = url

class GeoInformation(JsonObject):
  exact_location = False
  coordinates = None
  city = None
  district = None

  def __init__(self, exact_location, coordinates, city, district):
    self.exact_location = exact_location
    self.coordinates = coordinates
    self.city = city
    self.district = district

class Coordinate(JsonObject):
  lat = None
  lon = None

  def __init__(self, latitude, longitude):
    self.lat = float(latitude)
    self.lon = float(longitude)

  @staticmethod
  def parse(coordinates, separator=','):
    chunks = coordinates.split(separator)
    coordinate = Coordinate(float(chunks[0]), float(chunks[1]))
    return coordinate

class ContactInfo(JsonObject):
  telephone_number = "not_available"
  agency = "not_available"
  description = ""
  url = ""

  def __init__(self, telephone_number, agency, description, url):
    self.telephone_number = telephone_number
    self.agency = agency
    self.description = description
    self.url = url

# This class reflects a real state information provider, examples of such could be idealista, fotocasa and others.
class Provider(JsonObject):
  id = ""
  name = ""
  url = ""

  def __init__(self, id, name, url):
    self.id = id
    self.name = name
    self.url = url