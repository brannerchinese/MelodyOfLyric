# test_utils.py
# David Prager Branner
# 20141021

import sys
import os
sys.path.append(os.path.join('..', 'code'))
import utils as U
import pytest

def test_step_to_midi_01():
    """Test handling of some known notes."""
    # Middle C.
    step = 'C'
    octave = 4
    assert U.step_to_midi(step, octave) == 60
    # Highest MIDI note.
    step = 'G'
    octave = 9
    assert U.step_to_midi(step, octave) == 127
    # Lowest MIDI note.
    step = 'C'
    octave = -1
    assert U.step_to_midi(step, octave) == 0

def test_step_to_midi_02():
    """Test handling of non-integers."""
    step = 'C'
    alter = .1
    octave = 4
    with pytest.raises(Exception):
        U.step_to_midi(step, octave, alter)
    alter = 1
    octave = .4
    with pytest.raises(Exception):
        U.step_to_midi(step, octave, alter)

def test_step_to_midi_03():
    """Test handling of negative results."""
    # One octave below range.
    step = 'C'
    alter = -1
    octave = -2
    with pytest.raises(Exception):
        U.step_to_midi(step, octave, alter)
    # Three octaves below range.
    alter = 1
    octave = -4
    with pytest.raises(Exception):
        U.step_to_midi(step, octave, alter)

def test_step_to_midi_04():
    """Test handling of results above range."""
    # This should produce 131, above range.
    step = 'C'
    alter = -1
    octave = 10
    with pytest.raises(Exception):
        U.step_to_midi(step, octave, alter)
    # This should produce 128, 1 above range.
    step = 'G'
    alter = 1
    octave = 9
    with pytest.raises(Exception):
        U.step_to_midi(step, octave, alter)

def test_step_to_midi_05():
    """Test handling of non-scale note."""
    step = 'H'
    alter = -1
    octave = 5
    with pytest.raises(Exception):
        U.step_to_midi(step, octave, alter)
    step = 'b'
    alter = 1
    octave = 9
    with pytest.raises(Exception):
        U.step_to_midi(step, octave, alter)

def test_identify_tone():
    """From diacritics and final consonants, identify tone category and ○/●."""
    assert U.identify_tone('chhiong') == ('yīnpíng', '○')
    assert U.identify_tone('kui') == ('yīnpíng', '○')
    assert U.identify_tone('gîm') == ('yángpíng', '○')
    assert U.identify_tone('bî') == ('yángpíng', '○')
    assert U.identify_tone('bêng') == ('yángpíng', '○')
    assert U.identify_tone('ngớⁿ') == ('yīnshǎng', '●')
    assert U.identify_tone('óng') == ('yīnshǎng', '●')
    assert U.identify_tone('àm') == ('yīnqù', '●')
    assert U.identify_tone('àm') == ('yīnqù', '●')
    assert U.identify_tone('pòan') == ('yīnqù', '●')
    assert U.identify_tone('bān') == ('yángqù', '●')
    assert U.identify_tone('iā') == ('yángqù', '●')
    assert U.identify_tone('ngơ̄ⁿ') == ('yángqù', '●')
    assert U.identify_tone('sek') == ('yīnrù', '●')
    assert U.identify_tone('khip') == ('yīnrù', '●')
    assert U.identify_tone('to̍k') == ('yángrù', '●')
    assert U.identify_tone('bu̍t') == ('yángrù', '●')
