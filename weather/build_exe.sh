#!/bin/bash

CURRENT_DIR=$(pwd)
if [[ "${CURRENT_DIR##*/}" == "Project-Hub" ]]; then
    cd weather
elif [[ "${CURRENT_DIR##*/}" == "weather" ]]; then
    true
else
    echo "[Error] This script can only be executed in the 'Project-Hub' or 'weather' (in 'Project-Hub') directory."
    exit 1
fi

echo "The current directory is 'weather'. Starting execution."
pyinstaller -F -n Live_weather --onefile --icon=마스크.ico app.py
echo "Build completed: dist/your_script.exe"
 