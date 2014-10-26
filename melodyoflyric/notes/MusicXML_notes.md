## Notes on MusicXML Specification

 1. Reference at http://www.musicxml.com/UserManuals/MusicXML/MusicXML.htm

 1. **octave**: "Octaves are represented by the numbers 0 to 9, where 4 indicates the octave started by middle C." (http://www.musicxml.com/UserManuals/MusicXML/MusicXML.htm#EL-MusicXML-pitch.htm). So we should have a dictionary of correspondences, step to actual pitch: `{'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}`

   We are assuming equal temperament, so B# = C. 

 1. **alter**: "The alter element represents chromatic alteration in number of semitones (e.g., -1 for flat, 1 for sharp). Decimal values like 0.5 (quarter tone sharp) are used for microtones." Note that naturals are represented with the **accidental** element, not **alter**, so both must be considered in determining the actual pitch represented. Experimentally, in file test/data/test_accidentals.xml, we find that for successive C# in the same measure, the alter element shows the sharp value each time, while the accidental element shows only the first (i.e., accidental represents standard transcription while alter represents actual pitch). This is confirmed by the fact that C♮ in the same measure has no alter element but does have `<accidental>natural</accidental>`.

 1. `midi_pitch = (octave * 12) + (step value + alter) + 12`. The lowest legal value is 0. note that MIDI identifies Middle C as note #60, octave 5; Music XML identifies Middle C as not #48, octave 4. Hence we add 12 in calculating `midi_pitch`. (See http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm.) Note that MIDI's values assume octave 0 is equivalent to octave 1 in the MusicXML specification.

 1. Problem: **duration** seems to depend on **divisions**, a child-element of **measure**. How do we ensure that everything is uniform? But based on file 'sheu_ityng_pyiparshyng_20141009.xml' it appears that everything in a single document is regularized, so there is no problem about this. For more information see [the specification](http://www.musicxml.com/UserManuals/MusicXML/Content/EL-MusicXML-divisions.htm): 

        > The divisions element indicates how many divisions per quarter note are used to indicate a note's duration. For example, if duration = 1 and divisions = 2, this is an eighth note duration. Duration and divisions are used directly for generating sound output, so they must be chosen to take tuplets into account. Using a divisions element lets us use just one number to represent a duration for each note in the score, while retaining the full power of a fractional representation.

 1. **tied** notes are never single; both first and second always have `'tied': True`.

[end]
