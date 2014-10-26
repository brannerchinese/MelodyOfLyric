# test_utils.py
# David Prager Branner
# 20141024

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

def test_get_note_attrs_01():
    xml_notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_accidentals.xml'))
    assert R.get_note_attrs(xml_notes[0]) == {'pitch_data': 73, 'duration': 1}
    assert R.get_note_attrs(xml_notes[1]) == {'pitch_data': 73, 'duration': 1}
    assert R.get_note_attrs(xml_notes[2]) == {'pitch_data': 72, 'duration': 1}
    assert R.get_note_attrs(xml_notes[3]) == {'pitch_data': 73, 'duration': 1}
    with pytest.raises(IndexError):
        R.get_note_attrs(xml_notes[4])

def test_get_note_attrs_02():
    xml_notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline.xml'))
    for i, note in enumerate(xml_notes):
        assert R.get_note_attrs(xml_notes[0]) == {
                'duration': 2, 'rest': True}
        assert R.get_note_attrs(xml_notes[1]) == {
                'duration': 1, 'rest': True}
        assert R.get_note_attrs(xml_notes[2]) == {
                'pitch_data': 73,
                'duration': 2,
                'lyric_1': {'syllabic': 'single', 'text': 'one'}}
        assert R.get_note_attrs(xml_notes[3]) == {
                'pitch_data': 73,
                'duration': 2,
                'lyric_1': {'syllabic': 'single', 'text': 'two'}}
        assert R.get_note_attrs(xml_notes[4]) == {
                'pitch_data': 72,
                'duration': 1, 'tied': True,
                'lyric_1': {'syllabic': 'single', 'text': 'three'}}
        assert R.get_note_attrs(xml_notes[5]) == {
                'pitch_data': 72,
                'duration': 1, 'tied': True}
        assert R.get_note_attrs(xml_notes[6]) == {
                'pitch_data': 73,
                'duration': 2,
                'lyric_1': {'syllabic': 'single', 'text': 'four'}}
        assert R.get_note_attrs(xml_notes[7]) == {
                'duration': 1, 'rest': True}
        assert R.get_note_attrs(xml_notes[8]) == {
                'duration': 2, 'rest': True}
        assert R.get_note_attrs(xml_notes[9]) == {
                'duration': 2, 'rest': True}

def test_get_note_attrs_03():
    xml_notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline_8-8.xml'))
    for i, note in enumerate(xml_notes):
        assert R.get_note_attrs(xml_notes[0]) == {
                'duration': 720, 'rest': True}
        assert R.get_note_attrs(xml_notes[1]) == {
                'pitch_data': 73, 'duration': 480}
        assert R.get_note_attrs(xml_notes[2]) == {
                'pitch_data': 73, 'duration': 480}
        assert R.get_note_attrs(xml_notes[3]) == {
                'pitch_data': 72, 'duration': 240, 'tied': True}
        assert R.get_note_attrs(xml_notes[4]) == {
                'pitch_data': 72, 'duration': 240, 'tied': True}
        assert R.get_note_attrs(xml_notes[5]) == {
                'pitch_data': 73, 'duration': 480}
        assert R.get_note_attrs(xml_notes[6]) == {
                'duration': 0, 'rest': True}

def test_syllable_list_01():
    expected_result = [
            (None, None, [{'duration': 3}]),
            ('one', 'single', [{'pitch_data': 73, 'duration': 2}]),
            ('two', 'single', [{'pitch_data': 73, 'duration': 2}]),
            ('three', 'single', [{'pitch_data': 72, 'duration': 2}]),
            ('four', 'single', [{'pitch_data': 73, 'duration': 2}]),
            (None, None, [{'duration': 5}])
            ]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_cross_barline.xml')) == expected_result

def test_syllable_list_02():
    expected_result = [
            (None, None, [{'duration': 3}]),
            ('first', 'single', [{'pitch_data': 73, 'duration': 2}]),
            ('second', 'single', [{'pitch_data': 73, 'duration': 2}]),
            ('third', 'single', [{'pitch_data': 72, 'duration': 2}]),
            ('fourth', 'single', [{'pitch_data': 73, 'duration': 2}]),
            (None, None, [{'duration': 8}])
            ]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_cross_barline_8-8_and_lyrics.xml')) == expected_result

def test_syllable_list_03():
    expected_result = [
            (None, None, [{'duration': 3}]),
            ('one', 'single', [{'duration': 2, 'pitch_data': 73}]),
            ('two', 'single', [
                    {'duration': 1, 'pitch_data': 73}, 
                    {'duration': 1, 'pitch_data': 67}
                    ]),
            ('three', 'single', [{'duration': 2, 'pitch_data': 72}]),
            ('four', 'single', [{'duration': 2, 'pitch_data': 73}]),
             (None, None, [{'duration': 5}])
             ]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_cross_barline_with_melisma.xml')) == expected_result

def test_syllable_list_04():
    expected_result = [
            (None, None, [{'duration': 3}]),
            ('one', 'single', [{'duration': 2, 'pitch_data': 73}]),
            ('two', 'single', [{'duration': 1, 'pitch_data': 73}]),
            ('three', 'single', [
                    {'duration': 1, 'pitch_data': 67}, 
                    {'duration': 2, 'pitch_data': 72}
                    ]),
            ('four', 'single', [{'duration': 2, 'pitch_data': 73}]),
            (None, None, [{'duration': 5}])
            ]
    assert R.main(os.path.join('..', 'test', 'data',
            'test_cross_barline_with_tied_melisma.xml')) == expected_result
