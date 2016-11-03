#!/bin/bash

for f in $(eval echo {$1..$2}); do
    folder="$(printf "run%03d" $f)"
    echo
    echo "$folder"
    echo
#    [ -d "$folder" ] && cd "$folder" && cp ../ps00001/machinefile . && cd ..
    
    
    [ -d "$folder" ] && cd "$folder" && \
         rm -f *-0* *.nc *.mat && \
         ../make_swn_bb.py --cfgfile runargs.py --outfile bb.swn && \
         cp ../run.sh $folder.sh && \
         qsub $folder.sh && \
	cd ..
    sleep 0.1
done
