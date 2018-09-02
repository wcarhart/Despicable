# Despicable
*Lightweight multithreading framework for command line tasks*

`Despicable` acts as a parallelizer for shell commands. The tool allows you to run multiple shell commands in parallel.

For example, perhaps you'd like to copy a very large file while also compressing some other files. This can easily be accomplished with `Despicable`.

## Architecture Explained

## Usage
`Despicable` is a Python CLI. You can either list commands via the command line (note that commands *MUST* be wrapped in quotes):
```
python despicable.py -c "cmd0" "cmd1" "cmd2"
```
or via a text file:
```
python despicable.py -f command_list.txt
```
or both:
```
python despicable.py -c "cmd0" "cmd1" -f command_list.txt
```
*Note that the default command file is called the `Despicablefile`. If you put your commands in the `Despicablefile`, you do not need to specify the `-f` flag as `Despicable` will look in `Despicablefile` for commands by default.*

**Here is the full list of options:**
```
usage: despicable.py [-h] [-t THREAD_MAX] [-c COMMANDS [COMMANDS ...]]
                     [-f COMMAND_FILE] [-m MESSAGE]
                     [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [--log-file LOG_FILE] [-o]

Lightweight multithreading framework for command line tasks

optional arguments:
  -h, --help            show this help message and exit
  -t THREAD_MAX, --thread-max THREAD_MAX
                        maximum number of threads (default: 8)
  -c COMMANDS [COMMANDS ...], --commands COMMANDS [COMMANDS ...]
                        a command to be parallelized (must be wrapped in
                        double quotes) (default: None)
  -f COMMAND_FILE, --command-file COMMAND_FILE
                        name of the file that contains commands to be
                        parallelized (default: Despicablefile)
  -m MESSAGE, --message MESSAGE
                        The message to be displayed during concurrent
                        execution (default: Processing)
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The level at which to log information during execution
                        (default: INFO)
  --log-file LOG_FILE   The file to log info to during execution (default:
                        despicable_logs.txt)
  -o, --omit-logs       if included, information will not be logged (default:
                        False)
```
You can also use the `-m` or `--message` option to customize the status message while tasks are being executed.

## Examples
For demonstration purposes, suppose you would like to run the following commands in parallel:
```
cp /source/largefile.csv /destination/
bzip2 -z data.txt
scp big_file.json username@remotehost.edu:/some/remote/directory
qbittorrent-nox
```
You could run this either by (note that commands *MUST* be wrapped in quotes):
```
python despicable.py -c "cp /source/largefile.csv /destination/" "bzip2 -z data.txt" "scp big_file.json username@remotehost.edu:/some/remote/directory" "qbittorrent-nox"
```
```
python despicable.py -f command_list.txt
```
Where `command_list.txt` contains:
```
cp /source/largefile.csv /destination/
bzip2 -z data.txt
scp big_file.json username@remotehost.edu:/some/remote/directory
qbittorrent-nox
```
**Example output:**
```
$ python despicable.py -f command_list.txt
[>>>>>>>>>>>>>>>               ] 50% (Processing)
\ 2 tasks remaining
```
**Try it yourself:** put the following commands in `Despicablefile`:
```
sleep 10
sleep 5
sleep 1
sleep 15
```
and then run `python despicable.py` to see `Despicable` work!

## Logging
Logs from `Despicable` will default to `despicable_logs.txt`, but the log file can be changed with the `--log-file` option. You can also specify the log level with the `--log-level` option. Logs will include the communication from each `Minion` thread, indicating the `STDOUT` and `STDERR` for each spawned `Minion`.

## Comments
`Despicable` attempts to be lightweight and portable, meaning that it can be used with any tool or command that can be written as a single command in `BASH` or similar shells. Please log and issue or fork and open a PR if you have any questions or concerns.
