# House inspector
This project contains an extendable module that allows crawling housing websites and visualize diverse statistics, such as:
- average square meter price in an area

The information can be acquired by either crawling real-state housing or APIs if available. The goal is providing a platform that is agnostic
from the input source and allows adapting the different input formats to an internal representation of a property.

The aim is allowing the users comparing different housing platforms and take informed decisions when
analyzing the purchase or rent of a house.

## How to build
The system is distributed in the form of a docker-compose script + images for the components of the framework itself.

## How to run
You can `make start` to start it and `make stop` to stop it.

## How to run tests
You can `make test` to run the tests.

## How to add new backends

