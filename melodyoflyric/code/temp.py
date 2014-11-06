import read_xml as R
import utils as U
import os

def count_melodies(shortest, longest=0, filename=os.path.join(
            '..', 'data', 'sheu_ityng_pyiparshyng_20141025.xml')):
    xml_notes, divisions = R.get_notes(filename)
    melody = U.get_melody(xml_notes, divisions)
    intervals = U.get_intervals(melody)
    substrings = U.find_all_substrings(intervals, shortest, longest)
    interval_count = {}
    for substring in T.substrings:
        if substring in interval_count:
            interval_count[substring[1]] += 1
        else:
            interval_count[substring[1]] = 1
    return interval_count
