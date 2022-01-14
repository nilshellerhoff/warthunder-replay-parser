import requests
import sys
import os
from multiprocessing.pool import ThreadPool


# maximum number of files to download at the same time
MAX_CONCURRENT_DOWNLOADS = 5

def download_replay(replay_id, store_path=os.getcwd()):
    """
    download a replay from the replay server given it's id
    """

    # get the hex id in correct format
    replay_id = _get_hex_id(replay_id)

    # create the folder
    os.mkdir(replay_id)

    index = 0
    fileLink = 'http://wt-game-replays.warthunder.com/{}/{:04d}.wrpl'

    while r := requests.get(fileLink.format(replay_id, index)):
        print("downloading part %d" % (index + 1))
        if r.status_code == 404:
            break

        path = os.path.join(f"{store_path}", f"{replay_id}", f"{index:04d}.wrpl")
        with open(path, 'wb') as f:
            f.write(r.content)

        index += 1

    return index


def _get_hex_id(replay_id):
    """
    from a replay id (64-bit int) get the appropriate hex notation (zero-padded 16 char int) regardless of decimal or hex input
    """

    replay_id = str(replay_id)

    # replay_id is 64bit int (can be decimal or hex)
    # check length to find out, hex should be 16 chars (64 bit)
    if len(replay_id) == 16:
        replay_id = int(replay_id, 16)
    else:
        replay_id = int(replay_id)

    # convert to hex
    replay_id_hex = "{:016x}".format(replay_id)

    return replay_id_hex


def main():
    try:
        replay_id = sys.argv[1]
    except:
        print("Usage: download_replay.py <replay_id>")
        return

    num_parts = download_replay(replay_id)

    replay_id_hex = _get_hex_id(replay_id)

    print(f"downloaded {num_parts}-part replay to {replay_id_hex}")

if __name__ == "__main__":
    main()