#! /usr/bin/env python
# read_xml.py
# David Prager Branner
# 20141023

"""Open and analyze a MusicXML file."""

import sys
import os
import io
import lxml.etree

def main(filename=os.path.join(
        '..', 'data', 'sheu_ityng_pyiparshyng_20141009.xml')):
    xml_notes = get_notes(filename)
    note_attr_list = [get_note_attrs(xml_note) for xml_note in xml_notes]
    if check_consistency(note_attr_list):
        syllables = get_syllables(note_attr_list)
    return syllables

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
    return xml_notes

## The following, with different handling of encoding, is marginally slower than 
## get_notes().
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

def display_notes(xml_notes):
    """Print all subitems of all notes."""
    for note in notes:
        for item in note:
            if not item:
                continue
            print('  item: {}; subitems: {}'.format(item, list(item)))
            for subitem in item:
                print('    subitem: {}'.format(subitem))
                for subsubitem in subitem:
                    print('      subsubitem: {}'.format(subsubitem))

def get_note_attrs(xml_note):
    note_attrs = {}
    for child in xml_note.getchildren():
        # "if child is None" is required syntax; "if not child" is deprecated.
        if child is None:
            continue
        if child.tag == 'pitch':
            note_attrs['pitch_data'] = {i.tag: i.text for i in child}
        elif child.tag == 'rest':
            note_attrs['rest'] = True
        elif child.tag == 'duration':
            note_attrs['duration'] = int(child.text)
        elif child.tag == 'notations':
            note_attrs['tied'] = any([True for i in child if i.tag == 'tied'])
        elif child.tag == 'lyric':
            lyric_number = child.items()[0][1]
            note_attrs['lyric_' + lyric_number] = {i.tag: i.text for i in child}
    return note_attrs

def check_consistency(note_attr_list):
    """Not yet complete."""
    consistency = True
    for note_attr in note_attr_list:
        if 'pitch_data' not in note_attr and 'rest' not in note_attr:
            print('Neither pitch_data nor rest found in {}.'.format(note_attr))
            consistency = False
        elif 'pitch_data' in note_attr and 'rest' in note_attr:
            print('Both pitch_data and rest found in {}.'.format(note_attr))
            consistency = False
        # Also, no "tied" in isolation and lyric only at start of "tied" chain.
        # Does every note have duration?
    return consistency

def get_syllables(note_attr_list):
    """From list of note-by-note dictionaries produce list of syllables."""
    syllables = []
    last_note = 'impossible starting value'
    # Delete rests at start or finish, retain others as None syllables.
    for i, note_attrs in enumerate(note_attr_list):
        print('\n{}: {}'.format(i, note_attrs))
        # Content of syllables: [(syllable, [setting_notes])]
        try:
            # We are in rest, not note.
            del note_attrs['rest']
        except KeyError:
        # If there is no rest, then you have note and syllable.
            print('    Found syllable:', note_attrs)
            # First deal with note tied to previous note.
            if note_attrs.get('tied'): 
                # Is last note's pitch same as pitch of current note?
                if note_attrs.get('pitch_data').get('step') == last_note:
                    print("""    note_attrs.get('pitch_data').get('step') == """
                          """    last_note: {} == {}""".format(
                          note_attrs.get('pitch_data').get('step'), last_note)) 
                    # Supplement last note's length and discard current.
                    print("""    syllables[-1][1][-1]['duration'] += """
                          """note_attrs['duration']: {} += {}|""".
                          format(syllables[-1][1][-1]['duration'],
                          note_attrs['duration']))
                    syllables = increment_duration(syllables, note_attrs)
                    print("""    new duration:""", 
                            syllables[-1][1][-1]['duration']) # debug
                    print('    Do not append this SYLLABLE.')
                    print('    NON-FIRST TIED NOTE currently syllables:', 
                            syllables, end='\n\n')
                else:
                    # Tied but not to previous note; must be to next note.
                    # Should therefore appear as new syllable.
                    if 'lyric_1' not in note_attrs:
                        syllables[-1][1].append(note_attrs)
                    else:
                        syllables = append_syllable(syllables, 
                                note_attrs.pop('lyric_1')['text'], note_attrs)
                    last_note = note_attrs.get('pitch_data').get('step')
            else:
                # Not tied. 
                print('    Note is not tied.')
                # Pop current syllable; deal with lyric_1 by default.
                # But if no lyric is present, append note to previous syllable.
                if 'lyric_1' not in note_attrs:
#                    print("    syllables[-1]", syllables[-1])
                    syllables[-1][1].append(note_attrs)
                else:
                    syllables = append_syllable(syllables, 
                            note_attrs.pop('lyric_1')['text'], note_attrs)
                # Next time last_note is examined it should never match.
                last_note = 'impossible starting value'
                print('    Popped', syllables[-1][0])
                print('    Current last note:', last_note)
        else:
            # Perform these if rest.
            value = None
            # If previous note was rest, 
            # increase its value and do not append this one.
            if last_note == None:
                print("""last_note == None; syllables[-1][1][-1]['duration']: """
                      """{}; note_attrs['duration']: {}""".
                      format(syllables[-1][1][-1]['duration'], 
                            note_attrs['duration']))
                syllables = increment_duration(syllables, note_attrs)
                print("now syllables[-1][1][-1]['duration']: {}".
                        format(syllables[-1][1][-1]['duration']))
                print('    Do not append this REST.')
            else:
                syllables = append_syllable(syllables, value, note_attrs)
                print('    Appended rest:', value)
                last_note = value
        finally:
            print('    FINALLY currently syllables:', syllables, end='\n\n')
    return syllables

def append_syllable(syllables, value, note_attrs):
    syllables.append((value, [note_attrs]))
    return syllables

def increment_duration(syllables, note_attrs):
    syllables[-1][1][-1]['duration'] += note_attrs['duration']
    return syllables

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
