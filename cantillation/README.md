## Cantillation-related studies

### Non-Python requirements

 1. [WaoN](https://github.com/kichiki/WaoN) for converting `.wav` to `.mid` (MIDI). (Available through HomeBrew.)
 1. [MIDICSV](http://www.fourmilab.ch/webtools/midicsv/) (includes CSVMIDI) for conversion between `.mid` MIDI files and text-editable `.csv` files. (Available through HomeBrew.)
 1. [Fluidsynth](https://sourceforge.net/apps/trac/fluidsynth/): generate a MP3 from a MIDI. Installation instructions at http://apple.stackexchange.com/questions/107297/how-can-i-play-a-midi-file-from-terminal:
     1. Download [`GeneralUser` SoundFont](http://www.schristiancollins.com/generaluser.php).
     1. Rename file `GeneralUser GS FluidSynth v1.44.sf2` to `GeneralUser_GS_FluidSynth_v1.44.sf2` and moved it to location of `fluidsynth` (which is a symlink, so follow that link to the directory's true location).

### Background on MIDI

 1. http://www.midi.org/techspecs/midimessages.php
 1. http://www.sonicspot.com/guide/midifiles.html

### Steps

 1. Convert `.wav` to `.mid`:

        waon -i recording.wav -o output.mid

   Note that there are many options to 

 1. Convert `.mid` to editable `.csv`:

        midicsv output.mid > output.mid.csv

 1. Run `clean_midi.py`, to isolate only the highest-velocity note at any time-tick:

        python clean_midi <filename.csv>

   or

        python clean_midi

   for default input filename `output.csv` and output `output_edited.csv`.

 1. Convert `.csv` to `.mid`:
 
        csvmidi output_edited.csv > output.csv.mid

 1. Play MIDI file:

        fluidsynth -i <soundfont> <MIDI file>

[end]
