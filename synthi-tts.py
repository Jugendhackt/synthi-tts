#!/usr/bin/python3

from subprocess import Popen, PIPE
import sys
import os
import fileinput

text = ""
if len(sys.argv) > 1:
    text = sys.argv[1]
else:
    text = fileinput.input()[0].strip()

process = Popen(['espeak', '-q', '-x', '"' + text + '"'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
phonetic = stdout.decode('utf-8').strip()[5:]
#print(phonetic)

# create map from espeak-gentle translation
map = {}

with open("espeak-to-gentle", encoding="utf-8") as f:
    for line in f.readlines():
        phon, audio = line.split("=")
        audio = audio.split(" ")
        audio = [("everything/" + a.strip() + ".mp3") for a in audio]
        if len(phon) and not phon in map:
            map[phon] = audio

#map[" "] = ["silence.mp3"]
#print(map)


# create list of files from string
files = []

i = 0
while i < len(phonetic):
    if phonetic[i:i+3] in map:
        #print(phonetic[i:i+3] + "->" + ' '.join(map[phonetic[i:i+3]]), file=sys.stderr)
        files = files + map[phonetic[i:i+3]]
        i = i + 3
    elif phonetic[i:i+2] in map:
        #print(phonetic[i:i+2] + "->" + ' '.join(map[phonetic[i:i+2]]), file=sys.stderr)
        files = files + map[phonetic[i:i+2]]
        i = i + 2
    elif phonetic[i:i+1] in map:
        #print(phonetic[i:i+1] + "->" + ' '.join(map[phonetic[i:i+1]]), file=sys.stderr)
        files = files + map[phonetic[i:i+1]]
        i = i + 1
    else:
        print(phonetic[i] + ": not found", file=sys.stderr)
        i = i + 1

command = "ffmpeg"

for file in files:
    command = command + " -f mp3 -i " + file
command = command + " -filter_complex '"

for i in range(len(files)):
    command = command + "["+str(i)+":0]"
command = command + "concat=n="+str(len(files))+":v=0:a=1[out]' -map [out] -loglevel warning output.mp3"

try:
    os.remove("output.mp3")
except OSError:
    pass
os.system(command)

