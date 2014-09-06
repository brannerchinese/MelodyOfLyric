## Cantillation-related studies

### Non-Python requirements

 1. [WaoN](https://github.com/kichiki/WaoN) for converting `.wav` to `.mid` (MIDI). (Available through HomeBrew.)
 1. [MIDICSV](http://www.fourmilab.ch/webtools/midicsv/) (includes CSVMIDI) for conversion between `.mid` MIDI files and text-editable `.csv` files. (Available through HomeBrew.)
 1. [fluidsynth]() qqq
 1. SoundFont. qqq

### Steps

 1. Convert `.wav` to `.mid`:

        waon -i recording.wav -o output.mid

 1. Convert `.mid` to editable `.csv`:

        midicsv output.mid > output.mid.csv

 1. Run `clean_midi.py`:

        python clean_midi <filename.csv>

   or

        python clean_midi

   for default input filename `output.csv` and output `output_edited.csv`.

 1. Convert `.csv` to `.mid`:
 
        csvmidi output_edited.csv > output.csv.mid

 1. Play MIDI file:

        fluidsynth -i <soundfont> <MIDI file>

[end]
