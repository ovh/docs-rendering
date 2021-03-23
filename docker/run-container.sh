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
SETTINGS_PATH="${DOCSRENDERING_PATH}/pelicanconf.py"
TRANSLATIONS_PATH="${DOCSRENDERING_PATH}/config/"

trap "echo 'stoping container...' && docker stop ovh-docs-dev-env" 2

docker run --rm \
    -v $DOCS_FOLDER/pages:/home/python/src/docs/pages \
    -v $THEMES_PATH:/home/python/src/docs/themes \
    -v $PLUGINS_PATH:/home/python/src/docs/plugins \
    -v $SETTINGS_PATH:/home/python/src/docs/pelicanconf.py \
    -v $TRANSLATIONS_PATH:/home/python/src/docs/config \
    -u $(id -u):$(id -g) \
    -d \
    --name ovh-docs-dev-env \
    -p $PORT:8080 \
    ovh-docs-dev-env
docker logs -f ovh-docs-dev-env

