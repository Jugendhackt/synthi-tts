import os
import sys
import subprocess
import json
import math

# Converts seconds to timestamp string
def seconds_to_ffmpeg_format(seconds):
    result = str(math.floor(seconds/3600))+":"+str(math.floor(seconds/60)%60)+":"+str(seconds%60)
    return result


# Get the name of the gentle output file from CLI
jsonfile = sys.argv[1]
if not jsonfile.endswith("json"):
    jsonfile = jsonfile + ".json"
with open(jsonfile) as json_file:
    data = json.load(json_file)

# Loop through each word of the transcript
for word in data['words']:
    # Word has to be in the audio file
    if word['case'] != "not-found-in-audio":
        # Iterates phonemes
        for i in range(len(word["phones"])):
            # Check whether phoneme already exists as saved file
            if not os.path.isfile(str(jsonfile.replace(".json", "")) + "/" + word['phones'][i]['phone'].replace("_B","").replace("_I","").replace("_E","") + ".mp3"):
                # assemble ffmpeg command
                command = "ffmpeg -i "
                command = command + str(jsonfile.replace(".json", "")) 

                phone_offset = word['start']
                for j in range(i):
                    phone_offset += word['phones'][j]['duration']

                # Continue assembly of command
                # Beginning
                command = command + ".mp3 -vn -acodec mp3 -ss " + seconds_to_ffmpeg_format(phone_offset)
                command = command + " -t " + seconds_to_ffmpeg_format(word['phones'][i]['duration'])
                
                # Adding name of the phoneme extract
                command = command + " " + str(jsonfile.replace(".json", "")) + "/" + word['phones'][i]['phone'].replace("_B","").replace("_I","").replace("_E","") + ".mp3"

                # Prefer inner phonemes
                if "_I" in word['phones'][i]['phone']:
                    command = command + " -n -loglevel panic"
                else:
                    command = command + " -y -loglevel panic"
                # Execute ffmpeg
                os.system(command)
    
        # Progress/status
        print("currently at " + seconds_to_ffmpeg_format(word['start']) + " from " + seconds_to_ffmpeg_format(data['words'][-1]['end']))
