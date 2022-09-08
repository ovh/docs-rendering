#!/usr/bin/env bash

CMD=$(basename $0)
PAGES_SYMBOLIC_LINK=${GITPOD_REPO_ROOT}/pages
DOCS_DIR=${GITPOD_REPO_ROOT}/docs
OUTPUT_DIR=${GITPOD_REPO_ROOT}/output
ERR_LINKS_LOG=${OUTPUT_DIR}/err_links.log
CFG_FILE=${GITPOD_REPO_ROOT}/pelicanconf.py
INDEX_TPL=${GITPOD_REPO_ROOT}/index.html
INDEX_OUTPUT=${OUTPUT_DIR}/index.html

LANGUAGES=(de-de en-asia en-au en-ca en-gb en-ie en-sg en-us es-es es-us fr-ca fr-fr it-it pl-pl pt-pt)

declare -A MANAGER
MANAGER["DE-DE"]="https://www.ovh.com/auth/?action=gotomanager&from=https://www.ovh.de/&ovhSubsidiary=de"
MANAGER["EN-GB"]="https://www.ovh.com/auth/?action=gotomanager&from=https://www.ovh.co.uk/&ovhSubsidiary=GB"
MANAGER["EN-IE"]="https://www.ovh.com/auth/?action=gotomanager&from=https://www.ovh.ie/&ovhSubsidiary=ie"
MANAGER["ES-ES"]="https://www.ovh.com/auth/?action=gotomanager&from=https://www.ovh.es/&ovhSubsidiary=es"
MANAGER["FR-FR"]="https://www.ovh.com/auth/?action=gotomanager&from=https://www.ovh.com/fr/&ovhSubsidiary=fr"
MANAGER["IT-IT"]="https://www.ovh.com/auth/?action=gotomanager&from=https://www.ovh.it/&ovhSubsidiary=it"
MANAGER["PL-PL"]="https://www.ovh.com/auth/?action=gotomanager&from=https://www.ovh.pl/&ovhSubsidiary=pl"
MANAGER["PT-PT"]="https://www.ovh.com/auth/?action=gotomanager&from=https://www.ovh.pt/&ovhSubsidiary=pt"
MANAGER["EN-CA"]="https://ca.ovh.com/auth/?action=gotomanager&from=https://www.ovh.com/ca/en/&ovhSubsidiary=ca"
MANAGER["FR-CA"]="https://ca.ovh.com/auth/?action=gotomanager&from=https://www.ovh.com/ca/fr/&ovhSubsidiary=qc"
MANAGER["EN-ASIA"]="https://ca.ovh.com/auth/?action=gotomanager&from=https://www.ovh.com/asia/&ovhSubsidiary=asia"
MANAGER["EN-AU"]="https://ca.ovh.com/auth/?action=gotomanager&from=https://www.ovh.com.au/&ovhSubsidiary=au"
MANAGER["EN-SG"]="https://ca.ovh.com/auth/?action=gotomanager&from=https://www.ovh.com/sg/&ovhSubsidiary=sg"
MANAGER["EN-US"]="https://ca.ovh.com/auth/?action=gotomanager&from=https://www.ovh.com/world/&ovhSubsidiary=we"
MANAGER["ES-US"]="https://ca.ovh.com/auth/?action=gotomanager&from=https://www.ovh.com/world/&ovhSubsidiary=ws"

declare -A OVHCLOUD_LANG
OVHCLOUD_LANG["DE-DE"]="de"
OVHCLOUD_LANG["EN-GB"]="en-gb"
OVHCLOUD_LANG["EN-IE"]="en-ie"
OVHCLOUD_LANG["ES-ES"]="es-es"
OVHCLOUD_LANG["FR-FR"]="fr"
OVHCLOUD_LANG["IT-IT"]="it"
OVHCLOUD_LANG["PL-PL"]="pl"
OVHCLOUD_LANG["PT-PT"]="pt"
OVHCLOUD_LANG["EN-CA"]="en-ca"
OVHCLOUD_LANG["FR-CA"]="fr-ca"
OVHCLOUD_LANG["EN-ASIA"]="asia"
OVHCLOUD_LANG["EN-AU"]="en-au"
OVHCLOUD_LANG["EN-SG"]="en-sg"
OVHCLOUD_LANG["EN-US"]="en"
OVHCLOUD_LANG["ES-US"]="es"

declare -A OVHDOCS_LANG
OVHDOCS_LANG["DE-DE"]="de"
OVHDOCS_LANG["EN-GB"]="gb/en"
OVHDOCS_LANG["EN-IE"]="ie/en"
OVHDOCS_LANG["ES-ES"]="es"
OVHDOCS_LANG["FR-FR"]="fr"
OVHDOCS_LANG["IT-IT"]="it"
OVHDOCS_LANG["PL-PL"]="pl"
OVHDOCS_LANG["PT-PT"]="pt"
OVHDOCS_LANG["EN-CA"]="ca/en"
OVHDOCS_LANG["FR-CA"]="ca/fr"
OVHDOCS_LANG["EN-ASIA"]="asia/en"
OVHDOCS_LANG["EN-AU"]="au/en"
OVHDOCS_LANG["EN-SG"]="sg/en"
OVHDOCS_LANG["EN-US"]="us/en"
OVHDOCS_LANG["ES-US"]="us/es"

