@echo off
echo Creating Python Virtual Environment...
python -m venv venv

echo.
echo Installing requirements...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo Starting Setup Wizard...
python setup.py
pause
pause
