# process_poem.py
# David Prager Branner
# 20141026

import sys
import os
sys.path.append(os.path.join('..', 'code'))
import process_poem as P
import read_xml as R
import utils as U

def test_get_syllables_01():
    filename = os.path.join('..', 'test', 'data',
            'test_syllabics_and_melisma.xml')
    expected_result = [
            ('kú', ('yīnshǎng', '●'), 1.0),
            ('chiú', ('yīnshǎng', '●'), 2.0),
            ('io̍k', ('yángrù', '●'), 0.5)
            ]
    assert P.get_syllables(filename) == (expected_result, 2)
