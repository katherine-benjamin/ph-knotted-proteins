import sys
import sklearn.manifold
import numpy as np

def isomap(distance_matrix):
    model = sklearn.manifold.Isomap(metric="precomputed", n_components=2)
    embedding = model.fit_transform(distance_matrix)
    return embedding

def main():
	input_dm = sys.argv[1]
	output = sys.argv[2]

	embedding = isomap(np.loadtxt(input_dm))
	np.savetxt(output, embedding)

if __name__ == '__main__':
	main()