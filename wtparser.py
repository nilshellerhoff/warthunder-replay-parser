import os
import sys
import re

def parse_replays(path):
    '''
    Parse all replay files in a directory and return a list of listed players
    '''

    files =  _get_files(path)

    if len(files) == 0:
        print("No replays found in {}".format(os.path.abspath(path)))
        sys.exit()

    players = []

    for file in files:
        print("parsing {}".format(file))
        players += _parse_replay(file)

    print("")

    # filter duplicates
    return list(set(players))

def _get_files(path):
    '''
    Get the filenames of all relevant files.
    '''

    # get the absolute path
    abspath = os.path.abspath(path)

    dirfiles = os.listdir(abspath)

    # Currently we are only looking for files like 0000.wrpl, 0001.wrpl ...
    # (this is how https://warthunder.com/en/tournament/replay/ names replays)
    files_match = ".*\d\d\d\d.wrpl$"

    return [os.path.join(abspath, f) for f in dirfiles if re.search(files_match, f)]

def _parse_replay(path):
    '''
    Parse a single replay file and return found players in format (plane_name, player_id) (not sure about player_id)
    '''

    with open(path, 'rb') as f:
        repl = f.read()

    # Ignored strings (not plane names)
    ignored_str = ["levels"]

    # allowed letters for plane names
    letters = list(b"abcdefghijklmnopqrstuvwxyz1234567890-_")

    # This is the magic binary sequence which preceeds each plane name 
    magic_sequence = "01 20 01"
    sequence = [int(b, 16) for b in magic_sequence.split(" ")]

    players = []

    seq_mark = 0

    for i,c in enumerate(repl):
        # if sequence lenght has been reached, we found something interesting
        if seq_mark > len(sequence) - 1:
            seq_mark = 0

            # check if following 5 letters are ascii, if they are, assume plane
            if all(r in letters for r in repl[i+1:i+5]):
                plane = ""
                idx = 1
                while repl[i+idx] in letters:
                    plane += chr(repl[i+idx])
                    idx += 1
                
                # player id is two byte before sequnece? -> does not seem to be correct
                pid = "{:02x}{:02x}".format(repl[i-len(sequence)-1], repl[i-len(sequence)-2])
                #pid = str(repl[i-len(sequence)-1]) + str(repl[i-len(sequence)-2]) 

                # ignored special cases
                if plane in ignored_str:
                    continue
                
                players.append((plane, pid))

        # if we found something in the sequence, increase counter by one
        if c == sequence[seq_mark]:
            seq_mark += 1
    
    return players

if __name__ == "__main__":
    
    # if we have an argument, use this as path, otherwise use current folder
    try:
        path = os.path.abspath(sys.argv[1])
    except:
        path = os.getcwd()
    
    players = parse_replays(path)

    # sort players by plane name
    players = sorted(players)

    print("Found {} players".format(len(players)))
    print("")

    print("PID\tplane")
    for p in players:
        print("{}\t{}".format(p[1],p[0]))