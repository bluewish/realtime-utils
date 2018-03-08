#!/bin/bash

tmpfile=$(mktemp /tmp/cycl_test.XXXXXX)
cyclictest -l 1000 -m -S -p99 -h 400 > ${tmpfile}
python cycl_plot.py -f ${tmpfile}
rm ${tmpfile}