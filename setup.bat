@echo off
echo  Setting up Portfolio Project...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  Python is not installed. Please install Python3 first.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo  Creating project directories...
if not exist static\css mkdir static\css
if not exist static\js mkdir static\js
if not exist static\images mkdir static\images
if not exist data mkdir data
if not exist templates mkdir templates

echo.
echo  Setup complete!
echo.
echo  To activate the virtual environment, run:
echo    venv\Scripts\activate
echo.
echo   To run the application:
echo    python app.py
echo    or
echo    flask run
echo.
echo  The application will be available at: http://localhost:5000
echo.
pause