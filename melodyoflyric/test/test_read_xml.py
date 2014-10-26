# test_utils.py
# David Prager Branner
# 20141026

import sys
import os
sys.path.append(os.path.join('..', 'code'))
sys.path.append('data')
import read_xml as R
import pytest

def test_get_notes_01():
    # Four quarter notes.
    assert len(R.get_notes(
            os.path.join('data', 'test_accidentals.xml'))) == 2

def test_get_notes_02():
    # Two rests, three untied notes, a pair of tied notes, three more rests.
    assert len(R.get_notes(os.path.join(
            'data', 'test_cross_barline.xml'))[0]) == 10

def test_get_note_attrs_01():
    xml_notes, divisions = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_accidentals.xml'))
    assert R.get_note_attrs(xml_notes[0], divisions) == {'pitch_data': 73, 'duration': 1}
    assert R.get_note_attrs(xml_notes[1], divisions) == {'pitch_data': 73, 'duration': 1}
    assert R.get_note_attrs(xml_notes[2], divisions) == {'pitch_data': 72, 'duration': 1}
    assert R.get_note_attrs(xml_notes[3], divisions) == {'pitch_data': 73, 'duration': 1}
    with pytest.raises(IndexError):
        R.get_note_attrs(xml_notes[4], divisions)

def test_get_note_attrs_02():
    xml_notes, divisions = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline.xml'))
    for i, note in enumerate(xml_notes):
        assert R.get_note_attrs(xml_notes[0], divisions) == {
                'duration': 1.0, 'rest': True}
        assert R.get_note_attrs(xml_notes[1], divisions) == {
                'duration': 0.5, 'rest': True}
        assert R.get_note_attrs(xml_notes[2], divisions) == {
                'pitch_data': 73,
                'duration': 1.0,
                'lyric_1': {'syllabic': 'single', 'text': 'one'}}
        assert R.get_note_attrs(xml_notes[3], divisions) == {
                'pitch_data': 73,
                'duration': 1.0,
                'lyric_1': {'syllabic': 'single', 'text': 'two'}}
        assert R.get_note_attrs(xml_notes[4], divisions) == {
                'pitch_data': 72,
                'duration': 0.5, 'tied': True,
                'lyric_1': {'syllabic': 'single', 'text': 'three'}}
        assert R.get_note_attrs(xml_notes[5], divisions) == {
                'pitch_data': 72,
                'duration': 0.5, 'tied': True}
        assert R.get_note_attrs(xml_notes[6], divisions) == {
                'pitch_data': 73,
                'duration': 1.0,
                'lyric_1': {'syllabic': 'single', 'text': 'four'}}
        assert R.get_note_attrs(xml_notes[7], divisions) == {
                'duration': 0.5, 'rest': True}
        assert R.get_note_attrs(xml_notes[8], divisions) == {
                'duration': 1.0, 'rest': True}
        assert R.get_note_attrs(xml_notes[9], divisions) == {
                'duration': 1.0, 'rest': True}

def test_get_note_attrs_03():
    xml_notes, divisions = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline_8-8.xml'))
    for i, note in enumerate(xml_notes):
        assert R.get_note_attrs(xml_notes[0], divisions) == {
                'duration': 1.5, 'rest': True}
        assert R.get_note_attrs(xml_notes[1], divisions) == {
                'pitch_data': 73, 'duration': 1.0}
        assert R.get_note_attrs(xml_notes[2], divisions) == {
                'pitch_data': 73, 'duration': 1.0}
        assert R.get_note_attrs(xml_notes[3], divisions) == {
                'pitch_data': 72, 'duration': 0.5, 'tied': True}
        assert R.get_note_attrs(xml_notes[4], divisions) == {
                'pitch_data': 72, 'duration': 0.5, 'tied': True}
        assert R.get_note_attrs(xml_notes[5], divisions) == {
                'pitch_data': 73, 'duration': 1.0}
        assert R.get_note_attrs(xml_notes[6], divisions) == {
                'duration': 0, 'rest': True}

def test_syllable_list_01():
    expected_result = [
            (None, None, [{'duration': 1.5}]),
            ('one', 'single', [{'pitch_data': 73, 'duration': 1.0}]),
            ('two', 'single', [{'pitch_data': 73, 'duration': 1.0}]),
            ('three', 'single', [{'pitch_data': 72, 'duration': 1.0}]),
            ('four', 'single', [{'pitch_data': 73, 'duration': 1.0}]),
            (None, None, [{'duration': 2.5}])
            ]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_cross_barline.xml'))[0] == expected_result

def test_syllable_list_02():
    expected_result = [
            (None, None, [{'duration': 1.5}]),
            ('first', 'single', [{'pitch_data': 73, 'duration': 1.0}]),
            ('second', 'single', [{'pitch_data': 73, 'duration': 1.0}]),
            ('third', 'single', [{'pitch_data': 72, 'duration': 1.0}]),
            ('fourth', 'single', [{'pitch_data': 73, 'duration': 1.0}]),
            (None, None, [{'duration': 4}])
            ]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_cross_barline_8-8_and_lyrics.xml'))[0] == expected_result

def test_syllable_list_03():
    expected_result = [
            (None, None, [{'duration': 1.5}]),
            ('one', 'single', [{'duration': 1.0, 'pitch_data': 73}]),
            ('two', 'single', [
                    {'duration': 0.5, 'pitch_data': 73}, 
                    {'duration': 0.5, 'pitch_data': 67}
                    ]),
            ('three', 'single', [{'duration': 1.0, 'pitch_data': 72}]),
            ('four', 'single', [{'duration': 1.0, 'pitch_data': 73}]),
             (None, None, [{'duration': 2.5}])
             ]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_cross_barline_with_melisma.xml'))[0] == expected_result

def test_syllable_list_04():
    expected_result = [
            (None, None, [{'duration': 1.5}]),
            ('one', 'single', [{'duration': 1.0, 'pitch_data': 73}]),
            ('two', 'single', [{'duration': 0.5, 'pitch_data': 73}]),
            ('three', 'single', [
                    {'duration': 0.5, 'pitch_data': 67}, 
                    {'duration': 1.0, 'pitch_data': 72}
                    ]),
            ('four', 'single', [{'duration': 1.0, 'pitch_data': 73}]),
            (None, None, [{'duration': 2.5}])
            ]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_cross_barline_with_tied_melisma.xml'))[0] == expected_result

def test_syllable_list_05():
    """Test case in which "syllabic" includes 'begin' and 'end'."""
    expected_result = [
            (None, None, [{'duration': 0.5}]),
            ('kú', 'begin',
             [{'duration': 1.0,
               'lyric_2': {'text': '舉', 'syllabic': 'single'},
               'pitch_data': 59}]),
            ('chiú', 'end',
             [{'duration': 0.5,
               'lyric_2': {'text': '酒', 'syllabic': 'single'},
               'pitch_data': 59},
              {'duration': 1.0, 'pitch_data': 57},
              {'duration': 0.5, 'pitch_data': 55}]),
            ('io̍k', 'single',
             [{'duration': 0.5,
               'lyric_2': {'text': '欲', 'syllabic': 'single'},
               'pitch_data': 52}])]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_syllabics_and_melisma.xml'))[0] == expected_result