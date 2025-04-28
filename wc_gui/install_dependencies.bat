@echo off
SETLOCAL

python -m pip install --upgrade pip

IF EXIST requirements.txt (
    echo Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found.
    echo [Error] requirements.txt is required to run this script.
    exit /b 1s
)

echo Setup completed successfully!
ENDLOCAL
exit
