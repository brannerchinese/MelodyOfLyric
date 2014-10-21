# test_utils.py
# David Prager Branner
# 20141021

import sys
import os
sys.path.append(os.path.join('..', 'code'))
sys.path.append('data')
import read_xml as R
import pytest

def test_get_notes_01():
    # Four quarter notes.
    assert len(R.get_notes(os.path.join('data', 'test_accidentals.xml'))) == 4

def test_get_notes_02():
    # Two rests, three untied notes, a pair of tied notes, three more rests.
    assert len(R.get_notes(os.path.join(
            'data', 'test_cross_barline.xml'))) == 10
