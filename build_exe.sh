#!/bin/bash

REPO_NAME="Project-Hub"
CURRENT_DIR=$(pwd)
script1="./Exchange-Rate/build_exe.sh"
script2="./Live-Weather/build_exe.sh"
script3="./Watermark/build_exe.sh"


if [[ "${CURRENT_DIR##*/}" == ${REPO_NAME} ]]; then
    true

else
    echo "[Error] This script can only be executed in the '${REPO_NAME}' directory."
    exit 1
fi


echo "The current directory is ${REPO_NAME}. Starting execution."
$script1
$script2
$script3

echo "Build completed: Please check the dist folder in each folder (excluding WC-GUI)"
