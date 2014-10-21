#! /usr/bin/env python
# read_xml.py
# David Prager Branner
# 20141020

"""Open and analyze a MusicXML file."""

import sys
import os
import io
import lxml.etree

def main():
    pass

def get_notes(filename=os.path.join(
        '..', 'data', 'sheu_ityng_pyiparshyng_20141009.xml')):
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
    notes = root.xpath('//note')
    return notes

## The following is marginally slower than the previous example.
#def open_and_parse1(filename='sheu_ityng_pyiparshyng_20141009.xml'):
#    """Return list of 'note' elements from MusicXML file."""
#    filename = os.path.join('..', 'data', filename)
#    with open(filename, 'r') as f:
#        content = f.read()
#    parser = lxml.etree.HTMLParser(recover=True)
#    root = None
#    try:
#        root = lxml.etree.parse(io.BytesIO(bytes(content, 'utf-8')), parser)
#    except lxml.etree.XMLSyntaxError:
#        exc_type, exc_value, exc_traceback = sys.exc_info()
#        traceback.print_exception(exc_type, exc_value, exc_traceback)
#    notes = root.xpath('//note')
#    return notes

def display_notes(notes):
    """Print all subitems of all notes."""
    for note in notes:
#        print(list(note))
        for item in note:
            if not item:
                continue
            print('  item: {}; subitems: {}'.format(item, list(item)))
            for subitem in item:
                print('    subitem: {}'.format(subitem))
                for subsubitem in subitem:
                    print('      subsubitem: {}'.format(subsubitem))

def get_note_attrs(note):
    note_attrs = {}
    for child in note.getchildren():
        # "if child is None" is required syntax; "if not child" is deprecated.
        if child is None:
            continue
        if child.tag == 'pitch':
            note_attrs['pitch_data'] = {i.tag: i.text for i in child}
        elif child.tag == 'rest':
            note_attrs['rest'] = True
        elif child.tag == 'duration':
            note_attrs['duration'] = child.text
        elif child.tag == 'notations':
            note_attrs['tied'] = any([True for i in child if i.tag == 'tied'])
        elif child.tag == 'lyric':
            lyric_number = child.items()[0][1]
            note_attrs['lyric_' + lyric_number] = {i.tag: i.text for i in child}
    return note_attrs

def display_children(notes):
    for note in notes:
        print('\nNew note:')
        for child in note.getchildren():
#            if child.tag == 'duration':
#                return child
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

# Notes:
#
# pitch:
#     [grandchild.tag: step	grandchild.text: D - child.e., well-tempered note
#      grandchild.tag: alter	grandchild.text: 0: no accidental; 1: sharp; -1: flat — this information seems to be the same as the accidental
#      grandchild.tag: octave	grandchild.text: 4] - which octave
#
# lyric 
#    [('number', '1')] - used for rows of lyrics
#    [('single', 'syllabic'), - single vs. begin/end/middle
#     ('sip', 'text')] - actual transcription
#
# notations
#     [grandchild.tag: tied	grandchild.text: None - important for extending note
#      grandchild.tag: slur	grandchild.text: None] - not needed
#
# duration — number in 32nds — we can sum them in order to find the total duration of a syllable.
# 
# Don't need:
# voice - in case we have multiple voices
# type - type of graphic note - e.g., quarter — represents duration
# accidental - this information is already presented in pitch.alter
# stem - direction of note's stem
# beam [('number', '1')]
# rest - no other information


# Last full line:

# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: C	
# 	grandchild.tag: octave	grandchild.text: 4	
# child.tag: duration	child.text: 8	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: quarter	
# child.tag: stem	child.text: down	
# child.tag: lyric	child.items(): [('number', '1')]	
# 	grandchild.tag: syllabic	grandchild.text: begin	
# 	grandchild.tag: text	grandchild.text: kang	
# child.tag: lyric	child.items(): [('number', '2')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: 江	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: D	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 4	
# child.tag: duration	child.text: 8	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: quarter	
# child.tag: accidental	child.text: sharp	
# child.tag: stem	child.text: down	
# child.tag: lyric	child.items(): [('number', '1')]	
# 	grandchild.tag: syllabic	grandchild.text: end	
# 	grandchild.tag: text	grandchild.text: chiu	
# child.tag: lyric	child.items(): [('number', '2')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: 州	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: A	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 3	
# child.tag: duration	child.text: 8	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: quarter	
# child.tag: accidental	child.text: sharp	
# child.tag: stem	child.text: up	
# child.tag: lyric	child.items(): [('number', '1')]	
# 	grandchild.tag: syllabic	grandchild.text: begin	
# 	grandchild.tag: text	grandchild.text: su	
# child.tag: lyric	child.items(): [('number', '2')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: 司	
# child.tag: lyric	child.items(): [('number', '3')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: ritardando	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: C	
# 	grandchild.tag: octave	grandchild.text: 4	
# child.tag: duration	child.text: 4	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: eighth	
# child.tag: stem	child.text: up	
# child.tag: beam	child.text: begin	child.items(): [('number', '1')]	
# child.tag: notations	
# 	grandchild.tag: slur	grandchild.text: None	
# child.tag: lyric	child.items(): [('number', '1')]	
# 	grandchild.tag: syllabic	grandchild.text: end	
# 	grandchild.tag: text	grandchild.text: máⁿ	
# child.tag: lyric	child.items(): [('number', '2')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: 馬	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: G	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 3	
# child.tag: duration	child.text: 4	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: eighth	
# child.tag: accidental	child.text: sharp	
# child.tag: stem	child.text: up	
# child.tag: beam	child.text: end	child.items(): [('number', '1')]	
# child.tag: notations	
# 	grandchild.tag: slur	grandchild.text: None	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: A	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 3	
# child.tag: duration	child.text: 8	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: quarter	
# child.tag: accidental	child.text: sharp	
# child.tag: stem	child.text: up	
# child.tag: lyric	child.items(): [('number', '1')]	
# 	grandchild.tag: syllabic	grandchild.text: begin	
# 	grandchild.tag: text	grandchild.text: chheng	
# child.tag: lyric	child.items(): [('number', '2')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: 青	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: D	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 4	
# child.tag: duration	child.text: 8	
# child.tag: tie	child.items(): [('type', 'start')]	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: quarter	
# child.tag: accidental	child.text: sharp	
# child.tag: stem	child.text: down	
# child.tag: notations	
# 	grandchild.tag: tied	grandchild.text: None	
# child.tag: lyric	child.items(): [('number', '1')]	
# 	grandchild.tag: syllabic	grandchild.text: end	
# 	grandchild.tag: text	grandchild.text: sam	
# child.tag: lyric	child.items(): [('number', '2')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: 衫	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: D	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 4	
# child.tag: duration	child.text: 4	
# child.tag: tie	child.items(): [('type', 'stop')]	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: eighth	
# child.tag: stem	child.text: up	
# child.tag: beam	child.text: begin	child.items(): [('number', '1')]	
# child.tag: notations	
# 	grandchild.tag: tied	grandchild.text: None	
# 	grandchild.tag: slur	grandchild.text: None	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: C	
# 	grandchild.tag: octave	grandchild.text: 4	
# child.tag: duration	child.text: 4	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: eighth	
# child.tag: stem	child.text: up	
# child.tag: beam	child.text: continue	child.items(): [('number', '1')]	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: A	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 3	
# child.tag: duration	child.text: 4	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: eighth	
# child.tag: accidental	child.text: sharp	
# child.tag: stem	child.text: up	
# child.tag: beam	child.text: continue	child.items(): [('number', '1')]	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: F	
# 	grandchild.tag: octave	grandchild.text: 3	
# child.tag: duration	child.text: 4	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: eighth	
# child.tag: stem	child.text: up	
# child.tag: beam	child.text: end	child.items(): [('number', '1')]	
# child.tag: notations	
# 	grandchild.tag: slur	grandchild.text: None	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: A	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 3	
# child.tag: duration	child.text: 4	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: eighth	
# child.tag: accidental	child.text: sharp	
# child.tag: stem	child.text: up	
# child.tag: notations	
# 	grandchild.tag: slur	grandchild.text: None	
# child.tag: lyric	child.items(): [('number', '1')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: sip	
# child.tag: lyric	child.items(): [('number', '2')]	
# 	grandchild.tag: syllabic	grandchild.text: single	
# 	grandchild.tag: text	grandchild.text: 濕	
# 
# New note:
# child.tag: pitch	
# 	grandchild.tag: step	grandchild.text: G	
# 	grandchild.tag: alter	grandchild.text: 1	
# 	grandchild.tag: octave	grandchild.text: 3	
# child.tag: duration	child.text: 8	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: quarter	
# child.tag: accidental	child.text: sharp	
# child.tag: stem	child.text: up	
# child.tag: notations	
# 	grandchild.tag: slur	grandchild.text: None	
# 
# New note:
# child.tag: rest	
# child.tag: duration	child.text: 4	
# child.tag: voice	child.text: 1	
# child.tag: type	child.text: eighth	
# 
# New note:
# child.tag: rest	
# child.tag: duration	child.text: 16	
# child.tag: voice	child.text: 1
