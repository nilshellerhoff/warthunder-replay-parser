# Warthunder Replay Parser
Warthunder replay files unfortunately do not seem to contain any easily readable information (like WOT, which includes some JSON). This a very, very basic attempt at parsing Warthunder replay files (.wrpl). There is [wt-tools](https://github.com/klensy/wt-tools/), which though does not seem to work with (multipart) server replays.

## How to use it?

There are three scripts available:

### replays_scraper.py
> :warning: **Use at your own risk, scraping (protected) webpages might be against the TOS/law in certain countries**

This script can be used to scrape replays from the https://warthunder.com/en/tournament/replay/ page. Invoke it like this:
```
python replays_scraper.py <num_pages>
```
where `<num_pages>` is the number of pages to scrape (typically there are 25 replays per page). It will print a JSON object with all the found replays.

Since the page is login protected, this script expects a `auth_cookie.json` file with the cookies for the login:

auth_cookie.json:
```json
{
	"identity_sid" : "..."
}
```
where ... is the value of the `identity_sid` cookie (which you can get by logging in to warthunder.com and reading the cookies in your browser).

### download_replay.py
Download a replay from https://warthunder.com/en/tournament/replay/.

```
python download_replay.py <replay_id>
```
where `<replay_id>` is the replay ID (64-bit, either in decimal or hexadecimal notation). This will store the replay files in a folder named named after the replay ID in hex notation.

### parse_replay.py
Parse a replay in a folder

```
python parse_replay.py <replay_folder>
```

It expects the replay files to be named 0000.wrpl, 0001.wrpl, etc. If a `<replay_folder>` is not given, it will use the current directory.

The output will be in json form:
```
parsing replay in /path/to/replay/005569aa001501ca
parsing /path/to/replay/005569aa001501ca/0000.wrpl
parsing /path/to/replay/005569aa001501ca/0001.wrpl
parsing /path/to/replay/005569aa001501ca/0002.wrpl
parsing /path/to/replay/005569aa001501ca/0003.wrpl
parsing /path/to/replay/005569aa001501ca/0004.wrpl
parsing /path/to/replay/005569aa001501ca/0005.wrpl
parsing /path/to/replay/005569aa001501ca/0006.wrpl
parsing /path/to/replay/005569aa001501ca/0007.wrpl
parsing /path/to/replay/005569aa001501ca/0008.wrpl
parsing /path/to/replay/005569aa001501ca/0009.wrpl

{
    "level": "levels/avg_normandy.bin",
    "mission_file": "gamedata/missions/cta/tanks/normandy/normandy_dom.blk",
    "mission_name": "normandy_Dom",
    "time_of_day": "day",
    "weather": "hazy",
    "time_of_battle_ts": 1641217514,
    "time_of_battle": "2022-01-03 14:45:14",
    "num_players": 21,
    "players": [
        {
            "player_id": 34,
            "vehicles": [
                "us_m1a1_abrams",
                "us_m1a1_hc_abrams"
            ]
        },
        {
            "player_id": 35,
            "vehicles": [
                "us_m1_ip_abrams",
                "us_hstv_l"
            ]
        },
        ...
    ]
}
```

## Use as module
You can also use the scripts as a modules
```python
import replays_scraper
import download_replay
import parse_replay

# set the cookies
cookies = { "identity_sid" : "secret_key" }

# download the html
pages = replays_scraper.download_pages(1, cookies)

# scrape replay data from html
replays = []
for page in pages:
	replays += replays_scraper.parse_page(page)

# download the files of the last replay
download_replay.downloadReplay(replays[-1]["id"])

# get the hexadecimal id (= folder name)
replay_id_hex = download_replay._get_hex_id(replays[-1]["id"])

# parse the replay
print(parse_replay.parse_replay(replay_id_hex))
```
