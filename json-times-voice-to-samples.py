import os
import sys
import subprocess
import json
import math
import statistics

# Converts seconds to timestamp string
def seconds_to_ffmpeg_format(seconds):
    result = str(math.floor(seconds/3600))+":"+str(math.floor(seconds/60)%60)+":"+str(seconds%60)
    return result


def create_ffmpeg_command(folder_name, word, phone_index):
    command = "ffmpeg -i "
    command = command + folder_name 
    phone_offset = word['start']
    for j in range(phone_index):
        phone_offset += word['phones'][j]['duration']
    # Continue assembly of command
    # Beginning
    command = command + ".mp3 -vn -acodec mp3 -ss " + seconds_to_ffmpeg_format(phone_offset)
    command = command + " -t " + seconds_to_ffmpeg_format(word['phones'][i]['duration'])

    file_name = folder_name + "/" + word['phones'][phone_index]['phone'].replace("_B","").replace("_I","").replace("_E","") + "/"

    try:
        os.mkdir(file_name)
    except FileExistsError:
        pass
    #create incrementing numerical names
    name_found = False
    numerical_extension = 0;
    while not name_found:
        if not os.path.isfile(file_name + str(numerical_extension) + '.mp3'):
            file_name += str(numerical_extension) + '.mp3 -loglevel warning -y'
            name_found = True
        numerical_extension += 1

    # Adding name of the phoneme extract
    command = command + " " + file_name
    print(command)
    return command


# Get the name of the gentle output file from CLI
jsonfile = sys.argv[1]
if not jsonfile.endswith("json"):
    jsonfile = jsonfile + ".json"
with open(jsonfile) as json_file:
    data = json.load(json_file)

try:
    os.mkdir(jsonfile.replace('.json',''))
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
    print(phoneme_map[phonome])
    try:
        standart_deviation = statistics.stdev(phoneme_map[phonome])
    except statistics.StatisticsError:
        standart_deviation = 0.1
    phoneme_map[phonome] = [average, standart_deviation]


# Loop through each word of the transcript
for word in data['words']:
    # Word has to be in the audio file
    if word['case'] != "not-found-in-audio":
        # Iterates phonemes
        for i in range(len(word["phones"])):
            # Check whether phoneme already exists as saved file
            # assemble ffmpeg command and execute it
            if word['phones'][i]['duration'] >= phoneme_map[word['phones'][i]['phone']][0] - phoneme_map[word['phones'][i]['phone']][1] and\
               word['phones'][i]['duration'] <= phoneme_map[word['phones'][i]['phone']][0] + phoneme_map[word['phones'][i]['phone']][1]:
                os.system(create_ffmpeg_command(jsonfile.replace(".json",""), word, i))
    
        # Progress/status
        print("currently at " + seconds_to_ffmpeg_format(word['start']) + " from " + seconds_to_ffmpeg_format(data['words'][-1]['end']))
