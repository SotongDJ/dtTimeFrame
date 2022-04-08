#!/usr/bin/env python3
import libTimeTag
from subprocess import call
class timer(libTimeTag.tag):
    def __init__(self):
        #
        self.beginTimeStr = ""
        # self.currentTimeStr = "" # abandoned
        self.phraseStr = ""
        self.delimiterStr = ""
        #
        self.logFilenameStr = ""
        self.folderStr = "config/"
        self.testingBool = False
        self.errorBool = True
        #
        self.begin_time_str = ""
        self.delimiter_dict = {"date":"-","join":" ","time":":"}
        self.print_bool = True
        #
        self.log = libTimeTag.fileHandle()
        self.log.alt = sys.stdout
        self.error = libTimeTag.fileHandle()
        self.error.alt = sys.stderr
        self.script = libTimeTag.fileHandle()
        self.json_name = ""
    def convertDelimiter(self):
        date_str = self.delimiterStr[0]
        join_str = self.delimiterStr[1]
        time_str = self.delimiterStr[2]
        self.delimiter_dict = {"date":date_str,"join":join_str,"time":time_str}
    def startLog(self):
        self.log.name = F"{self.folderStr}{self.logFilenameStr}-log.txt"
        self.delimiterStr = "- :" # for convertTime()
        self.convertDelimiter()
        self.start()
        self.beginTimeStr = self.begin_time_str
    def printTimeStamp(self):
        self.timeStamp(self.phraseStr)
        self.phraseStr = ""
    def runCommand(self,targetStr="",mode="a"):
        time_msg_str = "[{}] Run command: {}".format(self.convertTime(),self.phraseStr)
        self.print(time_msg_str)
        commandList = self.phraseStr.split(" ")
        mode_dict = {"a":" >> ","w":" > "}
        if self.testingBool:
            self.script.name = F"{self.folderStr}{self.logFilenameStr}.sh"
        if self.errorBool:
            self.error.name = F"{self.folderStr}{self.logFilenameStr}-error.log"
        else:
            self.error.name = F"/tmp/{self.logFilenameStr}-error.log"
        if "" in commandList:
            error_msg_str = "\n[libCommand ERROR MSG] empty command line\n"
            self.print(error_msg_str)
        if targetStr != "":
            output_msg_str = F"    Output file: {targetStr}"
            self.print(output_msg_str)
            if self.testingBool:
                with self.script.handle() as script_handle:
                    script_handle.write(" ".join(commandList)+mode_dict[mode]+F"{export_file}\n")
            else:
                call(commandList, stdout=open(targetStr,mode),stderr=self.error.handle())
        else:
            if self.testingBool:
                with self.script.handle() as script_handle:
                    script_handle.write(" ".join(commandList)+"\n")
            else:
                call(commandList, stdout=self.log.handle(),stderr=self.error.handle())
    def printing(self,printMsgStr):
        self.print(printMsgStr)
    def printPhrase(self):
        self.print(self.phraseStr)
        self.phraseStr = ""
    def printBlankLine(self):
        self.blank()
    def printDashLine(self):
        self.dash()
    def stopLog(self):
        self.begin_time_str = self.beginTimeStr
        self.convertDelimiter()
        self.stop()
