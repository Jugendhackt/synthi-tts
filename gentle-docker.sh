#!/bin/sh

# $1 = local path to files
# $2 = audio file
# $3 = transcript

# This script fires up a docker container of gentle that exits automagically once it's done aligning stuff correctly

docker run -P -it -v $1:/gentle/output lowerquality/gentle python /gentle/align.py /gentle/output/$2 /gentle/output/$3 -o /gentle/output/output.json && exit 
