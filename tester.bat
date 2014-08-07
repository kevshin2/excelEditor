set userID = 
set password = 

downloader.py %userID % %password %

set locationOfSource = source.xls
set locationOfLogFile = tester.txt
set locationOfOutput = tester.xls
set name = "QA Tester"
set buildName = "Build Name Placeholder"


excelEditor.py %locationOfSource % %locationOfLogFile % %locationOfOutput % %name % %buildName %

Pause&Exit