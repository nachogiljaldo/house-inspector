.PHONY: help build

IMAGE_VERSION?=0.1
DOCKER_REPOSITORY?="localhost:443"

help:
	@echo "build - builds all docker images"
	@echo "start - starts the application"
	@echo "stop - stops the application"
	@echo "images-tag - tags docker images with an specific version"
	@echo "images-push - pushes docker images to the repository"

build:
	echo "Building docker images"
	docker build -t 'house-inspector:${IMAGE_VERSION}' -f build/house-inspector/Dockerfile .

images-tag:
	docker tag house-inspector:${IMAGE_VERSION}' ${DOCKER_REPOSITORY}/house-inspector:${IMAGE_VERSION}

images-push:
	docker push ${DOCKER_REPOSITORY}/cuponeitor-web:${IMAGE_VERSION}

start: prepare-environment
	echo "Starting environment"
	docker-compose -f scripts/docker-compose.yml up -d

stop:
	echo "Stopping environment"
	docker-compose -f scripts/docker-compose.yml down

prepare-environment:
	echo "Preparing execution environment"
	mkdir -p /data/elasticsearch