from datetime import datetime
from enum import Enum
import json
from json_helper import *

class Transfer(Enum):
  RENT="rent"
  PURCHASE="purchase"

# This class reflects a real state property such as a house or apartment
class Property(JsonObject):
  id = ""
  title = ""
  provider_id = []
  size = -1
  price = -1
  rooms = -1
  baths = -1
  floor = -1
  state = ""
  elevator = False
  community_expenses = None
  tags = []
  comment = ""
  year = None
  energy_efficiency = None
  transfer_type = Transfer.PURCHASE.value
  location = None
  contact_info = None
  last_modified = datetime.now()

  def __init__(self, id, provider_id, title, size, price, rooms, baths, floor, state, elevator,
               community_expenses, tags, comment, year, energy_efficiency, transfer_type, location, contact_info):
    self.id = id
    self.provider_id = provider_id
    self.title = title
    self.size = size
    self.price = price
    self.rooms = rooms
    self.baths = baths
    self.floor = floor
    self.state = state
    self.elevator = elevator
    self.community_expenses = community_expenses
    self.tags = tags
    self.comment = comment
    self.year = year
    self.energy_efficiency = energy_efficiency
    self.transfer_type = transfer_type.value
    self.location = location
    self.contact_info = contact_info

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
  latitude = None
  longitude = None

  def __init__(self, latitude, longitude):
    self.latitude = float(latitude)
    self.longitude = float(longitude)

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