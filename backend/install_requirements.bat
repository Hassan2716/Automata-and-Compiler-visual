@echo off
echo Updating pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing requirements...
pip install -r requirements.txt

pause

