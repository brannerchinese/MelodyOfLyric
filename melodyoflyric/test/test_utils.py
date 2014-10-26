# test_utils.py
# David Prager Branner
# 20141024

import sys
import os
sys.path.append(os.path.join('..', 'code'))
import read_xml as R
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

def test_check_consistency_01():
    xml_notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_accidentals.xml'))
    note_attr_list = [R.get_note_attrs(xml_note) for xml_note in xml_notes]
    assert U.check_consistency(note_attr_list)

def test_check_consistency_02():
    xml_notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline.xml'))
    note_attr_list = [R.get_note_attrs(xml_note) for xml_note in xml_notes]
    assert U.check_consistency(note_attr_list)

def test_check_consistency_03():
    xml_notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline_8-8.xml'))
    note_attr_list = [R.get_note_attrs(xml_note) for xml_note in xml_notes]
    assert U.check_consistency(note_attr_list)

def test_check_consistency_04():
    """Test of both 'pitch_data' and 'rest' in single note."""
    xml_notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline_8-8_extra_rest.xml'))
    note_attr_list = [R.get_note_attrs(xml_note) for xml_note in xml_notes]
    assert not U.check_consistency(note_attr_list)

def test_check_consistency_05():
    """Test of neither 'pitch_data' nor 'rest' in single note."""
    xml_notes = R.get_notes(os.path.join(
            '..', 'test', 'data',
            'test_cross_barline_8-8_no_rest_no_pitch.xml'))
    note_attr_list = [R.get_note_attrs(xml_note) for xml_note in xml_notes]
    assert not U.check_consistency(note_attr_list)

def test_identify_tone_01():
    """Test tone category identification."""
    # Test all seven tones.
    # Test all vowels.
    # Test final ⁿ, up to two final and three initial consonants.
    # Test diacritic on first of two vowels.
    assert U.identify_tone('chhiong') == ('yīnpíng', '○')
    assert U.identify_tone('kui') == ('yīnpíng', '○')
    assert U.identify_tone('gîm') == ('yángpíng', '○')
    assert U.identify_tone('bî') == ('yángpíng', '○')
    assert U.identify_tone('bêng') == ('yángpíng', '○')
    assert U.identify_tone('ngớⁿ') == ('yīnshǎng', '●')
    assert U.identify_tone('óng') == ('yīnshǎng', '●')
    assert U.identify_tone('àm') == ('yīnqù', '●')
    assert U.identify_tone('pòan') == ('yīnqù', '●')
    assert U.identify_tone('sòe') == ('yīnqù', '●')
    assert U.identify_tone('bān') == ('yángqù', '●')
    assert U.identify_tone('iā') == ('yángqù', '●')
    assert U.identify_tone('ngơ̄ⁿ') == ('yángqù', '●')
    assert U.identify_tone('sek') == ('yīnrù', '●')
    assert U.identify_tone('khip') == ('yīnrù', '●')
    assert U.identify_tone('to̍k') == ('yángrù', '●')
    assert U.identify_tone('bu̍t') == ('yángrù', '●')

def test_identify_tone_01():
    """Test fail on multiple diacritic."""
    with pytest.raises(Exception):
        U.identify_tone('bêòng')
    with pytest.raises(Exception):
        U.identify_tone('sòòk')
    with pytest.raises(Exception):
        U.identify_tone('gîîm')
    with pytest.raises(Exception):
        U.identify_tone('gîiîm')

def test_sum_syllable_durations_01():
    """Test summing syllable durations, melismatic and non-melismatic cases."""
    syllables = R.main(os.path.join(
            '..', 'test', 'data', 'test_syllabics_and_melisma.xml'))
    assert U.sum_syllable_durations(syllables[0]) == 1
    assert U.sum_syllable_durations(syllables[1]) == 2
    assert U.sum_syllable_durations(syllables[2]) == 4 # melismatic
    assert U.sum_syllable_durations(syllables[3]) == 1
