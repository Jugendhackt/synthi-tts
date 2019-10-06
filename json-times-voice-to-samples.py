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

if not os.path.exists(jsonfile):
    print("file " + jsonfile + " doesn't exist! aborting...", file=sys.stderr)
    sys.exit()

folder = str(sys.argv[2]) if len(sys.argv) > 2 else ""
if not folder.strip():
    folder = str(os.path.splitext(jsonfile)[0])
print("writing to folder " + folder)

with open(jsonfile) as json_file:
    data = json.load(json_file)

try:
    os.mkdir(folder)
except FileExistsError:
    #the folder already existsif not jsonfile.endswith("json"):
    pass


#decide which phoneme to use
# Loop through each word of the transcript
phoneme_map = {}
for word in data['words']:
    # Word has to be in the audio file
    if word['case'] != "not-found-in-audio":
        # Iterates phonemes
        for i in range(len(word["phones"])):
            try:
                phoneme_map[word['phones'][i]['phone']].append(word['phones'][i]['duration'])
            except KeyError:
                phoneme_map[word['phones'][i]['phone']] = [word['phones'][i]['duration']]

 #iterates over the phonomes, and replaces the list of all durations with the average duration               
for phonome in phoneme_map:
    sum_of_all_durations = 0
    for value in phoneme_map[phonome]:
        sum_of_all_durations += float(value)
    average = sum_of_all_durations / len(phoneme_map[phonome])
    phoneme_map[phonome] = average


# Loop through each word of the transcript
for word in data['words']:
    # Word has to be in the audio file
    if word['case'] != "not-found-in-audio":
        # Iterates phonemes
        for i in range(len(word["phones"])):
            # Check whether phoneme already exists as saved file
            if os.path.isfile(str(jsonfile.replace(".json", "")) + "/" + word['phones'][i]['phone'].replace("_B","").replace("_I","").replace("_E","") + ".mp3"):
                print("skipping " + word['phones'][i]['phone'].split("_", 1)[0] + " because it exists")
            else:
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
                    print("overriding " + word['phones'][i]['phone'])
                    command = command + " -n -loglevel warning"
                else:
                    print("processing " + word['phones'][i]['phone'])
                    command = command + " -y -loglevel warning"
                # Execute ffmpeg
                os.system(command)
    
        # Progress/status
        print("currently at " + seconds_to_ffmpeg_format(word['start']) + " from " + seconds_to_ffmpeg_format(data['words'][-1]['end']))
