# dtTimeFrame

dtTimeFrame is a module that pack **time track functions** and **subprocess call functions** into one single class.

- Homepage: <https://github.com/SotongDJ/dtTimeFrame>

## Install dtTimeFrame

```bash
pip install dttimeframe
```

## Example codes

### tag()

```python
from dtTimeFrame.timeFrame import tag # type: ignore

# Initiation
Tool = tag()
Tool.log.name = "log.txt" # filename of the log file, store stdout info
Tool.error.name = "err.txt" # filename of the err file, store stderr info
Tool.extra.name = "log.json" # filename of the extra command record, store time stamp, commands and others info

# start logging and write header into log/err files
Tool.start()

# > your code insert here < 

# print time stamp with personalized msg
Tool.timeStamp("PREVIEW: show something you want to info")

# command runner, base on subprocess.call()
phrase_str = F"echo this command line"
Tool.runCommand(phrase_str)

# command runner with specific output file
phrase_str = F"echo this command line into specific output file: test.txt"
Tool.runCommand(phrase_str,export_file="test.txt")

# > your code insert here < 

# end logging and write footer into log/err files 
Tool.stop()
```

### detector()

```python
from dtTimeFrame.timeFrame import detector # type: ignore

file_be_process_handle = detector(print_func=print,call_func=print)
# "file_be_process_handle = detector(print_func=Tool.timeStamp,call_func=Tool.runCommand)"
# combine use with tag() 
file_be_process_handle.do(target_str="target.txt")
if file_be_process_handle.missing(): # if target.txt missing?
    with open(file_be_process_handle.doing_str,"w") as target_handle: # doing-target.txt
        target_handle.write("Hello world\n")
    file_be_process_handle.done() # rename doing-target.txt as target.txt

print(open(file_be_process_handle.target_str).read())
```
