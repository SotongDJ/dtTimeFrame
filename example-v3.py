#!/usr/bin/env python3
import libTimeTag, argparse, datetime
parser = argparse.ArgumentParser(description="run some tool")
parser.add_argument("-n", "--name", help="give name string(optional)",type=str,default="something")
parser.add_argument("-o", "--output", help="give output log name (optional)",type=str,default="example-v3-log.txt")
parser.add_argument("-e", "--error", help="give error log name (optional)",type=str,default="example-v3-error.txt")
parser.add_argument("-s", "--script", help="give shell script name(optional)",type=str,default="example-v3-shell.sh")
args = parser.parse_args()
Tool = libTimeTag.tag()
Tool.log.name = args.output
Tool.error.name = args.error

Tool.start()

Tool.timeStamp("PREVIEW: show {}".format(args.name))

Tool.runCommand(F"echo {args.name}")

Tool.runCommand(F"echo {args.name} into {args.output}",export_file=args.output)

Tool.script.name = args.script
phrase_str = F"echo the following commands into {args.script}"
Tool.runCommand(phrase_str)

phrase_str = F"echo {args.name} into {args.script} but not {args.output}"
Tool.runCommand(phrase_str,export_file=args.output)

Tool.script.name = ""
Tool.runCommand("echo Turn off shell script export",export_file=args.output)

phrase_str = F"echo {args.name} into {args.output} but not example.sh"
Tool.runCommand(phrase_str,export_file=args.output)

Tool.stop()
