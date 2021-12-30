import requests
import sys
import os
from multiprocessing.pool import ThreadPool

# maximum number of files to download at the same time
MAX_CONCURRENT_DOWNLOADS = 5

def downloadReplay(replay_id):
    # create the folder
    os.mkdir(replay_id)

    index = 0
    fileLink = 'http://wt-game-replays.warthunder.com/{}/{:04d}.wrpl'

    while r := requests.get(fileLink.format(replay_id, index)):
        print("downloading part %d" % (index + 1))
        if r.status_code == 404:
            break

        with open(f'{replay_id}/{index:04d}.wrpl', 'wb') as f:
            f.write(r.content)

        index += 1


def main():
    try:
        replay_id = sys.argv[1]
    except:
        print("Usage: download_replay.py <replay_id>")
        return

    # replay_id is 64bit int (can be decimal or hex)
    # check length to find out, hex should be 16 chars (64 bit)
    if len(replay_id) == 16:
        replay_id = int(replay_id, 16)
    else:
        replay_id = int(replay_id)

    # convert to hex
    replay_id_hex = "{:016x}".format(replay_id)

    downloadReplay(replay_id_hex)

if __name__ == "__main__":
    main()