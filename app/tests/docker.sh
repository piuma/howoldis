#!/bin/sh

# Make sure tests fails if a command ends without 0
set -e

# Generate random port for testing
CLIENT_PORT=$(cat /dev/urandom|od -N2 -An -i|awk -v f=10000 -v r=19999 '{printf "%i\n", f + r * $1 / 65536}')

# Make sure the port is not already in use. In case it is, rerun the script to get a new port.
[ $(netstat -an | grep LISTEN | grep :$CLIENT_PORT | wc -l) -eq 0 ] || { ./$0 && exit 0 || exit 1; }

# Run container in a simple way
DOCKERCONTAINER=$(docker run -d -p 127.0.0.1:${CLIENT_PORT}:12345  image:testing)
sleep 5
# Make sure port is open
nc localhost ${TLS_CLIENT_PORT} < /dev/null || exit 1

# Make sure the container is not restarting or dying
sleep 40
docker ps -f id=${DOCKERCONTAINER}

# Clean up
docker stop ${DOCKERCONTAINER} && docker rm -fv ${DOCKERCONTAINER}
