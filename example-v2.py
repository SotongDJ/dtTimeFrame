#!/usr/bin/env python3
# python3 example-v2.py -o example-v2
import libCommand, argparse, datetime
parser = argparse.ArgumentParser(description="run some tool")
parser.add_argument("-s", "--script", help="export commands as script",action="store_true")
parser.add_argument("-n", "--name", help="give name string(optional)",type=str)
parser.add_argument("-o", "--output", help="give output name (optional, without extension)",type=str)
args = parser.parse_args()
if args.name:
    target_str = args.name
else:
    target_str = "something"
if args.output:
    output_str = args.output
else:
    output_str = 'run-{}'.format(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8),name="UTC+8")).strftime("%Y%m%d"))
Tool = libCommand.timer()
Tool.logFilenameStr = output_str
Tool.folderStr = "log/"
# default testingBool is False
if args.script:
    Tool.testingBool = True
Tool.startLog()

Tool.phraseStr = "PREVIEW: {}".format(target_str)
Tool.printTimeStamp()

Tool.phraseStr = F"echo {target_str}"
Tool.runCommand()

Tool.phraseStr = F"echo {target_str} into {Tool.folderStr}{output_str}-stdout.txt" # without "
Tool.runCommand(targetStr=F"{Tool.folderStr}{output_str}-stdout.txt")

Tool.testingBool = True
Tool.phraseStr = "echo the following commands into shell script" # without "
Tool.runCommand()

Tool.phraseStr = F"echo {target_str} into {Tool.folderStr}{output_str}-stdout.txt" # without "
Tool.runCommand(targetStr=F"{Tool.folderStr}{output_str}-stdout.txt")

Tool.stopLog()
