# test_utils.py
# David Prager Branner
# 20141021

import sys
import os
sys.path.append(os.path.join('..', 'code'))
import utils as U
import pytest

def test_step_to_midi_01():
    step = 'C'
    alter = 1
    octave = 4
    assert U.step_to_midi('C', 0, 4) == 60
