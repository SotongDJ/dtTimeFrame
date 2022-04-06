#!/usr/bin/env python3
import pathlib, time
from subprocess import call

class tag():
    def __init__(self):
        self.begin_time_str = ""
        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

        self.error_log_bool = True
        self.log_name_str = ""
        self.log_path_str = "config/"
        self.script_export_bool = False
        
    def startLog(self):
        self.begin_time_str = time.strftime("%Y%m%d%H%M%S")
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")

        pathStr = "{}{}.log".format(
            self.log_path_str,self.log_name_str
        )
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write("")

        if open(pathStr).read() != "":
            with open(pathStr,'a') as logFileHandle:
                logFileHandle.write("\n\n----\n\n")

        self.delimiter_str = "- :" # for convertTime()
        self.phrase_str = "Begin at {}".format(self.convertTime())
        
        self.printPhrase()
        self.printDashLine()

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

    def printTimeStamp(self):
        pathStr = "{}{}.log".format(
            self.log_path_str,self.log_name_str
        )
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        self.delimiter_str = "- :" # for convertTime()
        timeMsgStr = "[{}] {}".format(self.convertTime(),self.phrase_str)
        print( timeMsgStr )
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write( timeMsgStr+"\n" )
        
        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

    def runCommand(self,targetStr=""):
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)
        scriptStr = "{}{}.sh".format(self.log_path_str,self.log_name_str)
        pathStr = "{}{}.log".format(self.log_path_str,self.log_name_str)
        if self.error_log_bool:
            errorStr = "{}{}-error.log".format(self.log_path_str,self.log_name_str)
        else:
            errorStr = "/tmp/{}-error.log".format(self.log_name_str)
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        self.delimiter_str = "- :" # for convertTime()
        timeMsgStr = "[{}] Run command: {}".format(self.convertTime(),self.phrase_str)
        print( timeMsgStr )
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write( timeMsgStr + "\n" )
        
        with open(errorStr,'a') as logFileHandle:
            logFileHandle.write( timeMsgStr + "\n" )
        
        commandList = self.phrase_str.split(" ")
        if "" in commandList:
            errorMsgStr = "\n[libCommand ERROR MSG] \"\" in command line\n"
            print(errorMsgStr)
            with open(errorStr,'a') as logFileHandle:
                logFileHandle.write( errorMsgStr + "\n" )
            
        if self.script_export_bool:
            with open(scriptStr,"a") as target:
                target.write(" ".join(commandList)+"\n")
        elif targetStr == "":
            call(commandList, stdout=open(pathStr,'a'),stderr=open(errorStr,'a'))
        else:
            print("    Output file: {}\n".format(targetStr))
            with open(errorStr,"a") as target:
                target.write("    Output file: {}\n".format(targetStr))
            call(commandList, stdout=open(targetStr,'w'),stderr=open(errorStr,'a'))

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""
        
    def printing(self,printMsgStr):
        pathStr = "{}{}.log".format(
            self.log_path_str,self.log_name_str
        )
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        print(printMsgStr)
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write(printMsgStr+"\n")

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""
        
    def printPhrase(self):
        pathStr = "{}{}.log".format(
            self.log_path_str,self.log_name_str
        )
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        print(self.phrase_str)
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write(self.phrase_str+"\n")

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

    def printBlankLine(self):
        pathStr = "{}{}.log".format(
            self.log_path_str,self.log_name_str
        )
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        print("  ")
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write("  \n")

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

    def printDashLine(self):
        pathStr = "{}{}.log".format(
            self.log_path_str,self.log_name_str
        )
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        print("----------")
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write("----------\n")

        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_str = ""

    def convertTime(self):
        yearStr   = self.current_time_str[0:4]
        monthStr  = self.current_time_str[4:6]
        dayStr    = self.current_time_str[6:8]
        hourStr   = self.current_time_str[8:10]
        minuteStr = self.current_time_str[10:12]
        secondStr = self.current_time_str[12:14]

        if len(self.delimiter_str) != 3:
            self.delimiter_str =  "-_-"

        convertedMsgStr = (
            self.delimiter_str[0].join([ yearStr, monthStr, dayStr ])
            + self.delimiter_str[1]
            + self.delimiter_str[2].join([ hourStr, minuteStr, secondStr ]))

        return convertedMsgStr

    def stopLog(self):
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        # yearDiffInt   = int(self.current_time_str[0:4])  -int(self.begin_time_str[0:4])
        # monthDiffInt  = int(self.current_time_str[4:6])  -int(self.begin_time_str[4:6])
        dayDiffInt    = int(self.current_time_str[6:8])  -int(self.begin_time_str[6:8])
        hourDiffInt   = int(self.current_time_str[8:10]) -int(self.begin_time_str[8:10])
        minuteDiffInt = int(self.current_time_str[10:12])-int(self.begin_time_str[10:12])
        secondDiffInt = int(self.current_time_str[12:14])-int(self.begin_time_str[12:14])

        if secondDiffInt < 0 :
            minuteDiffInt = minuteDiffInt -1
            secondDiffInt = secondDiffInt + 60

        if minuteDiffInt < 0 :
            hourDiffInt = hourDiffInt -1
            minuteDiffInt = minuteDiffInt + 60

        if hourDiffInt < 0 :
            dayDiffInt = dayDiffInt -1
            hourDiffInt = hourDiffInt + 24

        if dayDiffInt < 0 :
            totalTimeStr = "More than one month..."
        else:
            totalTimeStr = (
                str(hourDiffInt) + " hr "+
                str(minuteDiffInt) + " min "+
                str(secondDiffInt) + " s "
            )

        self.delimiter_str = "- :" #for convertTime()
        self.phrase_str = "Finished on [{}]\n     Total time: {}\n".format(
            self.convertTime(),
            totalTimeStr
        )
        self.printPhrase()

        self.phrase_str = ""
        self.current_time_str = ""
