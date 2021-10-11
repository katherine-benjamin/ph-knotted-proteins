import sys
import gudhi.hera
import numpy as np
import pandas as pd

BARCODE_FILE = './data/diagrams/interpolated_x{}/{}_{}.txt'

def load_barcode(chain, interpolation, dim):
	return np.loadtxt(BARCODE_FILE.format(interpolation, chain, dim))

def main():
	csv = sys.argv[1]
	interpolation = sys.argv[2]
	dim = sys.argv[3]
	output_file = sys.argv[4]
	df = pd.read_csv(csv)
	chains = df['Chain']
	barcodes = [load_barcode(chain, interpolation, dim) for chain in chains]

	N = len(chains)
	dm = np.zeros((N,N))

	for i in range(N):
		print('row {}'.format(i))
		for j in range(i):
			dm[i,j] = dm[j,i] = gudhi.hera.wasserstein_distance(barcodes[i], barcodes[j])

	np.savetxt(output_file, dm)

if __name__ == "__main__":
	main()