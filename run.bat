@echo off
REM Run script for Fashion Finds project

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Fashion Finds application...
echo Open your browser to http://localhost:5000
python main.py