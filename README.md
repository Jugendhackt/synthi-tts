# THAT'S ME!

Deine Stimme digitalisieren und für dich sprechen lassen!

![made at Jugend Hackt 2019 Berlin](http://jhbadge.com/?evt=ber&year=2019)

## Vorhaben

### Daten sammeln

- Audio einsprechen  [audio.mp3]
- Audio traskribieren [plain text - transcription.txt]
- mit Force Aligner (gentle) Audio + Transkript zu Timecodes matchen
- Audiosample zerschnipseln (ffmpeg)

```bash
# prepare audio.mp3 and transcription.txt
# you need docker pre-installed
# this will generate an output.json inside the path specified.
./gentle-docker.sh [folder] [audio.mp3] [transcription.txt]
python3 json-times-voice-to-samples.py [folder/output.json]
```

### Text to speech

- [Audiodatenbank vom vorherigen Schritt]
- Text eingeben
- in IPA-Lautsprache wandeln (espeak)
- Audiosamples danach zusammenfügen (ffmpeg)

```bash
# make sure that voice model is complete
# only english is viable
python3 synthi-tts.py "Your text here"
```

