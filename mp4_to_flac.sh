#!/bin/bash

# Converts an mp4 file to flac audio as desired in the online course.

# if the .flac file already exists, then remove it before converting
FILE_PATH=morning.flac
if test -f $FILE_PATH; then
    rm -rf $FILE_PATH
fi

# first, use ffmpeg to convert the .mp4 to .wav
ffmpeg -i morning.mp4 morning.wav

# then, use sox to convert the .wav to .flac
sox morning.wav $FILE_PATH

# remove the intermediate .wav file
rm morning.wav