#! /usr/bin/env python
# utils.py
# David Prager Branner
# 20141025

step_to_pitch = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

seven_tones = [
        'yīnpíng',
        'yángpíng',
        'yīnshǎng',
        'yīnqù',
        'yángqù',
        'yīnrù',
        'yángrù']

def step_to_midi(step, octave, alter=0):
    """Produce the MIDI note number and do basic validation."""
    # Note that MIDI treats Middle C as note 60 (octave 5); MusicXML treats it
    # as being the first note in octave 4. Hence we add 12, for the extra
    # octave.
    if any([not isinstance(i, int) for i in [alter, octave]]):
        raise Exception
    if step not in step_to_pitch:
        raise Exception
    midi_pitch = (octave * 12) + (step_to_pitch[step] + alter) + 12
    if not (0 <= midi_pitch <= 127):
        raise Exception
    else:
        return midi_pitch

def check_consistency(note_attr_list):
    """Check that certain known problems do not occur (Not yet complete.)"""
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

def identify_tone(syllable):
    """From diacritics and final consonants, identify tone category and ○/●. """
    vowels = syllable.strip('bcghjklmnⁿpstz')
    diacritic = vowels.strip('aeioơu')
    if len(diacritic) > 1:
        raise Exception('Syllable {} has more than one diacritic.'.
                format(diacritic))
    if diacritic and diacritic in 'âêîôơ̂û':
        return ('yángpíng', '○')
    elif syllable[-1] in 'ptkh':
        # Rùshēng, and we are accounting for forms like mahⁿ (ⁿ stripped above).
        if not diacritic:
            return ('yīnrù', '●')
        # diacritic in 'a̍e̍i̍o̍u̍'
        else:
            return ('yángrù', '●')
    elif not diacritic:
        return ('yīnpíng', '○')
    elif diacritic and diacritic in 'āēīōơ̄ū':
        return ('yángqù', '●')
    elif diacritic and diacritic in 'àèìòờù':
        return ('yīnqù', '●')
    else:
        # diacritic in 'áéíóớú'
        return ('yīnshǎng', '●')

def append_syllable(syllables, value, syllabic, note_attrs):
    """Append value and note_attrs to syllables."""
    syllables.append((value, syllabic, [note_attrs]))
    return syllables

def increment_duration(syllables, note_attrs):
    """Combine the duration of current note to previous note."""
    syllables[-1][-1][-1]['duration'] += note_attrs['duration']
    return syllables

def sum_syllable_durations(syllable_tuple):
    """Given a syllable_tuple, sum the durations of its notes and return."""
#    if syllable_tuple[0] == None:
#        return
    total_duration = 0
    for note in syllable_tuple[-1]:
        total_duration += note['duration']
    return total_duration

def get_melody(xml_notes, divisions):
    return [
            R.get_note_attrs(xml_note, divisions)['pitch_data'] 
            for xml_note in xml_notes]

def get_intervals(melody):
    return [second - first for first, second in zip(melody, melody[1:])]

def nest_sublists(lst, length):
    """Given a flat list, create nested sublists each <= length."""
    return [
        [sublist for sublist in lst[index:index+length]]
            for index in range(0, len(lst), length)
            if index <= len(lst)
        ]