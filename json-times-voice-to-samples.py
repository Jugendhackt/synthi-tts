import os
import sys
import subprocess
import json
import math

def seconds_to_ffmpeg_format(seconds):
    result = str(math.floor(seconds/3600))+":"+str(math.floor(seconds/60)%60)+":"+str(seconds%60)
    return result

jsonfile = sys.argv[1]
if not jsonfile.endswith("json"):
    jsonfile = jsonfile + ".json"
with open(jsonfile) as json_file:
    data = json.load(json_file)

for word in data['words']:
    if word['case'] != "not-found-in-audio":
        for i in range(len(word["phones"])):
            if not os.path.isfile(str(jsonfile.replace(".json", "")) + "/" + word['phones'][i]['phone'].replace("_B","").replace("_I","").replace("_E","") + ".mp3"):
                command = "ffmpeg -i "
                command = command + str(jsonfile.replace(".json", "")) 
                phone_offset = word['start']
                try:
                    for j in range(i):
                        seconds_to_ffmpeg_format(word['phones'][i]['duration'])
                        phone_offset = phone_offset + word['phones'][j]['duration']
                except IndexError:
                    phone_offset = phone_offset;
                command = command + ".mp3 -vn -acodec copy -ss " + seconds_to_ffmpeg_format(phone_offset)
                if word['phones'][i]['duration'] > 0.06:
                    command = command + " -t " + seconds_to_ffmpeg_format(word['phones'][i]['duration'])
                else:
                    command = command + " -t " + seconds_to_ffmpeg_format(0.06)
                command = command + " " + str(jsonfile.replace(".json", "")) + "/" + word['phones'][i]['phone'].replace("_B","").replace("_I","").replace("_E","") + ".mp3"
                if "_I" in word['phones'][i]['phone']:
                    command = command + " -n -loglevel panic"
                else:
                    command = command + " -y -loglevel panic"
                os.system(command)
        print("currently at " + seconds_to_ffmpeg_format(word['start']) + " from " + seconds_to_ffmpeg_format(data['words'][-1]['end']))