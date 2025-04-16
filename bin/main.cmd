@echo off
setlocal

cd /d %~dp0..\
call .\venv\Scripts\activate.bat
python -m manga_text_detection
call .\venv\Scripts\deactivate.bat

endlocal