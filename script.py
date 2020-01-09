import re
import string
import os, time
import datetime
import fileinput

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
    
    
def getVersionNumber(segments):
    for segment in segments:
        if getSegmentName(segment) == "UNH":
            return segment.split("+")[2][6]



def subDate(line,days,indexNr):
    splittedLine = line.split("+") 
    currentDate = splittedLine[indexNr] 
    dateUpdate = datetime.datetime.strptime(currentDate, '%Y%m%d').date() + datetime.timedelta(days = days)
    print("date after strptime: ", dateUpdate)
    splittedLine[indexNr] = currentDate.replace(currentDate,dateUpdate.strftime('%Y%m%d'))
    joinSplittedLine = '+'.join(map(str,splittedLine))
    print("joined splitted line: ", joinSplittedLine)
    return joinSplittedLine



segmentsNew = []
global segments  
with open ("testedifact.edi" , "r+") as edifactile:
    segments = edifactile.readlines()
    versionNumber = getVersionNumber(segments)
    for segment in segments:
        segmmentName = getSegmentName(segment)
        if segmmentName == "INV":
            segmentsNew.append(subDate(segment, invDays, 5))       
        elif segmmentName == "FAL":
            if (versionNumber == "1" or "2"):
                segmentsNew.append(subDate(segment, invDays, 7)) 
            elif versionNumber > "2":
                segmentsNew.append(subDate(segment, invDays, 6)) 
        elif segmmentName == "DAT": 
            segmentsNew.append(subDate(segment, invDays, 1)) 
        else:
            segmentsNew.append(segment)
edifactile.close()
with open ("testedifact.edi" , "w") as edifactile:
    print(segmentsNew)
    edifactile.writelines(segmentsNew)
edifactile.close()


        






