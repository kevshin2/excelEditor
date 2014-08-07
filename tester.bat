set locationOfSource = V11.3_CurrentTestBucketRegressionStatus.xls
set locationOfLogFile = tester.txt
set locationOfOutput = tester.xls

"logFileDumpExcel.py" %locationOfSource % %locationOfLogFile % %locationOfOutput %

Pause&Exit