SUB_WARNING_ICON='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewBox="-1 0 80 80"><g transform="matrix(1 0 0 -1 0 80)"><path fill="#ff9800" d="M79 11l-34 62q-2 3 -4.5 3t-3.5 -3l-36 -62q-2 -3 -0.5 -5t4.5 -2h70q3 0 4.5 2t-0.5 5zM41 14q-4 0 -4 4t3.5 4t3.5 -4t-3 -4zM44 31q0 -2 -1 -2l-2 -1l-3 1v2l-1 6q-1 7 -0.5 12t1 6t1.5 2l2 1q3 0 3.5 -1.5t0.5 -7.5q1 -8 -1 -18v0z" /></g></svg>'

usage(){
  echo "\
Usage ${CMD} [OPTIONS]
§
  -h, --help§ Display this help
  --full§ Generate a full rendering of docs
  --restart§ Restart the pelican server
§
  " | column -t -s "§"
  exit 0
}

buildIndex(){
  sed -i '/_CHECK_LINK_/{
    s/_CHECK_LINK_//
    r '${1}'
  }' ${2}
  rm -rf ${1}
}

checkLinks() {
  cd ${DOCS_DIR}
  cp ${INDEX_TPL} ${INDEX_OUTPUT}
  t=$(mktemp)
  c=$(git log | head -n1 | awk '/^commit / {print $2}')
  git diff-tree --no-commit-id --name-only -r ${c} | while read g;
  do
    code=""
    title=$(awk -F ": " '/title: / {print $2}' ${g} | sed 's/^"//;s/"$//' | sed "s/^'//;s/'$//")
    gs=$(basename $g | cut -d. -f2)
    echo "<article><div class=\"card\"><header><b>Guide: ${title}</b><small>${g}</small></header><ul class=\"list-group\">" >> ${t}
    while read u
    do
      if [ ! -z ${u} ];then
        w=""
        if [[ "${u}" =~ ^"https://docs.ovh.com".* ]];then
          [[ "${u}" =~ .*"${OVHDOCS_LANG[${gs^^}]}".* ]] || w=$SUB_WARNING_ICON
        fi
        if [[ "${u}" =~ ^"https://www.ovhcloud.com".* ]];then
          [[ "${u}" =~ .*"${OVHCLOUD_LANG[${gs^^}]}".* ]] || w=$SUB_WARNING_ICON
        fi
        if [[ "${u}" =~ ^"https://www.ovh.com/auth/".* ]];then
          [[ "${u}" == "${MANAGER[${gs^^}]}" ]] || w=$SUB_WARNING_ICON
        fi
        http_code=$(curl -sL -o /dev/null -w "%{http_code}" --connect-timeout 5 ${u})
        if [ ${http_code} -ne 000 ];then
          [[ $http_code -ge 200 ]] && code_cls="bg-success"
          [[ $http_code -ge 300 ]] && code_cls="bg-warning"
          [[ $http_code -ge 400 ]] && code_cls="bg-danger"
          [[ $http_code -ge 500 ]] && code_cls="bg-dark"
          code+="<li class=\"list-group-item\"><span class=\"badge ${code_cls}\">${http_code}</span><a href=\"${u}\" target=\"_blank\">${u}${w}</a></li>"
        fi
      fi
    done <<<$(grep -o -E "(http|https)://[a-zA-Z0-9./&?=_%:-]*" $g | sort -u)
    [[ -n ${code} ]] || code="<li style=\"padding:8px 10px;\">No link found.</li>"
    echo "${code}</ul></div></article>" >> ${t}
  done
  buildIndex ${t} ${INDEX_OUTPUT}
  cd ${GITPOD_REPO_ROOT}
}

cloneBranch() {
  rm -rf ${DOCS_DIR} ${PAGES_SYMBOLIC_LINK} ${OUTPUT_DIR} && mkdir ${OUTPUT_DIR}
  cd ${GITPOD_REPO_ROOT}
  git clone --single-branch -b ${1} https://github.com/ovh/docs.git && wait && ln -s docs/pages && checkLinks
}

cleanBranch() {
  cd ${DOCS_DIR}
  c=$(git log | head -n1 | awk '/^commit / {print $2}')
  g=$(dirname $(git diff-tree --no-commit-id --name-only -r ${c}) | sort -u | awk -F "/" '{print $1"/"$2"/"$3}')
  find ./ -mindepth 3 -maxdepth 3 -type d | sort -u | grep -v "${g}" | while read f;do rm -rf "${f}";done
  cd ${GITPOD_REPO_ROOT}
}

startPelicanServer(){
  if [[ ${#} -eq 1 && "${1}" -eq "restart" ]];then
    if [ -d ${OUTPUT_DIR}/gb ]; then
      cd ${OUTPUT_DIR} && python -m pelican.server 8080
    else
      echo "ERROR: Output directory not found or empty." && exit 1
    fi
  else
    cd ${OUTPUT_DIR} && python -m pelican.server 8080
  fi
}

checkOptions(){
  case "$1" in
    -h|--help) usage ;;
    --full) cloneBranch ${2} ;;
    --restart) startPelicanServer restart ;;
    *) echo "Invalid option ${1}. Try '${CMD} -h for more information" && exit 1 ;;
  esac
}

[[ -z ${BRANCH} ]] && BRANCH="master"

[[ "${#}" == 0 ]] && cloneBranch ${BRANCH} && cleanBranch
[[ "${#}" == 1 ]] && checkOptions $1 ${BRANCH}
[[ "${#}" -gt 1 ]] && usage

pelican --debug --fatal errors -r -o ${OUTPUT_DIR} -s ${CFG_FILE} &
startPelicanServer
