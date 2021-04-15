#!/usr/bin/env python3
import libCommand, argparse, datetime
parser = argparse.ArgumentParser(description="run some tool")
parser.add_argument("-s", "--script", help="export commands as script",action="store_true")
args = parser.parse_args()


Tool = libCommand.timer()
# prefix-20210201.log
# prefix-20210201-error.log
Tool.logFilenameStr = 'prefix-{}'.format(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8),name="UTC+8")).strftime("%Y%m%d"))
Tool.folderStr = "log/"
Tool.testingBool = False
if args.script:
    Tool.testingBool = True
Tool.startLog()

Tool.phraseStr = "NOTE: {} not EXIST".format("something")
Tool.printTimeStamp()

Tool.phraseStr = "echo something"
Tool.runCommand()
Tool.phraseStr = "echo something into example.txt" # without "
Tool.runCommand(targetStr="example.txt")
Tool.testingBool = True
Tool.phraseStr = "echo this command into example.sh" # without "
Tool.runCommand()

Tool.stopLog()
