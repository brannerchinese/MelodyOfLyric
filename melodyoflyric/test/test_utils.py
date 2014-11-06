# test_utils.py
# David Prager Branner
# 20141106

import sys
import os
sys.path.append(os.path.join('..', 'code'))
import read_xml as R
import utils as U
import pytest
import string

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
    xml_notes, divisions = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_accidentals.xml'))
    note_attr_list = [
            R.get_note_attrs(xml_note, divisions) for xml_note in xml_notes]
    assert U.check_consistency(note_attr_list)

def test_check_consistency_02():
    xml_notes, divisions = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline.xml'))
    note_attr_list = [
            R.get_note_attrs(xml_note, divisions) for xml_note in xml_notes]
    assert U.check_consistency(note_attr_list)

def test_check_consistency_03():
    xml_notes, divisions = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline_8-8.xml'))
    note_attr_list = [
            R.get_note_attrs(xml_note, divisions) for xml_note in xml_notes]
    assert U.check_consistency(note_attr_list)

def test_check_consistency_04():
    """Test of both 'pitch_data' and 'rest' in single note."""
    xml_notes, divisions = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline_8-8_extra_rest.xml'))
    note_attr_list = [
            R.get_note_attrs(xml_note, divisions) for xml_note in xml_notes]
    assert not U.check_consistency(note_attr_list)

def test_check_consistency_05():
    """Test of neither 'pitch_data' nor 'rest' in single note."""
    xml_notes, divisions = R.get_notes(os.path.join(
            '..', 'test', 'data',
            'test_cross_barline_8-8_no_rest_no_pitch.xml'))
    note_attr_list = [
            R.get_note_attrs(xml_note, divisions) for xml_note in xml_notes]
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
            '..', 'test', 'data', 'test_syllabics_and_melisma.xml'))[0]
    assert U.sum_syllable_durations(syllables[0]) == 0.5
    assert U.sum_syllable_durations(syllables[1]) == 1.0
    assert U.sum_syllable_durations(syllables[2]) == 2 # melismatic
    assert U.sum_syllable_durations(syllables[3]) == 0.5

def test_nest_sublists_01():
    length = 7
    lst = list(range(100))
    expected_result = [[0, 1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12, 13],
            [14, 15, 16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25, 26, 27],
            [28, 29, 30, 31, 32, 33, 34],
            [35, 36, 37, 38, 39, 40, 41],
            [42, 43, 44, 45, 46, 47, 48],
            [49, 50, 51, 52, 53, 54, 55],
            [56, 57, 58, 59, 60, 61, 62],
            [63, 64, 65, 66, 67, 68, 69],
            [70, 71, 72, 73, 74, 75, 76],
            [77, 78, 79, 80, 81, 82, 83],
            [84, 85, 86, 87, 88, 89, 90],
            [91, 92, 93, 94, 95, 96, 97],
            [98, 99]]
    U.nest_sublists(lst, length) == expected_result

s = string.ascii_lowercase

def test_find_all_substrings_01():
    """Test that "longest" > len(s) does not raise error."""
    assert (U.find_all_substrings(s, 17, 300) ==
            U.find_all_substrings(s, 17, 27))

def test_find_all_substrings_02():
    """Test that "longest" < len(s) does not raise error."""
    assert (U.find_all_substrings(s, 17, 5) ==
            U.find_all_substrings(s, 17, 18))

def test_find_all_substrings_03():
    """Test that "longest" == len(s) does not raise error."""
    assert (U.find_all_substrings(s, 17, 17) ==
            U.find_all_substrings(s, 17, 18))
