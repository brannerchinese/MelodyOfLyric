#! /usr/bin/env python
# read_xml.py
# David Prager Branner
# 20141106

"""Open and analyze a MusicXML file."""

import sys
import os
import io
import lxml.etree
import utils as U

def main(filename=os.path.join(
        '..', 'data', 
        '''sheu_ityng_pyiparshyng_20141031_edited_thru_meas_191.xml''')):
    xml_notes, divisions = get_notes(filename)
    note_attr_list = [
            get_note_attrs(xml_note, divisions) for xml_note in xml_notes]
    if U.check_consistency(note_attr_list):
        syllables = get_syllables(note_attr_list)
    return syllables, divisions

def get_notes(filename):
    """Return list of 'note' elements from MusicXML file."""
    with open(filename, 'rb') as f:
        content = f.read()
    parser = lxml.etree.HTMLParser(recover=True)
    root = None
    try:
        root = lxml.etree.parse(io.BytesIO(content), parser)
    except lxml.etree.XMLSyntaxError:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    xml_notes = root.xpath('//note')
    divisions = root.xpath('//divisions')
    if len(divisions) > 1:
        raise Exception('<divisions> element is of cardinality {}.'.
                format(len(divisions)))
    return xml_notes, int(divisions[0].text)

def get_note_attrs(xml_note, divisions):
    """For a given note return the elements we need."""
    note_attrs = {}
    for child in xml_note.getchildren():
        # "if child is None" is required syntax; "if not child" is deprecated.
        if child is None:
            continue
        if child.tag == 'pitch':
            pitch_data = {i.tag: i.text for i in child}
            step, octave = pitch_data['step'], int(pitch_data['octave'])
            if 'alter' in pitch_data:
                alter = int(pitch_data['alter'])
            else:
                alter = 0
            note_attrs['pitch_data'] = U.step_to_midi(step, octave, alter)
        elif child.tag == 'rest':
            note_attrs['rest'] = True
        elif child.tag == 'duration':
            note_attrs['duration'] = int(child.text) / divisions
        elif child.tag == 'notations':
            note_attrs['tied'] = any([True for i in child if i.tag == 'tied'])
        elif child.tag == 'lyric':
            lyric_number = child.items()[0][1]
            note_attrs['lyric_' + lyric_number] = {i.tag: i.text for i in child}
    return note_attrs

def get_syllables(note_attr_list):
    """From list of note-by-note dictionaries produce list of syllables."""
    syllables = []
    last_note = 'impossible starting value'
    # Delete rests at start or finish, retain others as None syllables.
    for i, note_attrs in enumerate(note_attr_list):
        # Content of syllables: [(syllable, [setting_notes])]
        try:
            # We are in rest, not note.
            del note_attrs['rest']
        except KeyError:
        # If there is no rest, then you have note and syllable.
            # Deal with note tied to previous note. Either way, delete "tied".
            if note_attrs.get('tied'): 
                del note_attrs['tied']
                # Is last note's pitch same as pitch of current note?
                if note_attrs.get('pitch_data') == last_note:
                    # Supplement last note's length and discard current.
                    syllables = U.increment_duration(syllables, note_attrs)
                else:
                    # Tied but not to previous note; must be to next note.
                    # Should therefore appear as new syllable.
                    if 'lyric_1' not in note_attrs:
                        syllables[-1][2].append(note_attrs)
                    else:
                        lyric = note_attrs.pop('lyric_1')
                        syllables = U.append_syllable(syllables, 
                                lyric['text'], lyric['syllabic'], note_attrs)
                    last_note = note_attrs.get('pitch_data')
            else:
                # Not tied. 
                if 'tied' in note_attrs:
                    del note_attrs['tied']
                # Pop current syllable; deal with lyric_1 by default.
                # But if no lyric is present, append note to previous syllable.
                if 'lyric_1' not in note_attrs:
                    syllables[-1][2].append(note_attrs)
                else:
                    lyric = note_attrs.pop('lyric_1')
                    syllables = U.append_syllable(syllables, 
                            lyric['text'], lyric['syllabic'], note_attrs)
                # Next time last_note is examined it should never match.
                last_note = 'impossible starting value'
        else:
            # Perform these if rest.
            value = None
            # If previous note was rest, 
            # increase its value and do not append this one.
            if last_note == None:
                syllables = U.increment_duration(syllables, note_attrs)
            else:
                syllables = U.append_syllable(
                        syllables, value, value, note_attrs)
                last_note = value
    return syllables

def display_children(notes):
    """Display the children of a notes object. (Used for early debugging.)"""
    for note in notes:
        print('\nNew note:')
        for child in note.getchildren():
            print('child.tag: {}'.format(child.tag), end='\t')
            if child.text and child.text[0] != '\n':
                print('child.text: {}'.format(child.text), end='\t')
            if child.items():
                print('child.items(): {}'.format(child.items()), end='\t')
            if child:
                grandchildren = [(grandchild.tag, grandchild.text) 
                        for grandchild in child]
                for grandchild in grandchildren:
                    print('\n\tgrandchild.tag: {}\tgrandchild.text: {}'.
                            format(grandchild[0], grandchild[1]), 
                            end='\t')
            print()

def display_notes(xml_notes):
    """Print all subitems of all notes. (Used for early debugging.)"""
    for note in notes:
        for item in note:
            if not item:
                continue
            print('  item: {}; subitems: {}'.format(item, list(item)))
            for subitem in item:
                print('    subitem: {}'.format(subitem))
                for subsubitem in subitem:
                    print('      subsubitem: {}'.format(subsubitem))

