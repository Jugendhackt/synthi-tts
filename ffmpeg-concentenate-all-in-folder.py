import os
import subprocess

path = os.path.dirname(os.path.realpath(__file__))
path = path + "/"

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.mp3' in file and "output.mp3" not in file:
            files.append(os.path.join(r, file))


command = "ffmpeg"

for file in files:
    command = command + " -i " + file

command = command + " -filter_complex '"

for i in range(len(files)):
    command = command + "["+str(i)+":0]"
command = command + "concat=n="+str(len(files))+":v=0:a=1[out]' -map [out] output.mp3"

os.system(command)