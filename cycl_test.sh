#!/bin/bash

mkdir -p report
file_name=$(date "+%y_%m_%d_%H_%M_%S")
rdmsr 0x34 > report/${file_name}
cyclictest -D 30m -m -p99 -S -h 100 >> report/${file_name}
rdmsr 0x34 >> report/${file_name}
python cycl_plot.py -f report/${file_name}

