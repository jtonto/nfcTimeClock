#IMPORTS
import os
import datetime
import time
#TEMPLATES
date= time.strftime("%m-%d-%Y")
ctime= datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
when= str(ctime)
OutputFile= 'ASMRoster.txt'#    Your roster
fileN= 'whoDis.txt'#            Your user registry

#MANAGES WHODIS REGISTRY
def addName(fileN):
    'Pairs a new UID with a name and other info to the whoDis.txt'
    newUID= input('Enter UID: ')
    newName= input('Enter First and Last Name: ')
    #add other details here newThing= input('Enter info you want to know: ')
    fout= open(fileN, 'a')
    fout.write( newUID + ':'+ newName)
    fout.close()
def whoDis(UID, fileN):
    'Checks a tagID against a name conversion list'
    inf= open(fileN, 'r')
    lines= inf.readlines()
    inf.close()

    name= 'NotFoundError'
    for line in lines:
        if line.startswith(UID)== True:
            'You got the right profile'
            name= line.split(':')
            name= name[1]
            name= name.strip()
    return name
#FILE NAVIGATION HELPER FUNCTIONS
def isHere(OutputFile, name):
    'determines if current user should be signing in or out'
    count=0
    fout= open(OutputFile, "r")
    names= fout.readlines()
    fout.close()
    for line in names:
        if name in line:
            count+= 1
    if count%2==0:
        return True
    else:
        return False
def lineNum(OutputFile):
    'Numbers the lines for the attendance log'
    inf= open(OutputFile, 'r')
    lst= inf.readlines()
    inf.close()
    return str(len(lst)+1)
def checkDupe(OutputFile, name):
    'Searches the log and returns TRUE if a duplicate attempt is being made'
    fout= open(OutputFile, "r")
    lines= fout.readlines()
    fout.close()
    if len(lines)>0:
        if name in lines[-1] and datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") in line[-1]:
            return True
        else:
            return False
def goWrite(OutputFile, name, here):
    'logs if a student is present or not then swaps for repeat swipes'
    fout= open(OutputFile, "a")
    fdaily= open('LogFor'+time.strftime("%m-%d-%Y"), 'a')
    if here== True:
        fdaily.write(lineNum(OutputFile) + ': ' + name+' checked in at:  ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
        fout.write( lineNum(OutputFile) + ': ' + name+' checked in at:  ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
    elif here== False:
        fdaily.write(lineNum(OutputFile) + ': ' + name+' checked out at:  ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
        fout.write( lineNum(OutputFile) + ': ' +name+' checked out at: ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
    fout.close()
#FUNCTIONS TO WRITE LOGS  
def checkIn(OutputFile, name):
    'exports a list of students checking in individually'
    count= 0
    if os.path.exists(OutputFile):
        fout= open(OutputFile, "r")
        names= fout.readlines()
        fout.close()
        for line in names:
            if name in line:
                count+= 1
        if checkDupe(OutputFile, name)== False:
            goWrite(OutputFile, name, isHere)
    else:
        fout= open(OutputFile, "w")
        goWrite(OutputFile, name, True, datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") )
        fout.close()
def buildRoster(OutputFile):
    'signs students in and out and post to OutputFile (main program loop)'
    done= False
    while not done:
        UID= input("Tap now (enter 'u' for undo; 'f' to find information about a person or day or nothing to stop): ")
        if UID== '':
            done= True
        elif UID.lower()== 'a':#CASE FOR ADDING A NEW NAME
            addName(fileN)
        elif UID.lower()== 'f':#CASE FOR USER SEARCHING
            answer= input('Would you like to search for a Person(p) or Day(d)?')
            if answer.lower()== 'p':#Looking for a person
                pullName(OutputFile)
            if answer.lower()== 'd':#Looking for a certain day
                pullDate(OutputFile)
        elif UID.lower()== 'u':#CASE FOR UNDO
            undoError(OutputFile)
        else:
            UID= UID.upper()
            name= whoDis(UID, fileN)
            file= open(OutputFile, "a")
            if isHere(OutputFile, name)== True:
                file.write( lineNum(OutputFile) + ': ' + name+' checked in at:  ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
                print(' Welcome back '+ name + datetime.datetime.now().strftime("! The time is: %I:%M%p"))
            else:
                file.write( lineNum(OutputFile) + ': ' +name+' checked out at: ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + '\n')
                print('Goodbye '+ name + datetime.datetime.now().strftime(" The time is: %I:%M%p"))
            file.close()   
#FUNCTIONS TO SEARCH THROUGH LOG(pullDate and pullName are not consistently functional)
def pullDate(OutputFile):
    'Finds information from the chosen date'
    fin= open(OutputFile, 'r')
    taps= fin.readlines()
    fin.close()
    uDate= input("Enter date to search for(month dd, yyyy): ")
    uDate= uDate.lower()
    
    tapLst= []
    for tap in taps:
        dateLst= tap.split('on ')
        if dateLst[1].lower()== uDate:
            found= dateLst[1]
            tapLst.append(found)
    
    print(tapLst)
    print(dateLst)  
def pullName(OutputFile):
    'Finds information from the chosen date'
    fin= open(OutputFile, 'r')
    taps= fin.readlines()
    fin.close()
    uName= input("Enter a name to search for(First Last): ")
    uName= uName.lower()
    
    tapLst= []
    for tap in taps:
        if uName in tap.lower():
            tapLst.append(tap)
    return(tapLst)
#USER COMMANDS
def undoError(OutputFile):
    'Deletes the last line from the Output file'
    fin= open(OutputFile, 'r')
    taps= fin.readlines()
    fin.close()
    taps= taps[:-1]
    fout= open(OutputFile, 'w')
    for tap in taps:
        fout.write(tap)
        fout.close()
def printToday(OutputFile):
    'Sorts for taps done today and returns them'
    fin= open(OutputFile, 'r')
    taps= fin.readlines()
    fin.close()
    todayLog= []
    for tap in taps:
        if time.strftime("%m-%d-%Y") in tap:
            todayLog.append(tap)
    return todayLog
def countTime(OutputFile):
    'This totals a users time '
    pass

print('Welcome to HPAC!')
buildRoster(OutputFile)