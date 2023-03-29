# dtTimeFrame

dtTimeFrame is a module that pack **time track functions** and **subprocess call functions** into one single class.

- Homepage: <https://github.com/SotongDJ/dtTimeFrame>

## Install dtTimeFrame

```bash
pip install dttimeframe
```

## Example codes

```python
# import submodule
from dtTimeFrame import timeFrame as timeframe # type: ignore

# Initiation
Tool = timeframe.tag()
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
