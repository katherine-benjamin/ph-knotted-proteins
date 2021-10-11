import os
import numpy as np
import landscapes as pl

diagram_directory = './data/diagrams/interpolated_x6/'
landscape_directory = './data/landscapes/interpolated_x6/'

for filename in os.listdir(diagram_directory):
    print(filename)
    root, _ = filename.split('.')
    ls_filename = landscape_directory + root + '.lan'
    if not os.path.isfile(ls_filename):
        print("Computing...")
        barcode = np.loadtxt(diagram_directory + filename)
        landscape = pl.generate_landscape(barcode.tolist())
        landscape.save(ls_filename)
    else:
        print("Done!")