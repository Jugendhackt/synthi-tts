import os
import subprocess
import json
import math

def seconds_to_ffmpeg_format(seconds):
    result = str(math.floor(seconds/3600))+":"+str(math.floor(seconds/60)%60)+":"+str(seconds%60)
    return result
path = os.path.dirname(os.path.realpath(__file__))
path = path + "/"

for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            jsonfile = file


with open(jsonfile) as json_file:
    data = json.load(json_file)

for word in data['words']:
    for i in range(len(word["phones"])):
        command = "ffmpeg -i "
        command = command + str(jsonfile.replace("-data.json", "")) 
        phone_offset = word['start']
        try:
            for j in range(i):
                phone_offset = phone_offset + word['phones'][j]['duration']
        except IndexError:
            phone_offset = phone_offset;
        command = command + ".mp3 -vn -acodec copy -ss " + seconds_to_ffmpeg_format(phone_offset)
        command = command + " -t " + seconds_to_ffmpeg_format(word['phones'][i]['duration'])
        command = command + " " + str(jsonfile.replace("-data.json", "")) + "/" + word['phones'][i]['phone'].replace("_B","").replace("_I","").replace("_E","") + ".mp3"
        if "_I" in word['phones'][i]['phone']:
            command = command + " -loglevel panic"
        else:
            command = command + " -y -loglevel panic"
        print(command)
        os.system(command)