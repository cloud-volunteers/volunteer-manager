#!/bin/bash
# create container name variable
containername=volunteer-manager
# build images from docker-compose.yml
docker compose build
# compose docker container
docker compose up -d
# remove dangling <none> images
docker image prune -f
# attach to container
docker logs -f $containername

# How to use?
# add permissions to file
# chmod +x docker.sh
# execute script
# ./docker.sh 
