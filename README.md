# Warthunder Replay Parser
Warthunder replay files unfortunately do not seem to contain any easily readable information (like WOT, which includes some JSON). This a very, very basic attempt at parsing Warthunder replay files (.wrpl)

!!! This is still very much WIP and it will not work consistently !!!

## What can it do?
So far, it can only the planes involved in a match.

## How to use it?
You need to have python installed. Use it as follows:
```
python wtparser.py <directory where replay files are stored>
```
This assumes that the replay files in that directory belong to one battle only, and are named like `0000.wrpl`, `0001.wrpl` etc. This is the naming scheme used for replays downloaded from https://warthunder.com/en/tournament/replay/

If a directory is not given, it will use the current directory.