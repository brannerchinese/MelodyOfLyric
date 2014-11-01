# 20141031

import read_xml as R
import utils as U
from collections import Counter

"""Generate melisma data."""

def main():
    # Get list of syllables
    syllables, divisions = R.main()
    
    # If a syllable is melismatic:   len(syllable[2]) > 1
    # then add its tone category:    (U.identify_tone(syllable[0])[0]
    # and "melody" (pitch sequence): [attr['pitch_data'] for attr in syllable[2]]
    # as a 2-tuple to a list.
    melismatic = [
            [U.identify_tone(syllable[0])[0], 
             [attr['pitch_data'] for attr in syllable[2]]]
                    for syllable in syllables
                    if len(syllable[2]) > 1
            ]
    
    # Replace the melody with a sequence of intervals.
    # Then count +/- of first item so we know which direction the melismas move in.
    # The first of these is the most interesting.
    melisma_count = {}
    melismas = [(tone, U.get_intervals(melody)) for tone, melody in melismatic]
    for item in melismas:
        if item[0] not in melisma_count:
            melisma_count[item[0]] = [0, 0, 0]
        if item[1][0] < 0:
            melisma_count[item[0]][0] += 1
        elif item[1][0] > 0:
            melisma_count[item[0]][2] += 1
        else:
            melisma_count[item[0]][1] += 1
    print('Direction of start of each melisma:')
    for tone in U.seven_tones:
        print(tone, melisma_count[tone])


    # Should we eliminate cases of [0] here?
    
    # How do we determine whether a new syllable starts on a pitch higher, lower, or the same as the previous syllable?
    
    # Count non-melismatic examples of each tone. 
    # Use tuples so that we can then use Counter.
    nonmelismatic = [
            (U.identify_tone(syllable[0])[0], 
             tuple([attr['pitch_data'] for attr in syllable[2]]))
                    for syllable in syllables
                    if len(syllable[2]) == 1 and syllable[0] != None
            ]
    non_melismas = {}
    for item in nonmelismatic:
        if item[0] not in non_melismas:
            non_melismas[item[0]] = 1
        else:
            non_melismas[item[0]] += 1
    print('\nNumber of non-melismatic syllables:')
    for tone in U.seven_tones:
        print(tone, non_melismas[tone])

    # Convert these counts into total percentages.
    print('\nPercentages of melismatic and non-melismatic syllables:')
    tone_counts = {}
    for tone in U.seven_tones:
        tone_counts[tone] = sum(melisma_count[tone]) + non_melismas[tone]
        non_melismas[tone] = round(
                100 * non_melismas[tone] / tone_counts[tone], 1)
        for i, _ in enumerate(melisma_count[tone]):
            melisma_count[tone][i] = round(
                    100 * melisma_count[tone][i] / tone_counts[tone], 1)
        print('{}: {}; {}'.
                format(tone, melisma_count[tone], non_melismas[tone]))