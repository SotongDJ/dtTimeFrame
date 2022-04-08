#!/usr/bin/env python3
import libTimeTag, argparse, datetime
parser = argparse.ArgumentParser(description="run some tool")
parser.add_argument("-s", "--script", help="give command sh script (optional)",type=str)
parser.add_argument("-n", "--name", help="give name string(optional)",type=str)
parser.add_argument("-o", "--output", help="give output name (optional)",type=str)
args = parser.parse_args()
if args.name:
    name = args.name
else:
    name = "something"
if args.output:
    output = args.output
else:
    output = "example-stdout.txt"
Tool = libTimeTag.tag()
Tool.log.name = "example-log.txt"
Tool.error.name = "example-error.txt"

Tool.start()

Tool.timeStamp("PREVIEW: {} not EXIST".format(name))

Tool.runCommand(F"echo {name}")

Tool.runCommand(F"echo {name} into {output}",export_file=output)

Tool.script.name = "example-shell.sh"
phrase_str = F"echo the following commands into {Tool.script.name}"
Tool.runCommand(phrase_str)

phrase_str = F"echo {name} into {Tool.script.name} but not {output}"
Tool.runCommand(phrase_str,export_file=output)

Tool.script.name = ""
Tool.runCommand("echo Turn off shell script export",export_file=output)

phrase_str = F"echo {name} into {output} but not example.sh"
Tool.runCommand(phrase_str,export_file=output)

Tool.stop()
