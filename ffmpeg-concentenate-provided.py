import os
import subprocess
import argparse
import fileinput

parser = argparse.ArgumentParser(description='concentenate all provided files together.\nonly supports mp3 currently')

parser.add_argument('files', metavar='V', type=str, nargs='+')

args = parser.parse_args()

ipa = ""
if len(args.files) != 0:
    ipa = args.files
else:
    ipa = fileinput.input()[0].strip()
    ipa = ipa.split(" ")

print(ipa)

files = []
for file in ipa:
    files.append(file)

command = "ffmpeg"

for file in files:
    command = command + " -i " + file

command = command + " -filter_complex '"

for i in range(len(files)):
    command = command + "["+str(i)+":0]"
command = command + "concat=n="+str(len(files))+":v=0:a=1[out]' -map [out] output.mp3"

os.system(command)

print(args.files)
