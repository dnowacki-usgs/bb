#!/bin/bash

for f in $(eval echo {$1..$2}); do
    folder="$(printf "run%03d" $f)"
    echo
    echo "$folder"
    echo
 
    rfolder="$(pwd)"
    
    cd $folder

    find bb.prt-001 -exec bash -c 'for f; do tac "$f" | grep -m1 accuracy; done' _ {} + > ACCURACY.txt
    cat -n ACCURACY.txt > ACCURACY_RUNNO.txt
    awk '{print $1 " " $5}' ACCURACY_RUNNO.txt > ACCURACY.txt
    rm ACCURACY_RUNNO.txt

    mv ACCURACY.txt /sand/usgs/users/dnowacki/bb/$folder/ACCURACY.txt

    cp runargs.py /sand/usgs/users/dnowacki/bb/$folder/runargs.py
   
    cd ..

    cd /sand/usgs/users/dnowacki/bb/$folder
    ~/bb/convmat2nc.py
    ~/bb/runargs2nc.py

    cd $rfolder
    # cd 
    # ./cp2clay.sh $folder
done
