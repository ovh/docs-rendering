#!/bin/bash

# Params
# $1 : Folder (optionnal)

FOLDER="$1"
OUTPUT="$(echo $(basename $0)| cut -d '.' -f1).result.csv"

function help() {
	echo "Usage: "
	echo "./$(basename $0) <FOLDER>(Optionnal)"
	exit 0
}

# Test var count 
if [ $# -lt 0 -o $# -gt 1 ] 
then
	help
fi

export BRANCH="$(cat docs/.git/HEAD | cut -d / -f3)"

echo "INFO: Active branch = ${BRANCH}"

if [ ! -v ${FOLDER} ]
then
	echo "INFO: Checking folder = ${FOLDER}"
fi

[ -f ${OUTPUT} ] && rm -f ${OUTPUT}
touch ${OUTPUT}

for FILE in $(find ./${FOLDER} -name "*.md")
do
  echo "-"
  echo "### ${FILE}"
  for link in $(cat ${FILE} | grep -Eo "(http|https)://[a-zA-Z0-9./?=_%:-]*" | sort -u)
  do
    linkStatus=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 ${link})
    echo "(${linkStatus}) - ${link}"
    echo "${FILE};${link};${linkStatus}" >> ${OUTPUT}
  done
done
