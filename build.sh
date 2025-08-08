#!/bin/sh
set -e

IMAGE_NAME="my-python-app"
PYTHON_VERSION="3.13"
docker build --build-arg BASE_IMAGE=python:${PYTHON_VERSION}-slim -t xyseer/animeassistant:0.9c --platform linux/amd64,linux/arm64 --push .
docker build --build-arg BASE_IMAGE=python:${PYTHON_VERSION}-slim -t xyseer/animeassistant:latest --platform linux/amd64,linux/arm64 --push .
docker build --build-arg BASE_IMAGE=python:${PYTHON_VERSION}-alpine -t xyseer/animeassistant:0.9c-alpine --platform linux/amd64,linux/arm64 --push .
