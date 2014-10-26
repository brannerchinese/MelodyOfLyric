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
            ('kú', ('yīnshǎng', '●'), 2),
            ('chiú', ('yīnshǎng', '●'), 4),
            ('io̍k', ('yángrù', '●'), 1)
            ]
    assert P.get_syllables(filename) == expected_result
