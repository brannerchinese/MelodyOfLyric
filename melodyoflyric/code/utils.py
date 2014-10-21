#! /usr/bin/env python
# utils.py
# David Prager Branner
# 20141021

step_to_pitch = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

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
