#!/bin/bash

DOCS_FOLDER=$(pwd)
PORT=8080

usage="$(basename "$0") [-h] [-f folder] [-p port] build and start docs.ovh.com in a docker container

where:
    -h  show this help
    -f  set the docs repo path to build (default: current directory)
    -p  set the exposed docker port (default: 8080)
"

while getopts ':hp:f:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    p) PORT=$OPTARG
       ;;
    f) DOCS_FOLDER=$OPTARG
       ;;
    :) echo "Option -$OPTARG requires an argument." >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done

if ! command -v docker
then
    echo "Please install docker first !"
    exit 1
fi

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DOCSRENDERING_PATH="${SCRIPTPATH}/../"
THEMES_PATH="${DOCSRENDERING_PATH}/themes/"
PLUGINS_PATH="${DOCSRENDERING_PATH}/plugins/"

trap "echo 'stoping container...' && docker stop ovh-docs-dev-env" 2

docker run --rm \
    -v $DOCS_FOLDER/pages:/src/pages \
    -v $THEMES_PATH:/src/docs/themes \
    -v $PLUGINS_PATH:/src/docs/plugins \
    -d \
    --name ovh-docs-dev-env \
    -p $PORT:8080 \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    ovh-docs-dev-env
docker logs -f ovh-docs-dev-env

