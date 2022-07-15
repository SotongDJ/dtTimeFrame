#!/usr/bin/env python3
import sys, pathlib, json, time, datetime
from subprocess import call
#
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
    def clear(self): # clear content
        if self.name != "":
            with open(self.name,'w') as target_handle:
                    target_handle.write("")
#
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
        #
        self.record_dict = dict()
        self.json_name = ""
    def clearFile(self):
        self.log.clear()
        self.error.clear()
        self.script.clear()
    def print(self,word_str,end="\n"):
        log_list = [self.log,self.error]
        for target in log_list:
            if target.name != "":
                with target.handle() as target_handle:
                    target_handle.write(word_str+end)
        if self.print_bool:
            print(word_str)
    def record(self,time_str,content_str):
        count_int = len(self.record_dict)
        if count_int == 0:
            diff_str = "Initial, 0 s"
        else:
            diff_dict = self.measureTime(self.record_dict[count_int-1]["time_stamp"],time_str)
            diff_str = "{day} day {hour} hr {minute} min {second} s".format(**diff_dict)
        self.record_dict[count_int] = {
            "time_stamp": time_str,
            "print_msg": content_str,
            "time_diff": diff_str,
        }
    def start(self):
        self.begin_time_str = time.strftime("%Y%m%d%H%M%S")
        convert_time_str = self.convertTime(current=self.begin_time_str)
        phrase_str = F"Begin at {convert_time_str}"
        self.print(phrase_str)
        self.record(self.begin_time_str,phrase_str)
    def timeStamp(self,word_str):
        current_time_str = time.strftime("%Y%m%d%H%M%S")
        convert_time_str = self.convertTime(current=current_time_str)
        time_msg_str = "[{}] Note: {}".format(convert_time_str,word_str)
        self.print(time_msg_str)
        self.record(current_time_str,time_msg_str)
    def runCommand(self,word_str,export_file=None,mode="a"):
        current_time_str = time.strftime("%Y%m%d%H%M%S")
        convert_time_str = self.convertTime(current=current_time_str)
        time_msg_str = "[{}] Run command: {}".format(convert_time_str,word_str)
        self.print(time_msg_str)
        self.record(current_time_str,time_msg_str)
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
    def getTimeDict(self,input_str):
        time_dict = {
            "year"  : input_str[0:4],
            "month" : input_str[4:6],
            "day"   : input_str[6:8],
            "hour"  : input_str[8:10],
            "minute": input_str[10:12],
            "second": input_str[12:14],
        }
        return time_dict
    def convertTime(self,current=""):
        if current == "":
            current = time.strftime("%Y%m%d%H%M%S")
        current_time_dict = self.getTimeDict(current)
        if set(self.delimiter_dict.keys()) != set(["date","join","time"]):
            self.delimiter_dict =  {"date":"-","join":"_","time":":"}
        current_time_dict.update(self.delimiter_dict)
        format_str = "{year}{date}{month}{date}{day}{join}{hour}{time}{minute}{time}{second}"
        converted_msg_str = format_str.format(**current_time_dict)
        return converted_msg_str
    def measureTime(self,start,stop):
        int_dict = dict()
        start_date = datetime.datetime.strptime(start,"%Y%m%d%H%M%S")
        stop_date = datetime.datetime.strptime(stop,"%Y%m%d%H%M%S")
        start_int = int(datetime.datetime.timestamp(start_date))
        stop_int = int(datetime.datetime.timestamp(stop_date))
        int_dict["second"] = stop_int - start_int
        section_lists = [
            ["second","minute",60],
            ["minute","hour",60],
            ["hour","day",24],
        ]
        for section_list in section_lists:
            from_str,to_str,limit_int = section_list
            if int_dict[from_str] > limit_int:
                second_int = int_dict[from_str] % limit_int
                minite_int = int((int_dict[from_str] - second_int) / limit_int)
                int_dict[from_str] = second_int
                int_dict[to_str] = minite_int
            else:
                int_dict[to_str] = 0
        return int_dict
    def stop(self):
        current_time_str = time.strftime("%Y%m%d%H%M%S")
        diff_dict = self.measureTime(self.begin_time_str, current_time_str)
        totalTimeStr = "{day} day {hour} hr {minute} min {second} s".format(**diff_dict)
        end_phrase_str = "Finished on [{}]\n     Total time: {}"
        convert_time_str = self.convertTime(current=current_time_str)
        phrase_str = end_phrase_str.format(convert_time_str,totalTimeStr)
        self.print(phrase_str)
        self.record(current_time_str,phrase_str)
        if self.json_name != "":
            with open(self.json_name,"w") as target_handle:
                json.dump(self.record_dict,target_handle,indent=1)
#
class detector:
    def __init__(self):
        self.target_str = ""
        self.alt_target_str = ""
        self.print = print
    def missing(self):
        if pathlib.Path(self.target_str).exists():
            self.print(F"NOTE: {self.target_str} existed")
            target_bool = False
        else:
            if pathlib.Path(self.alt_target_str).exists():
                pathlib.Path(self.alt_target_str).unlink()
                self.print(F"NOTE: {self.alt_target_str} removed")
            target_bool = True
        return target_bool
    def do(self,target_str):
        self.target_str = target_str
        self.alt_target_str = "{}/{}".format(pathlib.Path(target_str).parent,"doing-"+pathlib.Path(target_str).name)
    def done(self):
        self.runCommand(F"mv -v {self.alt_target_str} {self.target_str}")
        self.target_str = ""
        self.alt_target_str = ""
