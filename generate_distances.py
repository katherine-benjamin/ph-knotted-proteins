import landscapes
import sys
import gudhi.hera
import numpy as np
import pandas as pd

VAL_DIAGRAM_FILE = './data/validation/diagrams/{}.txt'
VAL_LANDSCAPE_FILE = './data/validation/landscapes/{}.lan'
GEN_LANDSCAPE_FILE = './data/generators/landscapes/{}.lan'

def load_diagram(chain):
	return np.loadtxt(VAL_DIAGRAM_FILE.format(chain))

def distance_matrix(items, distance, name=""):
	N = len(items)
	dm = np.zeros((N,N))
	for i in range(N):
		print(name, "row", i)
		for j in range(i):
			dm[i,j] = dm[j,i] = distance(items[i], items[j])
	return dm

def truncated_landscape_distance(landscape1, landscape2):
	diff = landscapes.linear_combination([landscape1, landscape2], [1,-1])
	return diff.weighted_integral([0,1] + [0] * diff.max_k())

def main():

	trefoil_df = pd.read_csv('trefoil_list.csv')
	trefoil_chains = df['Chain']

	trefoil_diagrams = [load_diagram(chain) for chain in trefoil_chains]
	wass_dm = distance_matrix(trefoil_diagrams, gudhi.hera.wasserstein_distance)
	np.savetxt("./data/validation/wass_dm.txt", wass_dm, "wass")

	trefoil_landscapes = [pl.load(VAL_LANDSCAPE_FILE.format(chain)) for chain in trefoil_chains]
	landscape_dm = distance_matrix(trefoil_landscapes, landscapes.distance)
	np.savetxt("./data/validation/landscape_dm.txt", landscape_dm, "landscape")

	otcase_df = pd.read_csv('aotcase-otcase.csv')
	otcase_chains = df['Chain']

	otcase_landscapes = [pl.load(GEN_LANDSCAPE_FILE.format(chain)) for chain in otcase_chains]
	otcase_dm = distance_matrix(otcase_dm, truncated_landscape_distance) 
	np.savetxt("./data/generators/truncated_dm.txt", otcase_dm, "truncated")

if __name__ == "__main__":
	main()
