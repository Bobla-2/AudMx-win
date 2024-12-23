@echo off
start cmd /k "pyinstaller -i "C:\Users\savva\Documents\github\AudMx-win\icon.ico" --hidden-import pycaw  --hidden-import ctype --hidden-import pywin32 -w AudMX.py"
