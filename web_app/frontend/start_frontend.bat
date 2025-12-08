@echo off
echo Starting React Frontend...
cd /d %~dp0
set "PATH=C:\Program Files\nodejs;%PATH%"
call npm start
pause

