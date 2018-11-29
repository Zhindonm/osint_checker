#!/bin/bash

# Build the docker container
docker build -t osintchecker .

# Setup XForwarding
xhost + 127.0.0.1

# Run the docker container
docker run  -e DISPLAY=host.docker.internal:0 -i -t -v $(pwd)/logs:/logs osintchecker python /app/osint_checker.py "$1"
