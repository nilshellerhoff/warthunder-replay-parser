# Warthunder Replay Parser
Warthunder replay files unfortunately do not seem to contain any easily readable information (like WOT, which includes some JSON). This a very, very basic attempt at parsing Warthunder replay files (.wrpl). There is [wt-tools](https://github.com/klensy/wt-tools/), which though does not seem to work with (multipart) server replays.

## How to use it?

There are three scripts available:

### replays_scraper.py
**!!!Use at your own risk, scraping (protected) webpages might be against the TOS/law in certain countries!!!**

This script can be used to scrape replays from the https://warthunder.com/en/tournament/replay/ page. Invoke it like this:
```
python replays_scraper.py <num_pages>
```
where `<num_pages>` is the number of pages to scrape (typically there are 25 replays per page). It will print a JSON object with all the found replays.

Since the page is login protected, this script expects a `auth_cookie.json` file with the cookies for the login:

cookies.json:
```json
{
	"identity_sid" : "..."
}
```
where ... is the value of the `identity_sid` cookie (which you can get by logging in to warthunder.com and reading the cookies in your browser).

### download_replay.py
Download a replay from the [Warthunder replay server](https://warthunder.com/en/tournament/replay/).

```
python download_replay.py <replay_id>
```
where `<replay_id>` is the replay ID (64-bit, either in decimal or hexadecimal notation). This will store the replay files in a folder named named after the replay ID in hex notation.

### parse_replay.py
Parse a replay in a folder

```
python wtparser.py <replay_folder>
```

It expects the replay files to be named 0000.wrpl, 0001.wrpl, etc. If a `<replay_folder>` is not given, it will use the current directory.

The output will be in json form:
```
parsing replay in /path/to/replay
parsing /path/to/replay/0000.wrpl
parsing /path/to/replay/0001.wrpl
parsing /path/to/replay/0002.wrpl
parsing /path/to/replay/0003.wrpl
parsing /path/to/replay/0004.wrpl
parsing /path/to/replay/0005.wrpl
parsing /path/to/replay/0006.wrpl
parsing /path/to/replay/0007.wrpl
parsing /path/to/replay/0008.wrpl
parsing /path/to/replay/0009.wrpl
parsing /path/to/replay/0010.wrpl
parsing /path/to/replay/0011.wrpl
parsing /path/to/replay/0012.wrpl
parsing /path/to/replay/0013.wrpl
parsing /path/to/replay/0014.wrpl
parsing /path/to/replay/0015.wrpl
parsing /path/to/replay/0016.wrpl
parsing /path/to/replay/0017.wrpl

{
    "level": "levels/sicily.bin",
    "mission_file": "gamedata/missions/cta/planes/historical/bfd/sicily/sicily_bfd_norespawn.blk",
    "mission_name": "sicily_BfD_norespawn",
    "time_of_day": "day",
    "weather": "cloudy",
    "time_of_battle_ts": 1640607893,
    "time_of_battle": "2021-12-27 13:24:53",
    "players": [
        {
            "player_id": 11,
            "vehicles": [
                "f-86a-5"
            ]
        },
        {
            "player_id": 12,
            "vehicles": [
                "f-84f"
            ]
        },
        ...
    ]
}
```

You can also use the script as a module:
```python
import parse_replay
replay_data = parse_replay.parse_replay(replay_folder)
```
