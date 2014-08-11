from xlutils.copy import copy
import xlwt
import xlrd
import sys
import os
import datetime

"""converts dates to their proper format"""
def convertDate(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return str(datetime.date(datetuple[0], datetuple[1], datetuple[2]))
        return str(datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5]))
    if cell.ctype == xlrd.XL_CELL_EMPTY: 
        return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN: 
        return cell.value == 1
    return str(cell.value)

"""writes contents of argument 2 to the EIF TCS sheet of argument 1
    and writes it to a temp location"""
def writeLogFile(locationOfSheetToBeCopied, locationOfLogFile, locationOfWriteBack):
    readSheet = xlrd.open_workbook(locationOfSheetToBeCopied, sys.stdout, 0, True, "", "None", "None",True)

    #grab build number and total/run/pass from entry that was inserted
    buildNumber = readSheet.sheet_by_index(3).cell_value(4,4)
    trp = readSheet.sheet_by_index(3).cell_value(4,1)
    date = str(datetime.date.today())
    
    numberOfRows = readSheet.sheet_by_index(8).nrows

    writeSheet = copy(readSheet)
    
    entry = "%s %s %s" % (buildNumber, date, trp)
    
    sheetToBeModified = writeSheet.get_sheet(8)
    
    sheetToBeModified.write(2, 0, entry)
    
    #begin copying log file
    logFile = open(locationOfLogFile, 'r')
    
    rowPosition = 4

    for line in logFile:
        sheetToBeModified.write(rowPosition,0, line)
        rowPosition += 1

    #"delete" rows if logfile isnt longer than the previous logfile
    while rowPosition < numberOfRows:
        rowPosition += 1
        sheetToBeModified.write(rowPosition,0,"")
    
    logFile.close()
        
    writeSheet.save(locationOfWriteBack)
    
    readSheet.release_resources()
    
"""inserts an entry automatically into the EIF status sheet"""
def insertEntry(locationOfSheetToBeCopied, locationOfWriteBack, locationOfLogFile, name, buildName):
    
    #open file while keeping cell data
    readSheet = xlrd.open_workbook(locationOfSheetToBeCopied, sys.stdout, 0, True, "", "None", "None",True)

    eifStatus = readSheet.sheet_by_index(3)
    
    numberOfRows = eifStatus.nrows
    
    numberOfColumns = eifStatus.ncols

    #this is the row that needs to be inserted
    contentsOfCells = {4: generateEntry(locationOfLogFile, name, buildName)}
    
    rowPosition = 4
    colPosition = 0

    #read in each line already in the spreadsheet
    while rowPosition < numberOfRows:
        contentsOfRow = []
        while colPosition < numberOfColumns:
            if colPosition is not 0:
                contentsOfRow.append(eifStatus.cell_value(rowPosition, colPosition))
            else:
                contentsOfRow.append(convertDate(eifStatus.cell(rowPosition,colPosition),0))             
            colPosition += 1
        rowPosition += 1
        contentsOfCells[rowPosition] = contentsOfRow
        colPosition = 0

    writeSheet = copy(readSheet)
    
    sheetToBeModified = writeSheet.get_sheet(3)

    #write back the cells with new row inserted
    for row in contentsOfCells:
        while colPosition < numberOfColumns:
            sheetToBeModified.write(row,colPosition,contentsOfCells[row][colPosition]) 
            colPosition += 1
            
        colPosition = 0
   
    writeSheet.save(locationOfWriteBack)
    readSheet.release_resources()

"""takes the name of a log file and parses it for info, returns a list representing the entry"""
def generateEntry(locationOfLogFile, name, buildName):
    
    logFile = open(locationOfLogFile, "r")
    
    observations = "All pass"
    
    #checks for 100% pass condition, if false it will ask for user input
    search = logFile.read();
    
    if search.find("%PASS : 100.0% #PASS / #Valid") == -1:
        selection = ""
        while selection.lower() != 'y' and selection.lower() != "yes":
            observations = raw_input("\nThe test case does not have a 100% pass rate, please type in your observations: ")
            print "You entered: %s" % (observations)
            selection = raw_input("\nAre you satisfied with your observations? (Y/N): ")
    
    #finds the total number of tests        
    totalNum = search.partition("#Total: ")[2]
    totalNum = totalNum.partition("#")[0]
    
    #finds the number that ran
    numRan = search.partition("#Valid (non error): ")[2]
    numRan = numRan.partition("#")[0]
    
    #finds the number passed
    passed = search.partition("#PASS : ")[2]
    passed = passed.partition("#")[0]
    
    logFile.close()
    
    #create the Total/Run/Pass entry
    trp = "%s/%s/%s" % (totalNum, numRan, passed)
    
    return [str(datetime.date.today()), trp, observations, name, buildName]  

def main(args):
    if len(args) == 5:
        insertEntry(args[0],"temp.xls", args[1], args[3], args[4])
        print "\nENTRY INSERTED SUCCESSFULLY!"
        writeLogFile("temp.xls", args[1], args[2])
        print "\nLOG FILE HAS BEEN COPIED TO THE EXCEL WORKBOOK SUCCESSFULLY!"
        #clean up temp file
        os.remove("temp.xls")
        #clean up source xls file
        os.remove("source.xls")
    else:
        print "Not the right number of args, 5 are needed for this version."
        print "See the excelAutomation.bat file for an example. Printing args..."
        for string in args:
            print string

if __name__ == '__main__':
    main(sys.argv[1:])
