@echo off
setlocal

:: Required Python version (must match a py launcher tag, e.g. "3.11")
set "PYTHON_VERSION=3.11"

echo Checking for Python %PYTHON_VERSION%...
py -%PYTHON_VERSION% --version >nul 2>&1
if errorlevel 1 (
    echo Python %PYTHON_VERSION% not found.
    echo Installing Python 3.11.1...
    powershell -c "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe' -OutFile '%TEMP%\python-3.11.1-amd64.exe'"

    echo Launching installer. MAKE SURE TO CHECK "Add python.exe to PATH" OR THIS WILL NOT WORK.
    timeout /t 5
    "%TEMP%\python-3.11.1-amd64.exe"

    echo Press any key to continue once the Python installer has finished.
    pause

    echo.
    echo Python installation complete. Restart setup.bat to continue.
    exit /b
) else (
    echo Python %PYTHON_VERSION% is installed.
)

echo Checking for Tesseract OCR...
if exist "%ProgramFiles%\Tesseract-OCR\tesseract.exe" (
    echo Tesseract OCR is installed.
) else (
    echo Tesseract OCR not found.
    echo Installing Tesseract OCR 5.5.3...
    powershell -c "Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tesseract/releases/download/5.5.3/tesseract-ocr-w64-setup-5.5.3.20260724.exe' -OutFile '%TEMP%\tesseract-ocr-w64-setup-5.5.3.exe'"

    echo Launching installer. Install to the DEFAULT location so this script can find it later.
    timeout /t 5
    "%TEMP%\tesseract-ocr-w64-setup-5.5.3.exe"

    echo Press any key to continue once the Tesseract installer has finished.
    pause

    echo.
    echo Tesseract installation complete. Restart setup.bat to continue.
    exit /b
)

echo Setting up virtual environment...
if not exist "venv" (
    py -%PYTHON_VERSION% -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment with Python %PYTHON_VERSION%.
        pause
        exit /b
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists, skipping creation.
)

echo Installing dependencies into the virtual environment...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Warning: pip upgrade failed, continuing anyway.
)
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency install failed. Check the errors above.
    call venv\Scripts\deactivate.bat
    pause
    exit /b
)
call venv\Scripts\deactivate.bat

echo.
echo Setup complete. You can now run run.bat.
pause