import sys
import fileinput

ipa = ""
if len(sys.argv) > 1:
    ipa = sys.argv[1]
else:
    ipa = fileinput.input()[0].strip()

map = {}

with open("audiosamples-1/map", encoding="utf-8") as f:
    for line in f.readlines():
        phon, audio = line.strip().split(":")
        audio = "audiosamples-1/" + audio
        if phon and not phon in map:
            map[phon] = audio

#print(map)

for phon in ipa:
    if phon.strip():
        if phon in map:
            print(phon + ":" + map[phon])
        else:
            print(phon + ":" + "----------")
