import os
import sys
import numpy as np
import landscapes as pl

def main():
    diagram_directory = sys.argv[1]
    landscape_directory = sys.argv[2]
    for filename in os.listdir(diagram_directory):
        try:
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
        except:
            pass

if __name__ == "__main__":
    main()
