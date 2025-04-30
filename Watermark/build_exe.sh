#!/bin/bash

REPO_NAME="Project-Hub"
CURRENT_DIR=$(pwd)
TARGET_DIR="Watermark"
EXE_FILE_NAME="watermark"
ICO="water.ico"
logo="water.png"
CODE="app.py"

if [[ "${CURRENT_DIR##*/}" == ${REPO_NAME} ]]; then
    cd ${TARGET_DIR}
elif [[ "${CURRENT_DIR##*/}" == ${TARGET_DIR} ]]; then
    true
else
    echo "[Error] This script can only be executed in the '${REPO_NAME}' or ${TARGET_DIR} (in '${REPO_NAME}') directory."
    exit 1
fi

echo "The current directory is ${TARGET_DIR}. Starting execution."
pyinstaller -w -F -n ${EXE_FILE_NAME} --icon=${ICO} --add-data "${logo};." ${CODE}
echo "Build completed: dist/${EXE_FILE_NAME}.exe"
