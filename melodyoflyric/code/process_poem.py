#! /usr/bin/env python
# process_poem.py
# David Prager Branner
# 20141025

import os
import read_xml as R
import utils as U

def get_syllables(filename=os.path.join(
        '..', 'data', 'sheu_ityng_pyiparshyng_20141025.xml')):
    """Get all syllables of poem, their tones, and their durations."""
    syllables = [(
            syllable[0], 
            U.identify_tone(syllable[0]), 
            U.sum_syllable_durations(syllable)) 
                for syllable in R.main(filename) if syllable[0]
            ]
    return syllables

