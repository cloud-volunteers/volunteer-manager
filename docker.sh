#!/bin/bash
# Warning! This script will destroy old container and recreate new one!
# Decompose old docker container
docker-compose down
# Build new image from docker-compose.yml
docker-compose build
# Remove dangling <none> images
docker-image prune -f
# Compose new docker container
docker-compose up
# How to use?
# 1) Add permissions to file
# chmod +x docker.sh
# 2) execute script
# ./docker.sh 