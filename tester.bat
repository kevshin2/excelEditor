set locationOfSource = V11.3_CurrentTestBucketRegressionStatus.xls
set locationOfLogFile = tester.txt
set locationOfOutput = tester.xls
set name = "QA Tester"
set buildName = "Build Name Placeholder"

excelEditor.py %locationOfSource % %locationOfLogFile % %locationOfOutput % %name % %buildName %

Pause&Exit