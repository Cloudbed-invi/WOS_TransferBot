@echo off
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Starting Setup Wizard...
python setup.py
pause
