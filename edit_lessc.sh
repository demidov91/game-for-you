#!/usr/bin/env bash
LESSC_PATH=$1
NODE_PATH="#!$2"
NODE_PATH=${NODE_PATH//\//\\/}
sed -i -e "1s/.*/${NODE_PATH}/" ${LESSC_PATH}
