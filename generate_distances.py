import landscapes as pl
import sys
import gudhi.hera
import numpy as np
import pandas as pd

VAL_DIAGRAM_FILE = './data/validation/diagrams/interpolated_x{}/{}.txt'
VAL_LANDSCAPE_FILE = './data/validation/landscapes/interpolated_x{}/{}.lan'
GEN_LANDSCAPE_FILE = './data/generators/landscapes/interpolated_x{}/{}.lan'

def load_diagram(chain, interpolation):
	return np.loadtxt(VAL_DIAGRAM_FILE.format(interpolation, chain))

def distance_matrix(items, distance, name=""):
	N = len(items)
	dm = np.zeros((N,N))
	for i in range(N):
		print(name, "row", i)
		for j in range(i):
			dm[i,j] = dm[j,i] = distance(items[i], items[j])
	return dm

def truncated_landscape_distance(landscape1, landscape2):
	diff = pl.linear_combination([landscape1, landscape2], [1,-1])
	return pl.weighted_integral(diff, [0,1] + [0] * diff.max_k())

def landscape_one_distance(landscape1, landscape2):
	return pl.distance(landscape1, landscape2, 1)

def main():

	interpolation = sys.argv[1]
	"""
	trefoil_df = pd.read_csv('trefoil_list.csv')
	trefoil_chains = trefoil_df['Chain']

	trefoil_diagrams = [load_diagram(chain, interpolation) for chain in trefoil_chains]
	wass_dm = distance_matrix(trefoil_diagrams, gudhi.hera.wasserstein_distance, "wass")
	np.savetxt("./data/validation/wass_dm_x{}.txt".format(interpolation), wass_dm)

	trefoil_landscapes = [pl.load(VAL_LANDSCAPE_FILE.format(interpolation, chain))
								 for chain in trefoil_chains]
	landscape_dm = distance_matrix(trefoil_landscapes, landscapes_one_distance, "landscape")
	np.savetxt("./data/validation/landscape_dm_x{}.txt".format(interpolation), landscape_dm)
	"""
	otcase_df = pd.read_csv('aotcase-otcase.csv')
	otcase_chains = otcase_df['Chain']

	otcase_landscapes = [pl.load(GEN_LANDSCAPE_FILE.format(interpolation, chain)) for chain in otcase_chains]
	otcase_dm = distance_matrix(otcase_landscapes, truncated_landscape_distance, "truncated") 
	np.savetxt("./data/generators/truncated_dm_x{}.txt".format(interpolation), otcase_dm)

if __name__ == "__main__":
	main()
