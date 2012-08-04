#!/bin/bash

function usage() {
    echo "Usage: ${0} -w <workspace path> [-b <branch name>] [-t]"
    exit 1
}

function build() {
    [[ -d ${1} ]] || git clone git@github.com:abiquo/${1}.git
    cd ${1}
    [[ -n ${BRANCH} ]] && git checkout ${BRANCH}
    mvn clean install -fae ${@:2}
    [[ $? -ne 0 ]] && exit 1
    cd ..
}

while getopts "w:b:t" OPT; do
    case ${OPT} in
        w) WORKSPACE=${OPTARG} ;;
        b) BRANCH=${OPTARG} ;;
        t) ALL_TESTS=true ;;
        ?) usage ;;
    esac
done

[[ -z ${WORKSPACE} ]] && usage
cd ${WORKSPACE}

build commons-amqp
build abiquo -P libs -pl model,nodecollector,aimstub -Dtest.suite=none -Dit.suite=none
build jclouds-abiquo
build abiquo-ucs-client
if [[ "${ALL_TESTS}" == "true" ]]; then
    build abiquo-enterprise -P libs,storage -Dtest.suite=all -Dit.suite=all
else
    build abiquo-enterprise -P libs,storage
fi
build tarantino
build clientui