#!/bin/bash

num_files=$(ls -l ./output/prtl.tot.*  | wc -l )

echo $num_files 

# for i in $(seq 0 $num_files)
for ((i=0; i<$num_files; i++))
do
    echo $i 
    python ~/jacob_astroplasmas/TristanTools/scripts/process_jet_data.py $i
    wait
done


~/jacob_astroplasmas/TristanTools/scripts/ffmpeg_combine.sh ./plots/projections/ ./plots/projections.mp4

