#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DOCSRENDERING_PATH="${SCRIPTPATH}/../"
PLUGINS_PATH="${DOCSRENDERING_PATH}/plugins/"

docker run --rm \
    -v $PLUGINS_PATH:/home/python/src/docs/plugins \
    -u $(id -u):$(id -g) \
    ovh-docs-dev-env \
    python ${@}
