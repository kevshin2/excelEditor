from xlutils.copy import copy
import xlrd
import sys
import os
import datetime

"""converts dates to their proper format"""
def convertDate(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY: return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN: return cell.value == 1
    return cell.value

"""writes contents of argument 2 to the EIF TCS sheet of argument 1
    and writes it to a temp location"""
def writeLogFile(locationOfSheetToBeCopied, locationOfLogFile):
    writeSheet = xlrd.open_workbook(locationOfSheetToBeCopied, sys.stdout, 0, True, "", "None", "None",True)

    numberOfRows = writeSheet.sheet_by_index(8).nrows

    writeSheet = copy(writeSheet)

    logFile = open(locationOfLogFile, 'r')
    
    rowPosition = 2

    for line in logFile:
        writeSheet.get_sheet(8).write(rowPosition,0, line)
        rowPosition += 1

    #"delete" rows if logfile isnt longer than the previous logfile
    while rowPosition < numberOfRows:
        rowPosition += 1
        writeSheet.get_sheet(8).write(rowPosition,0,"")
    
    logFile.close()
        
    writeSheet.save("temp.xls")
    
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
                contentsOfRow.append(str(convertDate(eifStatus.cell(rowPosition,colPosition),0)))             
            colPosition += 1
        rowPosition += 1
        contentsOfCells[rowPosition] = contentsOfRow
        colPosition = 0

    writeSheet = copy(readSheet)

    #write back the cells with new row inserted
    for row in contentsOfCells:
        while colPosition < numberOfColumns:
            writeSheet.get_sheet(3).write(row,colPosition,contentsOfCells[row][colPosition]) 
            colPosition += 1
            
        colPosition = 0
   
    writeSheet.save(locationOfWriteBack)
    readSheet.release_resources()

"""takes the name of a log file and parses it for info, returns a list representing the entry"""
def generateEntry(locationOfLogFile, name, buildName):
    
    logFile = open(locationOfLogFile, "r")
    
    logFile.close()
    
    return [str(datetime.date.today()),"Test","Test",name, buildName]
    
    

def main(args):
    if len(args) == 5:
        writeLogFile(args[0], args[1])
        print "\nLOG FILE HAS BEEN COPIED TO THE EXCEL WORKBOOK SUCCESSFULLY!"
        insertEntry("temp.xls",args[2], args[1], args[3], args[4])
        print "\nENTRY INSERTED SUCCESSFULLY!"
        #clean up temp file
        os.remove("temp.xls")
    else:
        print "Not the right number of args, 5 are needed for this version."
        print "See the *.bat file for an example Printing args..."
        for string in args:
            print string

if __name__ == '__main__':
    main(sys.argv[1:])
