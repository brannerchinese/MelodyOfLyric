#! /usr/bin/env python
# edit_midi.py
# David Prager Branner
# 20140904

import sys
if sys.version_info.major < 3:
    print('Python 3 is required. You are using {}.{}.'.
            format(sys.version_info.major, sys.version_info.minor))
    sys.exit()
import os
import heapq as H

def main(filename='output.csv'):
    with open(os.path.join('../midi', filename), 'r') as f:
        content = f.read()
    # Extract only lines containing "Note_".
    content = [tuple(item.split(', ')[1:]) 
            for item in content.split('\n') 
            if 'Note_' in item]
    received_events = [(item[0], item[1], item[3], item[4]) for item in content]
    print(received_events) # debug
    # Get set of times and make heapq "times" as well as "received_events".
    times = list(set([int(i[0]) for i in content]))
    times.sort()
    print(times) # debug
    # Create empty list of "final_melody", variable "current" (current main
    # note).
    current_events = []
    final_melody = []
    current_note = None
    # Step through times
    for time in times:
        print(time)
        # If an off-item, remove from "current_events".
        if time[1] == 'Note_off_c':
            current_events.remove(time)
        # If an on-item, add to "current_events".
        if time[1] == 'Note_on_c':
            H.heappush(current_events, (time))
        # If highest-velocity item in "events" is not "current":
        largest = H.nlargest(1, current_events, key=lambda i: i[1])[0]
        if largest != current:
            # add "off" event for "current" to final_melody
            final_melody.append()
            # assign new highest-velocity value to "current"
            current = largest
            # add "on" event for new "current"
            final_melody.append()

# What if two simultaneous events are equally loud?

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'output.csv'
    else:
        filename = sys.argv[1]
    main(filename)
