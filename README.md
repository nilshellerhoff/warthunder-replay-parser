# Warthunder Replay Parser
Warthunder replay files unfortunately do not seem to contain any easily readable information (like WOT, which includes some JSON). This a very, very basic attempt at parsing Warthunder replay files (.wrpl). There is [wt-tools](https://github.com/klensy/wt-tools/), which though does not seem to work with server replays.

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

## WRPL format
- 0x0008: Mapfile (e.g. `levels/ruhr.bin`)
- 0x02E0: File number of replay (0x00 for `0000.wrpl`, 0x01 for `0001.wrpl` etc)
- 0x02D8 - 0x000002DB: Battle ID?
- every occurence of a plane name is prefixed by 0x012001