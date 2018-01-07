build:
  echo "Building docker images"

start:
  echo "Starting environment"
  docker-compose -f scripts/docker-compose.yml up -d

stop:
  echo "Stopping environment"
  docker-compose -f scripts/docker-compose.yml down

test:
  echo "Running unit tests"