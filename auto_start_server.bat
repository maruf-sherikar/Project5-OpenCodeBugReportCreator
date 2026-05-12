@echo off
cd /d "C:\Users\Maruf.sherikar.EXT.SVKMGRP\Downloads\AI Testing\learn-testing-with-ai\Project5-OpenCodeBugReportCreator"
:loop
python bug_report_app.py >> server.log 2>&1
echo Server stopped, restarting in 5 seconds...
timeout /t 5 /nobreak
goto loop