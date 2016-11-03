#!/bin/bash

tail -f $(printf "run%03d/PRINT-001" $1)
