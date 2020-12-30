#!/usr/bin/env bash
PY=${PY:-python}
PELICAN=${PELICAN:-pelican}

BASEDIR=$(pwd)
SRC_DIR=$BASEDIR/../pages
OUTPUT_DIR=$BASEDIR/../output
CFG_FILE=$BASEDIR/pelicanconf.py

cd $BASEDIR;
$PELICAN --debug --fatal errors -r -o $OUTPUT_DIR -s $CFG_FILE &
pid=$!
cd $OUTPUT_DIR;
$PY -m pelican.server 8080
