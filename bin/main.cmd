@echo off
setlocal

cd /d %~dp0..\
.\python\python.exe -m manga_text_detection

endlocal
