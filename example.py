#!/usr/bin/env python3
import libCommand, argparse, datetime
parser = argparse.ArgumentParser(description="run some tool")
parser.add_argument("-s", "--script", help="export commands as script",action="store_true")
parser.add_argument("-t", "--target", help="give target (optional)",type=str)
args = parser.parse_args()
if args.target:
    target_str = args.target
else:
    target_str = "something"
Tool = libCommand.timer()
# prefix-20210201.log
# prefix-20210201-error.log
Tool.logFilenameStr = 'prefix-{}'.format(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8),name="UTC+8")).strftime("%Y%m%d"))
Tool.folderStr = "log/"
# default testingBool is False
if args.script:
    Tool.testingBool = True
Tool.startLog()

Tool.phraseStr = "NOTE: {} not EXIST".format(target_str)
Tool.printTimeStamp()

Tool.phraseStr = F"echo {target_str}"
Tool.runCommand()
Tool.phraseStr = F"echo {target_str} into example.txt" # without "
Tool.runCommand(targetStr="example.txt")
Tool.testingBool = True
Tool.phraseStr = "echo the following commands into example.sh" # without "
Tool.runCommand()
Tool.phraseStr = F"echo {target_str} into example.txt" # without "
Tool.runCommand(targetStr="example.txt")

Tool.stopLog()
