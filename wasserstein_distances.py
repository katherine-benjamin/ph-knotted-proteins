import sys
import gudhi.hera
import numpy as np
import pandas as pd

BARCODE_FILE = './data/diagrams/{}_1.txt'

def load_barcode(chain):
	return np.loadtxt(BARCODE_FILE.format(chain))

def main():
	csv = sys.argv[1]
	output_file = sys.argv[2]
	df = pd.read_csv(csv)
	chains = df['Chain']
	barcodes = [load_barcode(chain) for chain in chains]

	N = len(chains)
	dm = np.zeros((N,N))

	for i in range(N):
		print('row {}'.format(i))
		for j in range(i):
			dm[i,j] = dm[j,i] = gudhi.hera.wasserstein_distance(barcodes[i], barcodes[j])

	np.savetxt(output_file, dm)

if __name__ == "__main__":
	main()
