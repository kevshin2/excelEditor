@echo off
set userID = 
set password = 

echo.

downloader.py %userID % %password %

set locationOfSource = source.xls
set locationOfLogFile = tester.txt
set locationOfOutput = tester.xls
set name = "QA Tester"
set buildName = "Build Name Placeholder"


excelEditor.py %locationOfSource % %locationOfLogFile % %locationOfOutput % %name % %buildName %

echo.

uploader.py %userID % %password % %locationOfOutput %

Pause&Exit