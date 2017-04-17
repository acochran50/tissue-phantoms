#!/usr/bin/env python

#-------------------------------------------------------------------------------
# MIT License

# Copyright (c) 2017 Alex Cochran

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#-------------------------------------------------------------------------------

# PhantomPlotter is a script to plot optical measurements of tissue phantoms.
# Takes 980 nm transmission data vs. sample thickness and generates a scatter
# plot from the averages of the trials for each sample, as well as error bars
# that represent a range of one standard deviation (pos. and neg.).

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time

# define data file from executable command input
filename = sys.argv[1]

# generate plot label & plot filename: "[sample type] mm/dd/yyyy"
testname = raw_input("Plot label: ")
file_label = testname.replace(" ", "_")

# if the directory the plot & data will be sent to does not exist, create it
script_dir = os.path.dirname(__file__)
output_dir = os.path.join(script_dir, 'output/{0}'.format(file_label))

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

# read data from file
data = np.genfromtxt(filename, delimiter = ',')

# testing environment
raw = float(raw_input("Raw source power [mW]: "))           # raw source power [mW]
amb = float(raw_input("Signal from ambient light [mW]: "))  # power measured from ambient light [mW]

# extract thickness and intensity values
thick   = data[:,][:,0]                         # [mm]
sig     = data[:,][:,1:]                        # [mW]
trans   = ((sig - amb) / (raw - amb)) * 100.0   # [%]

# average transmission; (1) computes for each element rather than the array as a whole (axis choice)
trans_avg   = np.array(trans).mean(1)

# compute stdev values for error bars; (1): same idea as the average calculation
trans_stdev = np.array(trans).std(1)
yerr = np.transpose(trans_stdev)

# concatenate arrays for output (stack columns)
trans_out = np.column_stack((thick, trans))
avg_out = np.column_stack((thick, trans_avg))

# produce output file with data + calculations
output_file = open('{0}/{1}.out'.format(output_dir,file_label), "w")
output_file.write("980 nm Optical Transmission: {0}\n{1}\n".format(testname, time.strftime("%m/%d/%y %H:%M:%S")))
output_file.write("\nRaw source power: {0} [mW]".format(raw))
output_file.write("\nAmbient signal: {0} [mW]\n".format(amb))
output_file.write("\nThickness [mm]\tTransmission [%]\n")
np.savetxt(output_file, trans_out, fmt='%.4e')
output_file.write("\nThickness [mm]\tAvg. Transmission [%]\n")
np.savetxt(output_file, avg_out, fmt='%.4e')
output_file.close()

# plot transmission data
plt.figure(1)
plt.errorbar(thick, trans_avg, yerr = yerr, fmt = 'b.')
plt.title("980 nm Optical Transmission: {0}\n{1}".format(testname, time.strftime("%m/%d/%y")))
plt.xlabel('Thickness [mm]')
plt.ylabel('Transmission [%]')
plt.rcParams['legend.numpoints'] = 1 # set number of markers in legend to 1
plt.legend('{0}'.format(testname))
plt.savefig('{0}/{1}.png'.format(output_dir, file_label))
plt.show()
