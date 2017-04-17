#!/usr/bin/env python

# A script to plot optical measurements of tissue phantoms.
# Takes 980 nm transmission data vs. sample thickness and generates a scatter
# plot from the averages of the trials for each sample, as well as error bars
# that represent a range of one standard deviation (pos. and neg.).

# Written by Alex Cochran, 2017.

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# define data file from executable command input
filename = sys.argv[1]

# generate plot label & plot filename: "[sample type] mm/dd/yyyy"
label = raw_input("Plot label: ")
file_label = label.replace(" ", "_")

# read data from file
data = np.genfromtxt(filename, delimiter = ',')

# testing environment
raw = float(raw_input("Raw source power [mW]: "))           # raw source power [mW]
amb = float(raw_input("Signal from ambient light [mW]: "))  # power measured from ambient light [mW]

# extract thickness and intensity values
thick   = data[:,][:,0]                         # [mm]
mW      = data[:,][:,1:]                        # [mW]
trans   = ((mW - amb) / (raw - amb)) * 100.0    # [%]

# average transmission; (1) computes for each element rather than the array as a whole (axis choice)
trans_avg   = np.array(trans).mean(1)

# compute stdev values for error bars; (1): same idea as the average calculation
trans_stdev = np.array(trans).std(1)
yerr = np.transpose(trans_stdev)

# plot transmission date
plt.figure(1)
plt.errorbar(thick, trans_avg, yerr = yerr, fmt = 'b.')
plt.title('980 nm Optical Transmission: %s' %(label))
plt.xlabel('Thickness [mm]')
plt.ylabel('Transmission [%]')
plt.rcParams['legend.numpoints'] = 1 # set number of markers in legend to 1
plt.legend(['%s' %(label)])
plt.savefig('plots/%s.png' %(file_label))
plt.show()
