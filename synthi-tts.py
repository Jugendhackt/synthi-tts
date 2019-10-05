#!/usr/bin/python3

from subprocess import Popen, PIPE
import sys
import os

# Getting folder and files from CLI
folder = ""
text = ""
if len(sys.argv) > 2:
    folder = sys.argv[1]
    if not folder.endswith("/"):
        folder = folder + "/"
        
    text = sys.argv[2]
else:
    print('usage: python3 synthi-tts.py <voice sample folder> "<text>"', file=sys.stderr)
    sys.exit()


# Getting language from espeak
process = Popen(['espeak', '-q', '-x', '"' + text + '"'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
phonetic = stdout.decode('utf-8').strip()[5:].replace("'", "")
#print(phonetic)

# create e_map from espeak-gentle translation
e_map = {}

with open("espeak-to-gentle", encoding="utf-8") as f:
    for line in f.readlines():
        ephon, gphon = line.split("=")
        gphon = gphon.split(" ")
        audio = [(folder + a.strip() + ".mp3") for a in gphon]
        e_map[ephon] = audio


e_map[" "] = ["silence.mp3"]
#print(e_map)


# create list of files from string
files = []

# iterating through espeak string
i = 0
while i < len(phonetic):
    # multiple chars (1-3) can define a sound
    if phonetic[i:i+3] in e_map:
        files = files + e_map[phonetic[i:i+3]]
        i = i + 3
    elif phonetic[i:i+2] in e_map:
        files = files + e_map[phonetic[i:i+2]]
        i = i + 2
    elif phonetic[i:i+1] in e_map:
        files = files + e_map[phonetic[i:i+1]]
        i = i + 1
    else:
        print(phonetic[i] + ": not found", file=sys.stderr)
        i = i + 1

# Assembly of ffmpeg command
command = "ffmpeg"

for file in files:
    command = command + " -f mp3 -i " + file

command = command + " -filter_complex '"

for i in range(len(files)):
    command = command + "["+str(i)+":0]"

# Setup for export
command = command + "concat=n="+str(len(files))+":v=0:a=1[out]' -map [out] -y -loglevel warning output.mp3"

# Execute ffmpeg
os.system(command)

if os.system(command) == 0:
    print("file written to output.mp3")
    # iterating through espeak string
