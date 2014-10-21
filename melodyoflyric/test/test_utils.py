# test_utils.py
# David Prager Branner
# 20141021

import sys
import os
sys.path.append(os.path.join('..', 'code'))
import utils as U
import pytest

def test_step_to_midi_01():
    """Test handling of Middle C."""
    step = 'C'
    alter = 0
    octave = 4
    assert U.step_to_midi(step, alter, octave) == 60

def test_step_to_midi_02():
    """Test handling of non-integers."""
    step = 'C'
    alter = .1
    octave = 4
    with pytest.raises(Exception):
        U.step_to_midi(step, alter, octave)
    alter = 1
    octave = .4
    with pytest.raises(Exception):
        U.step_to_midi(step, alter, octave)

def test_step_to_midi_03():
    """Test handling of negative results."""
    step = 'C'
    alter = -1
    octave = -2
    with pytest.raises(Exception):
        U.step_to_midi(step, alter, octave)
    alter = 1
    octave = -4
    with pytest.raises(Exception):
        U.step_to_midi(step, alter, octave)

def test_step_to_midi_04():
    """Test handling of results above range."""
    step = 'C'
    alter = -1
    octave = 10
    with pytest.raises(Exception):
        U.step_to_midi(step, alter, octave)
    step = 'B'
    alter = 1
    octave = 9
    with pytest.raises(Exception):
        U.step_to_midi(step, alter, octave)
