#!/bin/bash

CURRENT_DIR=$(pwd)
TARGET_DIR="Live-Weather"
EXE_FILE_NAME="Live_Weather"

if [[ "${CURRENT_DIR##*/}" == "Project-Hub" ]]; then
    cd weather
elif [[ "${CURRENT_DIR##*/}" == ${TARGET_DIR} ]]; then
    true
else
    echo "[Error] This script can only be executed in the 'Project-Hub' or ${TARGET_DIR} (in 'Project-Hub') directory."
    exit 1
fi

echo "The current directory is ${TARGET_DIR}. Starting execution."
pyinstaller -F -n ${EXE_FILE_NAME} --icon=마스크.ico app.py
echo "Build completed: dist/${EXE_FILE_NAME}.exe"
