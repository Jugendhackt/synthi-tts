#!/bin/bash
echo processing folder $1
mkdir $1-trim

for f in $1/*; do
	ffmpeg -i $f -af "silenceremove=start_periods=1:start_duration=0.01:start_threshold=-40dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=0.01:start_threshold=-40dB:detection=peak,aformat=dblp,areverse" -y -loglevel warning $1-trim/$(basename $f)
done
