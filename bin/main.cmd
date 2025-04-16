@echo off
setlocal

cd /d %~dp0..\
.\venv\Scripts\python.exe -m manga_text_detection

endlocal
