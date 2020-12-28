#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

docker build \
    --build-arg UID=$(id -u) \
    --build-arg GID=$(id -g) \
    -t ovh-docs-dev-env \
    --no-cache \
    $SCRIPTPATH/../
