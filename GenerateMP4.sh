#!/bin/bash

for i in $(ls images/*.h264)
do echo "Processing $i ..."
avconv -framerate 4111/100 -i "$i" -vcodec copy -r 4111/100 "$i.mp4"
done
