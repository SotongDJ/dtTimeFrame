#!/usr/bin/env python3
import datetime
import json
import math
import sys
import time
from pathlib import Path
from subprocess import call
from typing import Any

#
class fileHandle:
    def __init__(self) -> None:
        self.name = ""
        self.stat = "init"
        self.alt = None
    def append(self,word_str:str) -> None:
        if self.name != "":
            with open(self.name,'a') as target_handle:
                if self.stat != "on":
                    if open(self.name).read() != "":
                        target_handle.write("----------\n")
                    self.stat = "on"
                target_handle.write(word_str)
    def handle(self,mode:str='a') -> Any:
        if self.name == "":
            return self.alt
        else:
            self.append("")
            return open(self.name,mode)
    def clear(self) -> None: # clear content
        if self.name != "":
            with open(self.name,'w') as target_handle:
                    target_handle.write("")
class recordHandle(fileHandle):
    def __init__(self, handle:Any=json) -> None:
        self.name = ""
        self.stat = "init"
        self.alt = None
        self.handle = handle
    def load(self) -> dict:
        return self.handle.load(open(self.name)) if self.name != "" else {}
    def dump(self,target_dict:dict) -> None:
        with open(self.name,"w") as target_handle:
            self.handle.dump(target_dict,target_handle)
#
class tag:
    def __init__(self) -> None:
        #
        self.begin_time_str = ""
        self.delimiter_dict = {"date":"-","join":" ","time":":"}
        self.print_bool = True
        #
        self.log = fileHandle()
        self.log.alt = sys.stdout  # type: ignore
        self.error = fileHandle()
        self.error.alt = sys.stderr  # type: ignore
        self.script = fileHandle()
        #
        # self.json_name = ""
        self.record_dict = dict()
        self.extra = recordHandle()
    def clearFile(self) -> None:
        self.log.clear()
        self.error.clear()
        self.script.clear()
        self.extra.clear()
    def print(self,word_str:str,end:str="\n") -> None:
        log_list = [self.log,self.error]
        for target in log_list:
            if target.name != "":
                with target.handle() as target_handle:  # type: ignore
                    target_handle.write(word_str+end)
        if self.print_bool:
            print(word_str)
    def record(self,time_str:str,content_str:str,command_str:str="") -> None:
        count_int = len(self.record_dict)
        if count_int == 0:
            diff_str = "Initial, 0 s"
        else:
            diff_dict = self.measureTime(self.record_dict[count_int-1]["time_stamp"],time_str)
            diff_str = "{day} day {hour} hr {minute} min {second} s".format(**diff_dict)
        record_entry_dict = {
            "time_stamp": time_str,
            "print_msg": content_str,
            "time_diff": diff_str,
        }
        if command_str != "":
            record_entry_dict["cmd"] = command_str
        self.record_dict[count_int] = record_entry_dict
    def start(self) -> None:
        self.begin_time_str = time.strftime("%Y%m%d%H%M%S")
        convert_time_str = self.convertTime(current=self.begin_time_str)
        phrase_str = F"Begin at {convert_time_str}"
        self.print(phrase_str)
        self.record(self.begin_time_str,phrase_str)
    def timeStamp(self,word_str:str,prefix_str:str="[info]") -> None:
        current_time_str = time.strftime("%Y%m%d%H%M%S")
        convert_time_str = self.convertTime(current=current_time_str)
        time_msg_str = "[{}] {} {}".format(convert_time_str,prefix_str,word_str)
        self.print(time_msg_str)
        self.record(current_time_str,time_msg_str)
    def runCommand(self,word_str:str,export_file:str="",mode:str="a",direct_out=False) -> None:
        mode_dict = {"a":" >> ","w":" > "}
        current_time_str = time.strftime("%Y%m%d%H%M%S")
        convert_time_str = self.convertTime(current=current_time_str)
        time_msg_str = "[{}] Run command: {}".format(convert_time_str,word_str)
        self.print(time_msg_str)
        commandList = word_str.split(" ")
        if export_file == "":
            full_command_str = " ".join(commandList)+"\n"
        else:
            full_command_str = " ".join(commandList)+mode_dict[mode]+F"{export_file}"+"\n"
        self.record(current_time_str,time_msg_str,command_str=full_command_str)
        if "" in commandList:
            self.print("\n[libCommand ERROR MSG] empty command line\n")
        if export_file:
            self.print(F"    Output file: {export_file}")
        if direct_out:
            call(commandList, stdout=sys.stdout,stderr=sys.stderr)
        else:
            if self.script.name == "":
                if export_file:
                    call(commandList, stdout=open(export_file,mode),stderr=self.error.handle())
                else:
                    call(commandList, stdout=self.log.handle(),stderr=self.error.handle())
            else:
                with self.script.handle() as script_handle:  # type: ignore
                    script_handle.write(full_command_str)
    def blank(self) -> None:
        self.print("  ")
    def dash(self) -> None:
        self.print("----------")
    def getTimeDict(self,input_str:str) -> dict:
        time_dict = {
            "year"  : input_str[0:4],
            "month" : input_str[4:6],
            "day"   : input_str[6:8],
            "hour"  : input_str[8:10],
            "minute": input_str[10:12],
            "second": input_str[12:14],
        }
        return time_dict
    def convertTime(self,current:str="") -> str:
        if current == "":
            current = time.strftime("%Y%m%d%H%M%S")
        current_time_dict = self.getTimeDict(current)
        if set(self.delimiter_dict.keys()) != set(["date","join","time"]):
            self.delimiter_dict =  {"date":"-","join":"_","time":":"}
        current_time_dict.update(self.delimiter_dict)
        format_str = "{year}{date}{month}{date}{day}{join}{hour}{time}{minute}{time}{second}"
        converted_msg_str = format_str.format(**current_time_dict)
        return converted_msg_str
    def measureTime(self,start:str,stop:str) -> dict:
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
    def stop(self) -> None:
        current_time_str = time.strftime("%Y%m%d%H%M%S")
        diff_dict = self.measureTime(self.begin_time_str, current_time_str)
        totalTimeStr = "{day} day {hour} hr {minute} min {second} s".format(**diff_dict)
        end_phrase_str = "Finished on [{}]\n     Total time: {}"
        convert_time_str = self.convertTime(current=current_time_str)
        phrase_str = end_phrase_str.format(convert_time_str,totalTimeStr)
        self.print(phrase_str)
        self.record(current_time_str,phrase_str)
        if self.extra.name != "":
            summary_dict = {}
            if Path(self.extra.name).exists():
                summary_dict.update(self.extra.load())
            summary_dict.update({str(len(summary_dict)+x):y for x,y in self.record_dict.items()})
            self.extra.dump(dict_sort(summary_dict))
    def checkPoint(self,input_str:str) -> bool:
        if Path("stop.txt").exists():
            self.timeStamp(F"Manually skip, as 'stop.txt' existed, at [{input_str}]")
        else:
            self.timeStamp(F"{input_str}")
        return not Path("stop.txt").exists()
