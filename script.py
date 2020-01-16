import re
import string
import os, time
import datetime
import os
import keyword

#regexINV = r"^(?:INV)\+(?:[^+\n]*\+){4}(\d{8})"
#regexFal = r"^(?:FAL)\+(?:[^+\n]*\+){6}(\d{8})"
#regexDat = r"(?<=DAT\+)\d{8}"

path = input("Folder path:  " )
path = path + "/"


while True:
    try:
        invDays = int(input("INV days: " ))
        falDays = int(input("FAL days: "))
        datDays = int(input("DAT days: "))
    except ValueError:
        print("Expected number")
        continue
    else:
        break




def getSegmentName(line): 
    return line.split("+")[0]
    
    
def getVersionNumber(segments):
    for segment in segments:
        if getSegmentName(segment) == "UNH":
            return int(segment.split("+")[2][6])



def subDate(line,days,indexNr):
    splittedLine = line.split("+") 
    currentDate = splittedLine[indexNr]
    print("Old date: ", currentDate) 
    dateUpdate = datetime.datetime.strptime(currentDate, '%Y%m%d').date() + datetime.timedelta(days = days)
    print("New date: ", dateUpdate)
    splittedLine[indexNr] = currentDate.replace(currentDate,dateUpdate.strftime('%Y%m%d'))
    joinSplittedLine = '+'.join(map(str,splittedLine))
    #print("joined splitted line: ", joinSplittedLine)
    print("New segment: ", joinSplittedLine)
    return joinSplittedLine

       
directory = os.listdir(path)

for file in directory:
    print("----------- file name:" , file , "-----------") 
    with open (path + file , "r+", encoding='utf-8-sig') as edifactile:
        segments = edifactile.readlines()
        versionNumber = getVersionNumber(segments)
        segmentsNew = []
        for segment in segments:
            segmmentName = getSegmentName(segment)
            if segmmentName == "INV":
                segmentsNew.append(subDate(segment, invDays, 5))       
            elif segmmentName == "FAL":
                if versionNumber == 1:
                    segmentsNew.append(subDate(segment, invDays, 7))
                elif versionNumber == 2:
                    segmentsNew.append(subDate(segment, invDays, 7))
                elif versionNumber > 2:
                    segmentsNew.append(subDate(segment, invDays, 6))
            elif segmmentName == "DAT": 
                segmentsNew.append(subDate(segment, invDays, 1)) 
            else:
                segmentsNew.append(segment)
        edifactile.seek(0)
        edifactile.truncate()
        edifactile.writelines(segmentsNew)

os.system("pause")









        






