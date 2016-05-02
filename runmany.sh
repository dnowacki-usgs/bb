#!/bin/bash

for f in {1..96}; do
    folder="$(printf "run%03d" $f)"
    echo
    echo "$folder"
    echo
#    [ -d "$folder" ] && cd "$folder" && cp ../ps00001/machinefile . && cd ..
    
    
    [ -d "$folder" ] && cd "$folder" && \
         ./make_swn_bb.py --cfgfile runargs.py --outfile bb.swn && \
         #../runmodel.sh pspace && cd ..
	cd ..
done
