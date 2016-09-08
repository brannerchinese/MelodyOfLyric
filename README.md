## MelodyOfLyric

Tools for the analysis of MusicXML files of transcribed Taiwanese cantillation.

Not yet documented. There is a slide file in the `presentations` directory.

Tentatively, run the following in a REPL to get basic data:

```python
import process_poem
import untested_code
process_poem.avg_duration_by_place_and_pyngtzeh(syllables, divisions)
process_poem.avg_duration_by_place_and_tone(syllables, divisions)
process_poem.avg_duration_by_place(syllables, divisions)
process_poem.avg_duration_by_pyngtzeh(syllables, divisions)
process_poem.avg_duration_by_tone(syllables, divisions)
untested_code.main()
```

Needed here: 

 1. Description of process of transcription.
 1. List of functions available.

### Tests still needed:

 1. For `untested_code.py`. Also, move this code into `process_poem.py`.
 1. For `utils.get_melody()` and `utils.get_intervals()`.
 1. For `process_poem.count_melodies()`.

[end]
