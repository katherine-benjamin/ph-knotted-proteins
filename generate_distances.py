import landscapes as pl
import sys
import gudhi.hera
import numpy as np
import pandas as pd

DIAGRAM_PREF = './data/validation/diagrams/interpolated_x{}/noise_v{}/{}_1.txt'
LANDSCAPE_PREF = './data/validation/landscapes/interpolated_x{}/'
GEN_LANDSCAPE_PREF = './data/generators/landscapes/interpolated_x{}/'

def load_diagram(chain, interpolation, noise):
	pref = DIAGRAM_PREF
	if noise != 0:
		pref += "noise_v{}/".format(noise)
	pref += "{}_1.txt"
	return np.loadtxt(pref.format(interpolation, chain))

def load_landscape(chain, interpolation, noise):
	pref = LANDSCAPE_PREF
	if noise != 0:
		pref += "noise_v{}/".format(noise)
	pref += "{}_1.lan"
	return pl.load(pref.format(interpolation, chain))

def load_gen_landscape(chain, interpolation, noise):
	pref = GEN_LANDSCAPE_PREF
	if noise != 0:
		pref += "noise_v{}/".format(noise)
	pref += "{}.lan"
	return pl.load(pref.format(interpolation, chain))

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
	if len(sys.argv) > 2:
		noise = sys.argv[2]
	else:
		noise = 0

	suffix = "_x{}".format(interpolation) + ("_v{}".format(noise) if noise != 0 else "")

	trefoil_df = pd.read_csv('trefoil_list.csv')
	trefoil_chains = trefoil_df['Chain']

	trefoil_diagrams = [load_diagram(chain, interpolation, noise) for chain in trefoil_chains]
	wass_dm = distance_matrix(trefoil_diagrams, gudhi.hera.wasserstein_distance, "wass")
	np.savetxt("./data/validation/wass_dm{}.txt".format(suffix), wass_dm)
	
	trefoil_landscapes = [load_landscape(chain, interpolation, noise) for chain in trefoil_chains]
	landscape_dm = distance_matrix(trefoil_landscapes, landscape_one_distance, "landscape")
	np.savetxt("./data/validation/landscape_dm{}.txt".format(suffix), landscape_dm)
	
	otcase_df = pd.read_csv('aotcase-otcase.csv')
	otcase_chains = otcase_df['Chain']

	otcase_landscapes = [load_gen_landscape(chain, interpolation, noise) for chain in otcase_chains]
	otcase_dm = distance_matrix(otcase_landscapes, truncated_landscape_distance, "truncated") 
	np.savetxt("./data/generators/truncated_dm{}.txt".format(suffix), otcase_dm)

if __name__ == "__main__":
	main()