#
class detector:
    def __init__(self,print_func:Any=print,call_func:Any=print,target_str:str="") -> None:
        self.target_str = ""
        self.doing_str = ""
        self.print = print_func
        self.call = call_func
        self.unlink = True
        if target_str != "":
            self.do(target_str)
    def missing(self) -> bool:
        if Path(self.target_str).exists():
            self.print(F"NOTE: {self.target_str} existed")
            target_bool = False
        else:
            if Path(self.doing_str).exists():
                if self.unlink:
                    Path(self.doing_str).unlink()
                    self.print(F"NOTE: {self.doing_str} removed")
                    target_bool = True
                else:
                    self.print(F"NOTE: {self.doing_str} keep and skip")
                    target_bool = False
            else:
                target_bool = True
        return target_bool
    def do(self,target_str:str) -> None:
        self.target_str = target_str
        self.doing_str = "{}/{}".format(Path(target_str).parent,"doing-"+Path(target_str).name)
    def done(self) -> None:
        self.print(F"NOTE: {self.doing_str} done")
        self.call(F"mv -v {self.doing_str} {self.target_str}")
#
class paginator:
    def __init__(self,input_list:list,split_num:int=5) -> None:
        self.parent_list = input_list
        self.parent_count = len(input_list)
        self.split_number = split_num
        self.split_left = self.parent_count%self.split_number
        self.split_ceil = math.ceil(self.parent_count/self.split_number)
        self.output_dict = dict()
    def count(self) -> dict:
        for each_num in range(self.split_ceil):
            group_bool = ((each_num == self.split_ceil - 1) and (self.split_left > 0))
            group_size = self.split_left if group_bool else self.split_number
            self.start_num = each_num*self.split_number
            self.end_num = (each_num*self.split_number)+group_size
            self.output_dict[each_num] = [self.parent_list[pos_num] for pos_num in range(self.start_num,self.end_num)]
        return self.output_dict
#
def dict_sort(inputDict:dict,reverse_bool:bool=False) -> dict:
    if type(inputDict) == type(dict()):
        outputDict = {}
        outputDict.update({n:inputDict[n] for n in sorted(list(inputDict.keys()),reverse=reverse_bool)})
        for x,y in outputDict.items():
            if type(y) == type(dict()):
                outputDict[x] = dict_sort(y)
        return outputDict
    else:
        return inputDict
