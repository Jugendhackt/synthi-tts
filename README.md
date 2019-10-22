# synthi-tts

Digitize your own voice to have it speak for you! Fully automated!

![Made at Jugend Hackt 2019 Berlin](http://jhbadge.com/?evt=ber&year=2019)

**Notice by Niklas:** I've taken this prototype and [re-implemented it to make everything sound a lot better!](https://github.com/nkreer/sinatoki) I would like to thank everyone who helped me bring this idea to life, especially Moritz and Jackob who were responsible for the code in this repo!

---

## Creating the voice model

- Speak a little! [audio.mp3]
- Transcribe what you've said [plain text - transcription.txt]
- use forced aligner (gentle) to match timecodes in audio and transcript
- extract phoneme slices (ffmpeg)

```bash
# prepare audio.mp3 and transcription.txt
# you need docker pre-installed
# this will generate an output.json inside the path specified.
./gentle-docker.sh <path> <audio.mp3> <transcription.txt>
python3 json-times-voice-to-samples.py <path/output.json> [output-folder]
```

## Speech synthesis

- requires the voice model created prior to this step
- enter text
- convert to IPA-phonetics (espeak)
- intelligently concatenate voice samples from the model (ffmpeg)

```bash
# make sure that voice model is complete
# English is recommended
python3 synthi-tts.py "Your text here" -f <output-folder>
```

Use ```python3 synthi-tts.py --help``` for further help with arguments you may use.

## TODO

* Matching and concatenation on syllable/word level for even better and more understandable synthesis
* Audio edits to remove glottal stops at the end of the short voice samples
* make this a lot faster!
* write an interface so it can be used as your voice system-wide
* graphical TTS utility
