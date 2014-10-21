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

def test_get_note_attrs_01():
    notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_accidentals.xml'))
    assert R.get_note_attrs(notes[0]) == {
            'pitch_data': {'step': 'C', 'alter': '1', 'octave': '5'},
            'duration': '1'}
    assert R.get_note_attrs(notes[1]) == {
            'pitch_data': {'step': 'C', 'alter': '1', 'octave': '5'},
            'duration': '1'}
    assert R.get_note_attrs(notes[2]) == {
            'pitch_data': {'step': 'C', 'octave': '5'}, 'duration': '1'}
    assert R.get_note_attrs(notes[3]) == {
            'pitch_data': {'step': 'C', 'alter': '1', 'octave': '5'},
            'duration': '1'}
    with pytest.raises(IndexError):
        R.get_note_attrs(notes[4])

def test_get_note_attrs_02():
    notes = R.get_notes(os.path.join(
            '..', 'test', 'data', 'test_cross_barline.xml'))
    for i, note in enumerate(notes):
        assert R.get_note_attrs(notes[0]) == {
                'duration': '2', 'rest': True}
        assert R.get_note_attrs(notes[1]) == {
                'duration': '1', 'rest': True}
        assert R.get_note_attrs(notes[2]) == {
                'pitch_data': {'step': 'C', 'alter': '1', 'octave': '5'},
                'duration': '2'}
        assert R.get_note_attrs(notes[3]) == {
                'pitch_data': {'step': 'C', 'alter': '1', 'octave': '5'},
                'duration': '2'}
        assert R.get_note_attrs(notes[4]) == {
                'pitch_data': {'step': 'C', 'octave': '5'},
                'duration': '1', 'tied': True}
        assert R.get_note_attrs(notes[5]) == {
                'pitch_data': {'step': 'C', 'octave': '5'},
                'duration': '1', 'tied': True}
        assert R.get_note_attrs(notes[6]) == {
                'pitch_data': {'step': 'C', 'alter': '1', 'octave': '5'},
                'duration': '2'}
        assert R.get_note_attrs(notes[7]) == {
                'duration': '1', 'rest': True}
        assert R.get_note_attrs(notes[8]) == {
                'duration': '2', 'rest': True}
        assert R.get_note_attrs(notes[9]) == {
                'duration': '2', 'rest': True}

