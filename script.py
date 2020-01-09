import re
import string
import os, time
import datetime



#regexINV = r"^(?:INV)\+(?:[^+\n]*\+){4}(\d{8})"
#regexFal = r"^(?:FAL)\+(?:[^+\n]*\+){6}(\d{8})"
#regexDat = r"(?<=DAT\+)\d{8}"


invDays = int(input("INV days: " ))
falDays = int(input("FAL days: "))
datDays = int(input("DAT days: "))

#formatedINVdate = ("\\g<1>" + INVDays)
#print(formatedINVdate)

def getSegmentName(line): 
    return line.split("+")[0]
    
    
def getVersionNumber(line):
    splittedLine = line.split("+")
    #print("splitted INV line from get version function: ", splittedLine)
    versionNumber = splittedLine[1][10]
    print("version number from get version function: ", versionNumber)
    return versionNumber



def subDate(line,days,indexNr):
    splittedLine = line.split("+") 
    currentDate = splittedLine[indexNr] 
    dateUpdate = datetime.datetime.strptime(currentDate, '%Y%m%d').date() + datetime.timedelta(days = days)
    print("date after strptime: ", dateUpdate)
    splittedLine[indexNr] = currentDate.replace(currentDate,dateUpdate.strftime('%Y%m%d'))
    joinSplittedLine = '+'.join(map(str,splittedLine))
    print("joined splitted line: ", joinSplittedLine)
    return joinSplittedLine
   

#subbedDate = re.sub(pattern,newDate.strftime("%Y%m%d"),line)
#print("subbed date: ", subbedDate)


with open ("testedifact.edi", "r") as edifactile:
    for line in edifactile:
        segmmentName = getSegmentName(line)
        if segmmentName == "INV":
            versionNumber = getVersionNumber(line)
            subDate(line, invDays, 5) 
            #replace the line with the return value of subdate function        
        elif segmmentName == "FAL":
            if (versionNumber == "1" or "2"):
                subDate(line, falDays, 7)
            elif versionNumber > "2":
                subDate(line, falDays, 6 )
        elif segmmentName == "DAT": 
            subDate(line, datDays, 1)
            
              
       
        






