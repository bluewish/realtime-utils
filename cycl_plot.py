#!/usr/bin/python

import sys, os
import optparse
import matplotlib.pyplot as plt

def process_cmd():
    parser = optparse.OptionParser(description="Process the result of cyclictest")
    parser.add_option("-f", "--file", dest='result_file', default="")
    opts, args = parser.parse_args()
    if not os.path.exists(opts.result_file):
        parser.print_help()
        sys.exit(-1)
    return os.path.realpath(opts.result_file)

def process_output(result_file):
    with open(result_file) as f:
        found_hist = False
        hist_data = {}
        lat_count = 0
        max_lat = []
        min_lat = []
        avg_lat = []
        for line in f.readlines():
            if line.strip().lower() == "# histogram":
                found_hist = True
                continue
            if line.strip().lower().startswith("# total:"):
                found_hist = False
                continue
            if found_hist:
                temp_data = line.strip().split()
                cpu_num = len(temp_data) - 1
                lat_value = int(temp_data[0])
                for x in xrange(1, cpu_num):
                    lat_count = int(temp_data[x])
                    if lat_count != 0:
                        if not hist_data.has_key(x):
                            hist_data[x] = []
                        hist_data[x].append((lat_value, lat_count))
            if line.strip().lower().startswith("# min latencies"):
                min_lat = line.split(":")[1].split()
            if line.strip().lower().startswith("# avg latencies"):
                avg_lat = line.split(":")[1].split()
            if line.strip().lower().startswith("# max latencies"):
                max_lat = line.split(":")[1].split()

    return hist_data, min_lat, max_lat, avg_lat

def draw_figure(hist_data, min, max, avg):
    print hist_data[1]
    color_table=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    for cpu_no in hist_data.keys():
        x = [item[0] for item in hist_data[cpu_no]]
        y = [item[1] for item in hist_data[cpu_no]]
        fig = plt.plot(x, y, color_table[cpu_no]+'*',
                       label="cpu[%s]:avg=%d,min=%d,max=%d" % (cpu_no, int(avg[cpu_no-1]), int(min[cpu_no-1]), int(max[cpu_no-1])))
    plt.legend()
    plt.show()

if __name__ == "__main__":
    #process_output(sys.argv[1])
    hist, min, max, avg = process_output(process_cmd())
    draw_figure(hist, min, max, avg)