#!/usr/bin/env python3
import libTimeTag, argparse, datetime
parser = argparse.ArgumentParser(description="run some tool")
parser.add_argument("-s", "--script", help="export commands as script",action="store_true")
parser.add_argument("-t", "--target_str", help="give target (optional)",type=str)
parser.add_argument("-f", "--target_file", help="give target (optional)",type=str)
args = parser.parse_args()
if args.target_str:
    target_str = args.target_str
else:
    target_str = "something"
if args.target_file:
    target_file = args.target_file
else:
    target_file = "example.txt"
Tool = libTimeTag.tag()
# prefix-20210201.log
# prefix-20210201-error.log
Tool.log_name_str = 'prefix-{}'.format(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8),name="UTC+8")).strftime("%Y%m%d"))
Tool.log_path_str = "log/"
# default testingBool is False
if args.script:
    Tool.script_export_bool = True
Tool.startLog()
Tool.phrase_str = "NOTE: {} not EXIST".format(target_str)
Tool.printTimeStamp()

Tool.phrase_str = F"echo {target_str}"
Tool.runCommand()
Tool.phrase_str = F"echo {target_str} into {target_file}"
Tool.runCommand(target_str=target_file)
Tool.script_export_bool = True
Tool.phrase_str = "echo the following commands into example.sh"
Tool.runCommand()
Tool.phrase_str = F"echo {target_str} into example.sh but not {target_file}"
Tool.runCommand(target_str=target_file)
Tool.script_export_bool = False
Tool.phrase_str = F"echo {target_str} into {target_file} but not example.sh"
Tool.runCommand(target_str=target_file)

Tool.stopLog()
