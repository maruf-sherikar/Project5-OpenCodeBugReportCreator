@echo off
cd /d "C:\Users\Maruf.sherikar.EXT.SVKMGRP\Downloads\AI Testing\learn-testing-with-ai\Project5-OpenCodeBugReportCreator"
echo Starting server...
start /b python server.py > server.log 2>&1
timeout /t 2 /nobreak
echo Server should be running on port 8002
pause