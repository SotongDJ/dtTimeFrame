#!/usr/bin/env python3
import pathlib, time
from subprocess import call

class tag():
    def __init__(self):
        self.begin_time_str = ""
        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_dict = {"date":"-","join":" ","time":":"}

        self.log_name_str = ""
        self.log_path_str = "config/"
        self.error_log_bool = True
        self.script_export_bool = False
        
    def startLog(self):
        self.begin_time_str = time.strftime("%Y%m%d%H%M%S")
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")

        pathStr = F"{self.log_path_str}{self.log_name_str}.log"
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write("")

        if open(pathStr).read() != "":
            with open(pathStr,'a') as logFileHandle:
                logFileHandle.write("\n\n----\n\n")

        self.phrase_str = "Begin at {}".format(self.convertTime())
        
        self.printPhrase()
        self.printDashLine()

    def printTimeStamp(self):
        pathStr = F"{self.log_path_str}{self.log_name_str}.log"
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        timeMsgStr = "[{}] {}".format(self.convertTime(),self.phrase_str)
        print( timeMsgStr )
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write( timeMsgStr+"\n" )
        
        self.current_time_str = ""
        self.phrase_str = ""

    def runCommand(self,targetStr=""):
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)
        scriptStr = F"{self.log_path_str}{self.log_name_str}.sh"
        pathStr = F"{self.log_path_str}{self.log_name_str}.log"
        if self.error_log_bool:
            errorStr = F"{self.log_path_str}{self.log_name_str}-error.log"
        else:
            errorStr = F"/tmp/{self.log_name_str}-error.log"
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
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
            print(F"    Output file: {targetStr}\n")
            with open(errorStr,"a") as target:
                target.write(F"    Output file: {targetStr}\n")
            call(commandList, stdout=open(targetStr,'w'),stderr=open(errorStr,'a'))

        self.current_time_str = ""
        self.phrase_str = ""
        
    def printing(self,printMsgStr):
        pathStr = F"{self.log_path_str}{self.log_name_str}.log"
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        print(printMsgStr)
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write(printMsgStr+"\n")

        self.current_time_str = ""
        self.phrase_str = ""
        
    def printPhrase(self):
        pathStr = F"{self.log_path_str}{self.log_name_str}.log"
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        print(self.phrase_str)
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write(self.phrase_str+"\n")

        self.current_time_str = ""
        self.phrase_str = ""

    def printBlankLine(self):
        pathStr = F"{self.log_path_str}{self.log_name_str}.log"
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        print("  ")
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write("  \n")

        self.current_time_str = ""
        self.phrase_str = ""

    def printDashLine(self):
        pathStr = F"{self.log_path_str}{self.log_name_str}.log"
        pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)

        print("----------")
        with open(pathStr,'a') as logFileHandle:
            logFileHandle.write("----------\n")

        self.current_time_str = ""
        self.phrase_str = ""

    def convertTime(self):
        yearStr   = self.current_time_str[0:4]
        monthStr  = self.current_time_str[4:6]
        dayStr    = self.current_time_str[6:8]
        hourStr   = self.current_time_str[8:10]
        minuteStr = self.current_time_str[10:12]
        secondStr = self.current_time_str[12:14]
        # fallback
        if set(self.delimiter_dict.keys()) != set(["date","time","join"]):
            self.delimiter_dict =  {"date":"-","join":"_","time":"-"}
        date_str = self.delimiter_dict["date"].join([yearStr, monthStr, dayStr])
        time_str = self.delimiter_dict["time"].join([hourStr, minuteStr, secondStr])
        convertedMsgStr = (self.delimiter_dict["join"].join([date_str,time_str]))

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
        end_phrase_str = "Finished on [{}]\n     Total time: {}\n"
        self.phrase_str = end_phrase_str.format(self.convertTime(),totalTimeStr)
        self.printPhrase()
