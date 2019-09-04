#!/bin/bash

ffmpeg -r 4 -i "$1"%03d.png -vcodec mpeg4 -y $2
