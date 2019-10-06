#!/usr/bin/python3

from subprocess import Popen, PIPE
import sys
import os
import argparse

#using argparse to get the information about language, folder and text from CLI
parser = argparse.ArgumentParser("synthi-tts <text>")
parser.add_argument('text', metavar='<text>', type=str, nargs='*', help='the text the program has to pronounce.')
parser.add_argument('-f', dest='folder', action='store', help='the folder from which the program loads the phonemes.')
parser.add_argument('-l', dest='language', action='store', default='english', help='the language the program uses to determine the pronounciation.\nDefault: english')
parser.add_argument('--no_warnings', dest='missing_phonemes_print', action='store_true', default=False, help="use this flag if you don't want to see messages telling you which parts of the phenatics the program does'nt know.")


# Getting folder and files from CLI
args = parser.parse_args()
text = ' '.join(args.text)
print(text)
# Getting language from espeak
process = Popen(['espeak', '-q', '-x', '"' + text + '"', '-v', args.language.lower()], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
phonetic = stdout.decode('utf-8').strip()[5:].replace("'", "").replace("_:", "")
print(phonetic)

# create e_map from espeak-gentle translation
e_map = {}

with open("espeak-to-gentle", encoding="utf-8") as f:
    for line in f.readlines():
        ephon, gphon = line.split("=")
        gphon = gphon.split(" ")
        audiofiles = [(str(args.folder) + '/' + a.strip() + ".mp3") for a in gphon]
        for audiofile in audiofiles:
            if not os.path.exists(audiofile):
                audiofiles.remove(audiofile)
                if not args.missing_phonemes_print:
                    print("phoneme " + ephon + ": file not found: " + audiofile, file=sys.stderr)
        if audiofiles:
            e_map[ephon] = audiofiles


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
        if not args.missing_phonemes_print:
            print(phonetic[i] + ": not defined. skipping", file=sys.stderr)
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
    print("file successfully written to output.mp3")
    # iterating through espeak string
