#! /usr/bin/env python
# edit_midi.py
# David Prager Branner
# 20140904

import sys
if sys.version_info.major < 2:
    print('Python 3 is required. You are using {}.{}.'.
            format(sys.version_info.major, sys.version_info.minor))
    sys.exit()
import os
import heapq

def main(filename):
    with open(os.path.join('../midi', filename), 'r') as f:
        content = f.open()
    # Get set of times and make heapq "times" as well as midi events "events".
    # Create empty list of "notes", variable "current": (note, velocity).
    # Step through times
        # If an off-item, remove from "events".
        # If an on-item, add to "events".
        # If highest-velocity item in "events" is not "current":
            # add "off" event for "current"
            # assign new highest-velocity value to "current"
            # add "on" event for new "current"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'output.csv'
    else:
        filename = sys.argv[1]
    main(filename)
