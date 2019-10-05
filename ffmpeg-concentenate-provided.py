import os
import sys
import subprocess
import fileinput

ipa = ""
if len(sys.argv) > 1:
    ipa = sys.argv[1]
else:
    ipa = fileinput.input()[0].strip()

ipa = ipa.split(" ")

files = []
for file in ipa:
    files.append(file)

command = "ffmpeg"

for file in files:
    command = command + " -i " + file

command = command + " -filter_complex '"

for i in range(len(files)):
    command = command + "["+str(i)+":0]"
command = command + "concat=n="+str(len(files))+":v=0:a=1[out]' -map [out] -loglevel panic output.mp3"

try:
    os.remove("output.mp3")
except OSError:
    pass
os.system(command)

print(command)
