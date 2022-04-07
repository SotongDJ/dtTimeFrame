#!/usr/bin/env python3
import time, sys, json
from subprocess import call
class fileHandle:
    def __init__(self):
        self.name = ""
        self.stat = "init"
        self.alt = None
    def append(self,word_str):
        if self.name != "":
            with open(self.name,'a') as target_handle:
                if self.stat != "on":
                    if open(self.name).read() != "":
                        target_handle.write("----------\n")
                    self.stat = "on"
                target_handle.write(word_str)
    def handle(self,mode='a'):
        if self.name == "":
            return self.alt
        else:
            self.append("")
            return open(self.name,mode)
class tag:
    def __init__(self):
        #
        self.begin_time_str = ""
        self.delimiter_dict = {"date":"-","join":" ","time":":"}
        self.print_bool = True
        #
        self.log = fileHandle()
        self.log.alt = sys.stdout
        self.error = fileHandle()
        self.error.alt = sys.stderr
        self.script = fileHandle()
        self.json_name = ""
    def print(self,word_str,end="\n"):
        log_list = [self.log,self.error,self.script]
        for target in log_list:
            if target.name != "":
                with target.handle() as target_handle:
                    target_handle.write(word_str+end)
        if self.print_bool:
            print(word_str)
    def start(self):
        self.begin_time_str = time.strftime("%Y%m%d%H%M%S")
        phrase_str = "Begin at {}".format(self.convertTime())
        #
        self.print(phrase_str)
        self.dash()
    def timeStamp(self,word_str):
        time_msg_str = "[{}] {}".format(self.convertTime(),word_str)
        self.print(time_msg_str)
    def runCommand(self,word_str,export_file=None,mode="a"):
        time_msg_str = "[{}] Run command: {}".format(self.convertTime(),word_str)
        self.print(time_msg_str)
        commandList = word_str.split(" ")
        mode_dict = {"a":" >> ","w":" > "}
        if "" in commandList:
            error_msg_str = "\n[libCommand ERROR MSG] empty command line\n"
            self.print(error_msg_str)
        if export_file:
            output_msg_str = F"    Output file: {export_file}"
            self.print(output_msg_str)
            if self.script.name == "":
                call(commandList, stdout=open(export_file,mode),stderr=self.error.handle())
            else:
                with self.script.handle() as script_handle:
                    script_handle.write(" ".join(commandList)+mode_dict[mode]+F"{export_file}\n")
        else:
            if self.script.name == "":
                call(commandList, stdout=self.log.handle(),stderr=self.error.handle())
            else:
                with self.script.handle() as script_handle:
                    script_handle.write(" ".join(commandList)+"\n")
    def blank(self):
        self.print("  ")
    def dash(self):
        self.print("----------")
    def convertTime(self):
        current_time_str = time.strftime("%Y%m%d%H%M%S")
        yearStr   = current_time_str[0:4]
        monthStr  = current_time_str[4:6]
        dayStr    = current_time_str[6:8]
        hourStr   = current_time_str[8:10]
        minuteStr = current_time_str[10:12]
        secondStr = current_time_str[12:14]
        # fallback
        if set(self.delimiter_dict.keys()) != set(["date","time","join"]):
            self.delimiter_dict =  {"date":"-","join":"_","time":"-"}
        date_str = self.delimiter_dict["date"].join([yearStr, monthStr, dayStr])
        time_str = self.delimiter_dict["time"].join([hourStr, minuteStr, secondStr])
        converted_msg_str = (self.delimiter_dict["join"].join([date_str,time_str]))
        return converted_msg_str
    def stop(self):
        current_time_str = time.strftime("%Y%m%d%H%M%S")
        # yearDiffInt   = int(current_time_str[0:4])-int(self.begin_time_str[0:4])
        # monthDiffInt  = int(current_time_str[4:6])-int(self.begin_time_str[4:6])
        dayDiffInt    = int(current_time_str[6:8])-int(self.begin_time_str[6:8])
        hourDiffInt   = int(current_time_str[8:10])-int(self.begin_time_str[8:10])
        minuteDiffInt = int(current_time_str[10:12])-int(self.begin_time_str[10:12])
        secondDiffInt = int(current_time_str[12:14])-int(self.begin_time_str[12:14])
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
        end_phrase_str = "Finished on [{}]\n     Total time: {}"
        phrase_str = end_phrase_str.format(self.convertTime(),totalTimeStr)
        self.print(phrase_str)
