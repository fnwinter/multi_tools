@echo off
cd /d "%~dp0"
python -m PyInstaller --onefile --noconsole --name DisplayClone display_clone.py
