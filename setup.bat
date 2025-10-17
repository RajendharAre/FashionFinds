@echo off
REM Setup script for Fashion Finds project

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete! To run the application:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the application: python main.py
echo 3. Open your browser to http://localhost:5000