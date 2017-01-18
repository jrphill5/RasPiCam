#!/bin/bash

for i in $(ls images/*.h264)
do echo "Processing $i ..."
avconv -framerate 41 -i "$i" -vcodec copy -r 41 "$i.mp4"
done
