#!/bin/bash

find run*/bb.prt-001 -exec bash -c 'for f; do tac "$f" | grep -m1 accuracy; done' _ {} + > ACCURACY.txt
cat -n ACCURACY.txt > ACCURACY_RUNNO.txt
awk '{print $1 " " $5}' ACCURACY_RUNNO.txt > ACCURACY.txt
rm ACCURACY_RUNNO.txt
