# THAT'S ME!

Deine Stimme digitalisieren und für dich sprechen lassen!

## Vorhaben

### Daten sammeln

- Audio einsprechen
- Audio traskribieren
- mit Force Aligner (gentle) Audio + Transkript zu Timecodes matchen
- Audiosample zerschnipseln (ffmpeg)

### Text to speech

- [Audiodatenbank]
- Text eingeben
- in IPA-Lautsprache wandeln (espeak)
- Audiosamples danach zusammenfügen (ffmpeg)


### How to use

- python3 ipa-to-files.py "hier den Text, der in Sprache umgesetzt werden soll" | python3 ffmpeg-concentenate-provided.py

Aligning speech with transcript:

- ./gentle-docker.sh /full/path/to/folder/containing/audio/and/transcripts audiofile transcriptfile

This will generate an output.json inside the path specified.

