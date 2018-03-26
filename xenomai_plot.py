#!/usr/bin/python

import sys, os
import optparse
import matplotlib.pyplot as plt

def process_cmd():
    parser = optparse.OptionParser(description="Process the result of xenomai")
    parser.add_option("-f", "--file", dest='result_file', default="")
    opts, args = parser.parse_args()
    if not os.path.exists(opts.result_file):
        parser.print_help()
        sys.exit(-1)
    return os.path.realpath(opts.result_file)

def process_output(result_file):
    hist_data = []
    avg = 0
    count = 0
    min = 0
    max = 0
    with open(result_file) as f:
        for line in f.readlines():
            if len(line.strip()) == 0:
                continue
            if line.startswith("#"):
                continue
            lat_value = float(line.strip().split()[0])
            if min == 0:
                min = lat_value
            if lat_value > max:
                max = lat_value
            lat_count = int(line.strip().split()[1])
            avg += lat_value * lat_count
            count += lat_count
            hist_data.append((lat_value, lat_count))
        avg = float(avg / count)
    return hist_data, min, max, avg

def draw_figure(hist_data, min, max, avg):
    color_table=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    cpu_count = 0
    lat_avg = 0
    lat_max = 0
    lat_min = 0

    x = [item[0] for item in hist_data]
    y = [item[1] for item in hist_data]
    fig = plt.plot(x, y, 'r*',
                       label="avg=%f,min=%f,max=%d" % (avg, min, max))

    plt.legend()
    plt.ylabel("Number of Samples")
    plt.xlabel("Latency (us)")
    plt.show()

if __name__ == "__main__":
    #process_output(sys.argv[1])
    hist, min, max, avg = process_output(process_cmd())
    draw_figure(hist, min, max, avg)