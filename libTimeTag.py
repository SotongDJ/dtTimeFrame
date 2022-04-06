#!/usr/bin/env python3
import pathlib, time, sys
from subprocess import call
class logFile:
    def __init__(self):
        self.log_name = None
        self.error_name = None
    def create(self,log_name,err=None):
        self.log_name = log_name
        if err:
            self.error_name = err
        self.append("",print_bool=False)
        if open(self.log_name).read() != "":
            if self.error_name:
                if open(self.error_name).read() != "":
                    self.append("\n\n----\n\n",print_bool=False)
            else:
                self.append("\n\n----\n\n",print_bool=False)
    def append(self,word_str,print_bool=True):
        if self.log_name:
            with open(self.log_name,'a') as logFileHandle:
                logFileHandle.write(word_str+"\n")
            if self.error_name:
                with open(self.error_name,'a') as logFileHandle:
                    logFileHandle.write(word_str+"\n")
        if print_bool:
            print(word_str)
    def error(self,word_str):
        if self.log_name:
            if self.error_name:
                with open(self.error_name,'a') as logFileHandle:
                    logFileHandle.write(word_str+"\n")
            else:
                with open(self.log_name,'a') as logFileHandle:
                    logFileHandle.write("ERROR: no specific error log file\n"+word_str+"\n")
        print(word_str)
    def log_handle(self):
        if self.log_name:
            return open(self.log_name,'a')
        else:
            return sys.stdout
    def err_handle(self):
        if self.error_name:
            return open(self.error_name,'a')
        else:
            return sys.stderr

class tag:
    def __init__(self):
        #
        self.begin_time_str = ""
        self.current_time_str = ""
        self.phrase_str = ""
        self.delimiter_dict = {"date":"-","join":" ","time":":"}
        #
        self.log_name_str = ""
        self.log_path_str = "config/"
        self.log_bool = True
        self.log_file_handle = logFile()
        self.error_log_bool = True
        self.script_export_bool = False
    def startLog(self):
        self.begin_time_str = time.strftime("%Y%m%d%H%M%S")
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        if self.log_bool:
            pathlib.Path(self.log_path_str).mkdir(parents=True,exist_ok=True)
            path_str = F"{self.log_path_str}{self.log_name_str}-log.txt"
            if self.error_log_bool:
                error_path_str = F"{self.log_path_str}{self.log_name_str}-log-error.txt"
                self.log_file_handle.create(path_str,err=error_path_str)
            else:
                self.log_file_handle.create(path_str)
        self.phrase_str = "Begin at {}".format(self.convertTime())
        #
        self.printPhrase()
        self.printDashLine()
    def printTimeStamp(self):
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        time_msg_str = "[{}] {}".format(self.convertTime(),self.phrase_str)
        self.log_file_handle.append(time_msg_str)
        #
        self.current_time_str = ""
        self.phrase_str = ""
    def runCommand(self,targetStr=None):
        self.current_time_str = time.strftime("%Y%m%d%H%M%S")
        time_msg_str = "[{}] Run command: {}".format(self.convertTime(),self.phrase_str)
        self.log_file_handle.append(time_msg_str)
        #
        commandList = self.phrase_str.split(" ")
        if "" in commandList:
            error_msg_str = "\n[libCommand ERROR MSG] \"\" in command line\n"
            self.log_file_handle.error(error_msg_str)  
        if self.script_export_bool:
            script_str = F"{self.log_path_str}{self.log_name_str}.sh"
            with open(script_str,"a") as target:
                target.write(" ".join(commandList)+"\n")
        elif targetStr:
            output_msg_str = F"    Output file: {targetStr}"
            self.log_file_handle.append(output_msg_str)
            call(commandList, stdout=open(targetStr,'w'),stderr=self.log_file_handle.err_handle())
        else:
            call(commandList, stdout=self.log_file_handle.log_handle(),stderr=self.log_file_handle.err_handle())
        #
        self.current_time_str = ""
        self.phrase_str = ""
    def printing(self,printMsgStr):
        self.log_file_handle.append(printMsgStr)
    def printPhrase(self):
        self.log_file_handle.append(self.phrase_str)
        self.phrase_str = ""
    def printBlankLine(self):
        self.log_file_handle.append("  ")
    def printDashLine(self):
        self.log_file_handle.append("----------")
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
        # yearDiffInt   = int(self.current_time_str[0:4])-int(self.begin_time_str[0:4])
        # monthDiffInt  = int(self.current_time_str[4:6])-int(self.begin_time_str[4:6])
        dayDiffInt    = int(self.current_time_str[6:8])-int(self.begin_time_str[6:8])
        hourDiffInt   = int(self.current_time_str[8:10])-int(self.begin_time_str[8:10])
        minuteDiffInt = int(self.current_time_str[10:12])-int(self.begin_time_str[10:12])
        secondDiffInt = int(self.current_time_str[12:14])-int(self.begin_time_str[12:14])
        if secondDiffInt < 0 :
            minuteDiffInt = minuteDiffInt-1
            secondDiffInt = secondDiffInt+60
        if minuteDiffInt < 0 :
            hourDiffInt = hourDiffInt-1
            minuteDiffInt = minuteDiffInt+60
        if hourDiffInt < 0 :
            dayDiffInt = dayDiffInt-1
            hourDiffInt = hourDiffInt+24
        if dayDiffInt < 0 :
            totalTimeStr = "More than one month..."
        else:
            totalTimeStr = F"{hourDiffInt} hr {minuteDiffInt} min {secondDiffInt} s"
        end_phrase_str = "Finished on [{}]\n     Total time: {}\n"
        self.phrase_str = end_phrase_str.format(self.convertTime(),totalTimeStr)
        self.printPhrase()
