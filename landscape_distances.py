import landscapes as pl
import sys
import numpy as np
import pandas as pd

LANDSCAPE_FILE = './data/landscapes/interpolated_x{}/{}_{}.lan'

def load_landscape(chain, interpolation, dim):
	return pl.load(LANDSCAPE_FILE.format(interpolation, chain, dim))

def main():
	csv = sys.argv[1]
	interpolation = sys.argv[2]
	dim = sys.argv[3]
	output_file = sys.argv[4]
	df = pd.read_csv(csv)
	chains = df['Chain']
	landscapes = [load_landscape(chain, interpolation, dim) for chain in chains]

	N = len(chains)
	dm = np.zeros((N,N))

	for i in range(N):
		print("row {}".format(i))
		for j in range(i):
			dm[i,j] = dm[j,i] = pl.distance(landscapes[i], landscapes[j], 1)

	np.savetxt(output_file, dm)

if __name__ == "__main__":
	main()