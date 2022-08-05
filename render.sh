#!/usr/bin/env bash

BRANCH="$1"
PY=${PY:-python}
PELICAN=${PELICAN:-pelican}

SRC_DIR=${GITPOD_REPO_ROOT}/pages
OUTPUT_DIR=${GITPOD_REPO_ROOT}/output
CFG_FILE=${GITPOD_REPO_ROOT}/pelicanconf.py

if [ -z ${BRANCH} ]
then
	BRANCH="master"
fi

cd ${GITPOD_REPO_ROOT}

if [ -d ${GITPOD_REPO_ROOT}/docs ]
then
	rm -rf ${GITPOD_REPO_ROOT}/docs
fi

rm -rf ${GITPOD_REPO_ROOT}/output/* 2>>/dev/null

git clone --single-branch -b ${BRANCH} https://github.com/ovh/docs.git

if [ ! -L pages ] 
then
	ln -s docs/pages
fi

$PELICAN --debug --fatal errors -r -o $OUTPUT_DIR -s $CFG_FILE &
pid=$!
cd $OUTPUT_DIR;
$PY -m pelican.server 8080
