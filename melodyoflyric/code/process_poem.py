#! /usr/bin/env python
# process_poem.py
# David Prager Branner
# 20141026

import os
import read_xml as R
import utils as U

def get_syllables(filename=os.path.join(
        '..', 'data', 'sheu_ityng_pyiparshyng_20141031_edited_thru_meas_191.xml')):
    """Get all text syllables of poem, their tones, and their durations."""
    syllables, divisions = R.main(filename)
    syllables = [(
            syllable[0],
            U.identify_tone(syllable[0]),
            U.sum_syllable_durations(syllable))
                for syllable in syllables if syllable[0]
            ]
    return syllables, divisions

def avg_duration_by_place(syllables, divisions, places=[7]):
    place_counts = [[0, 0] for i in range(places[0])] # what about |place| > 1?
    for i, syllable in enumerate(syllables):
        place_counts[i % places[0]][0] += 1
        place_counts[i % places[0]][1] += syllable[2]
    place_counts = [[i[0],
               i[1],
               round(i[1] / i[0], 1)]
            for i in place_counts
            if i[0] != 0]
    return place_counts

def avg_duration_by_tone(syllables, divisions):
    tone_counts = {'yīnpíng': [0, 0],
              'yángpíng': [0, 0],
              'yīnshǎng': [0, 0],
              'yīnqù': [0, 0],
              'yángqù': [0, 0],
              'yīnrù': [0, 0],
              'yángrù': [0, 0]}
    for syllable in syllables:
        tone_counts[syllable[1][0]][0] += 1
        tone_counts[syllable[1][0]][1] += syllable[2]
    tone_counts = {i: [tone_counts[i][0],
                  tone_counts[i][1],
                  round(tone_counts[i][1] / tone_counts[i][0], 1)]
            for i in tone_counts
            if tone_counts[i][0] != 0}
    return tone_counts

def avg_duration_by_pyngtzeh(syllables, divisions):
    pyngtzeh_counts = {'○': [0, 0],
              '●': [0, 0]}
    for syllable in syllables:
        pyngtzeh_counts[syllable[1][1]][0] += 1
        pyngtzeh_counts[syllable[1][1]][1] += syllable[2]
    pyngtzeh_counts = {i: [pyngtzeh_counts[i][0],
                  pyngtzeh_counts[i][1],
                  round(pyngtzeh_counts[i][1] / pyngtzeh_counts[i][0], 1)]
            for i in pyngtzeh_counts
            if pyngtzeh_counts[i][0] != 0}
    return pyngtzeh_counts

def avg_duration_by_place_and_tone(syllables, divisions, places=[7]):
    tone_place_counts = {
            'yīnpíng': [[0, 0] for i in range(places[0])],
            'yángpíng': [[0, 0] for i in range(places[0])],
            'yīnshǎng': [[0, 0] for i in range(places[0])],
            'yīnqù': [[0, 0] for i in range(places[0])],
            'yángqù': [[0, 0] for i in range(places[0])],
            'yīnrù': [[0, 0] for i in range(places[0])],
            'yángrù': [[0, 0] for i in range(places[0])]
            }
    for i, syllable in enumerate(syllables):
        tone_place_counts[syllable[1][0]][i % places[0]][0] += 1
        tone_place_counts[syllable[1][0]][i % places[0]][1] += syllable[2]
    tone_place_counts = {
            tone: [
                [count, duration, round(duration / count, 1)]
                for [count, duration] in tone_place_counts[tone]
                if count != 0
                ]
            for tone in tone_place_counts
            }
    return tone_place_counts

def avg_duration_by_place_and_pyngtzeh(syllables, divisions, places=[7]):
    pyngtzeh_place_counts = {
            '○': [[0, 0] for i in range(places[0])],
            '●': [[0, 0] for i in range(places[0])]}
    for i, syllable in enumerate(syllables):
        pyngtzeh_place_counts[syllable[1][1]][i % places[0]][0] += 1
        pyngtzeh_place_counts[syllable[1][1]][i % places[0]][1] += syllable[2]
    pyngtzeh_place_counts = {
            tone: [
                [count, duration, round(duration / count, 1)]
                for [count, duration] in pyngtzeh_place_counts[tone]
                if count != 0
                ]
            for tone in pyngtzeh_place_counts
            }
    return pyngtzeh_place_counts

def count_melodies(shortest, longest=0, filename=os.path.join(
            '..', 'data', 
            '''sheu_ityng_pyiparshyng_20141031_edited_thru_meas_191.xml''')):
    """Report any sequences of intervals that appear more than once."""
    # QQQ not yet in test suite!
    # QQQ we would like to see the lyrics in question here, not note- indices.
    xml_notes, divisions = R.get_notes(filename)
    melody = U.get_melody(xml_notes, divisions)
    intervals = U.get_intervals(melody)
    substrings = U.find_all_substrings(intervals, shortest, longest)
    interval_count = {}
    for substring in substrings:
        if substring[1] in interval_count:
            interval_count[substring[1]].append(substring[0])
        else:
            interval_count[substring[1]] = [substring[0]]
    interval_count = {key: interval_count[key] for key in interval_count
            if len(interval_count[key]) > 1}
    return interval_count
