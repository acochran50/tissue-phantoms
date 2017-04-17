# Tissue Phantoms
Alex Cochran, 2017.

This repository contains code dedicated to data processing for 980 nm transmission tests of PDMS tissue phantoms. This work is done as part of Alex Cochran's senior design project for the Materials Science & Engineering Undergraduate Program at the Ohio State University.

The files in this repository are simple scripts used to manage data collected during optical characterization testing of the tissue phantoms. They rely on a command-line interface for simplicity. More files will be added as needed.

## Scripts

### PhantomPlotter
The PhantomPlotter script is a short Python program used to plot 980 nm transmission data versus tissue phantom sample thickness. The data files used with this script should be formatted as CSV files, with thickness [mm] in the first column with the corresponding transmission [mW] data in the columns following. The command to run PhantomPlotter is: `python PhantomPlotter.py [data path]` where `[data path]` is the path to the data the user wishes to plot. Several prompts will then appear, asking the user for input on the desired plot label and testing parameters for the 980 nm source (raw source power & ambient light power).

## LICENSE
This repository and the files within it are licensed using the MIT License.
