Music transcription notes

 1. Dylan Maldonado-Roberts
 
   1. Ad seen on Columbia-area bus-shelter for Dylan, 212-473-7423. Whitepages.com shows as Dylan Maldonado, 30-34 years old.  85 E 10th St Apt 6s New York, NY 10003-5441.
   
   1. Left phone message, 20140903.
   
   1. At http://www.hotfrog.com/Companies/Dylan-Roberts-Music found: http://www.dylanrobertsmusic.com. dylanrobertsmusic@gmail.com

 1. Matt Ostrowski. Wrote to ask about transcription and notation services/tools, 20140903. He says everyone uses [Sibelius](http://www.sibelius.com/products/audioscore/ultimate.html) for notation now.
 
 1. Jeff Fowler and Kat Barone-Adesi recommend using Praat to detect pitches.
 
 1. Mike Walker says:

        > For actually notating the music digitally, you'd probably enjoy Lilypond, a GPLed LaTeX-esque Scheme-based markup language for sheet music. Its default output is loads better than commercial software that costs hundreds of dollars, and if you're already approaching things from a programmer mindset it's not hard to learn. … Lilypond's default output is significantly better than the default output of Finale/Sibelius

 1. Suggestions from http://music.stackexchange.com/questions/4514:

   1. Generate Midi first.
   1. http://codingteam.net/project/scolily
   1. "[Synthesia](http://synthesiagame.com/) can display sheet music from a midi."
   1. Note-recognition system such as [SeventhString](http://www.seventhstring.com/xscribe/overview.html)

 1. Suggestions from http://dsp.stackexchange.com/questions/10364:
 
   1. [Aubio](http://aubio.org/). DPB finds available through Homebrew (20140903). Use `brew install aubio --with-python`, but use `pip` to install `numpy` first (Python 2 only). But insurmountable problems compiling; abandoned.
   1. [MuseScore](http://musescore.org/) (open-source alternative to Sibelius). See also http://www.osalt.com/musescore.

 1. Ubuntu results, from http://ubuntuforums.org/showthread.php?t=2198434:
 
   1. "Package scolily. I have not tried it. 'Description-en: Utility to create music scores from microphone'."
   1. Service: http://customguitartabs.com/.
   1. "There's also denemo, which is in the Software Center. It's not easy to install and has a rather steep learning curve. It also uses lilypond, and the printed pages are as professional looking as any you will ever see. I've used it before."

 1. Recommendations at http://en.softonic.com/s/music-note-recognition-software:
 
   1. [Audio To MiDi VST](http://audio-to-midi-vst.en.softonic.com/): "Real-time Audio to MIDI conversion. The plugin receives input from an audio channel and performs real-time music recognition. Resulting MIDI events can be sent to the VST host, System MIDI Out Device or to a MIDI file."

 1. Recommendations at http://stackoverflow.com/questions/5852102/software-to-convert-audio-to-midi:
 
   1. WAV to MIDI: **[WaoN](http://waon.sourceforge.net/)**. "read wav file and write standard MIDI file format 0." Available on HomeBrew (20140903).
   1. [SoX](http://sox.sourceforge.net/). SoX is a cross-platform (Windows, Linux, MacOS X, etc.) command line utility that can convert various formats of computer audio files in to other formats. It can also apply various effects to these sound files, and, as an added bonus, SoX can play and record audio files on most platforms.

 1. Recommendations at http://pedrokroger.net/converting-midi-files-mp3-mac-os/:
 
   1. [Fluidsynth](https://sourceforge.net/apps/trac/fluidsynth/): generate a MP3 from a MIDI. Installation instructions at http://apple.stackexchange.com/questions/107297/how-can-i-play-a-midi-file-from-terminal:
     1. Downloaded `GeneralUser` SoundFont from http://www.schristiancollins.com/generaluser.php.
     1. Renamed file `GeneralUser GS FluidSynth v1.44.sf2` to `GeneralUser_GS_FluidSynth_v1.44.sf2` and moved it to location of `fluidsynth` (which is a symlink, so follow that link to the directory's true location).
   1. Midi-to-sound-files: [Timidity++](http://timidity.sourceforge.net/#info). "TiMidity++ is a software synthesizer. It can play MIDI files by converting them into PCM waveform data; give it a MIDI data along with digital instrument data files, then it synthesizes them in real-time, and plays. It can not only play sounds, but also can save the generated waveforms into hard disks as various audio file formats."

 1. Others:
 
   1. [Mingus](https://code.google.com/p/mingus/) for Python.
   1. [transcribe-melodies](https://code.google.com/p/transcribe-melodies/) for Python. "Use the Echo Nest audio analysis tools (http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation_2.2.pdf) to segment the audio into notes and identify each note's pitch and duration. Then make a representation of the melody in music21 (http://mit.edu/music21/) to easily analyse, make notation, or make midi."
   1. [PythonInMusic](https://wiki.python.org/moin/PythonInMusic) for Python. 

 1. Midi editors
 
   1. midicsv: Convert `.mid` to or from `.csv`.

[end]