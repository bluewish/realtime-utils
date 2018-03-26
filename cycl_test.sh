#!/bin/bash

mkdir -p report
file_name=$(date "+%y_%m_%d_%H_%M_%S")
cyclictest -D 1m -m -S -p99 -h 100 > report/${file_name}
python cycl_plot.py -f report/${file_name}
