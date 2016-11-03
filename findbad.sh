#!/bin/bash

find run* -type d '!' -exec test -e "{}/bb.prt-001" ';' -print | while read line; do
    echo "Resubmitting run ${line: -3}"
    ./submany.sh ${line: -3} ${line: -3}
done
   
