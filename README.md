# ph-knotted-proteins

This repository is a companion to the paper:

It contains the data analysed in the paper, as well as the Python code used to generate those data and to produce the accompanying figures.

## Dependencies

Almost all of the code in this repository depends on [Numpy](https://numpy.org) and [Pandas](https://pandas.pydata.org).

Computing Wasserstein distances requires [GUDHI](https://gudhi.inria.fr).

Computing Isomap embeddings requires [scikit-learn](https://scikit-learn.org/stable/).

Generating almost all of the figures requires both [matplotlib](https://matplotlib.org) and [seaborn](https://seaborn.pydata.org).

Plotting generators for homology requires [Plotly](https://plotly.com).

## Pipeline

Beginning from protein coordinate data obtained from KnotProt and the PDB, the computational pipeline applied in the paper is as follows.

1. For each protein chain, add five linearly interpolated points between each successive pair of alpha carbon coordinates.
2. Compute first persistent homology of the Vietoris-Rips complexes associated to these interpolated chains:

    a) For trefoil-knotted chains (listed in `trefoil_list.csv`), generate persistence diagrams with [Ripser](https://github.com/Ripser/ripser).
    
    b) For AOTCase and OTCase chains (listed in `aotcase-otcase.csv`), generate both persistence diagrams and corresponding representative homology generators with [Eirene](https://github.com/Eetion/Eirene.jl).
    
3. Compute persistence landscapes from these persistence diagrams.
4. Compute distance matrices on trefoil-knotted chains using Wasserstein and landscape distances, and generate two-dimensional Isomap embeddings from these.
5. Perform statistical tests on landscapes corresponding to trefoil-knotted proteins.

Steps 1 and 2 are standard, and we include their output. This repository contains the code required to complete the remaining steps.

## Data

The repository contains four types of data. They are stored in the `data` subdirectory.

### Point clouds

Coordinates for protein chains are stored as `.xyz` files in `./data/chains/`. For example, the coordinates of the 3KZK_A chain are stored in `./data/chains/3kzk_A.xyz`.

Interpolated chains are stored in the `./data/chains/interpolated_x6/` subdirectory. For example, the file `./data/chains/interpolated_x6/3kzk_A_x6.xyz` is the result of adding 5 equidistant, linearly interpolated points between each successive pair of coordinates in `./data/chains/3kzk_A.xyz`.

### Persistence diagrams

We make a distinction between diagrams used for statistical analysis (generated with Ripser), and those used to study representatives (generated with Eirene). These correspond to the two main subsections in the results section of the paper.

The former are stored in `./data/validation/diagrams/`. For example, the degree-one persistence diagram corresponding to the 3KZK_A chain is stored in `./data/validation/diagrams/3kzk_A.txt`.

The latter are stored in `./data/generators/diagrams/`. For example, the diagram corresponding to 3KZK_A is stored in `./data/generators/diagrams/3kzk_A.txt`. We note that the only difference between these two diagrams is the order in which the features are presented.

For the latter case, we also store representative generators for homology classes as output by Eirene. These may be found in `./data/generators/reps/`. For example, the representative generator for the 13th feature of the 3KZK_A diagram is stored in `.data/generators/reps/3kzk_A_representative_13.txt`.

### Persistence landscapes

Landscapes are stored in the `.lan` format specified in [the paper of Bubenik and Dłotko](https://www.sciencedirect.com/science/article/pii/S0747717116300104). They are therefore compatible with [The Persistence Landscape Toolbox](https://www2.math.upenn.edu/~dlotko/persistenceLandscape.html).

We again make a distinction between the two sections.

Landscapes for the first section are stored in `./data/validation/landscapes/`. For example, the landscape corresponding to the persistence diagram for 3KZK_A is stored in `./data/validation/landscapes/3kzk_A.lan`.

Landscapes for the second section are stored in `./data/generators/landscapes/`. Here, the landscape corresponding to the persistence diagram for 3KZK_A may be found in `./data/generators/landscapes/3kzk_A.lan`.

### Distance matrices

We have precomputed all three distance matrices used in our analysis. For the validation section, the Wasserstein distance matrix is stored in `./data/validation/wass_dm.txt` and the landscape distance matrix is stored in `./data/validation/landscape_dm.txt`. For the generators section, the distance matrix is stored in `./data/generators/truncated_dm.txt`.

## Usage

### Persistence landscapes

This repository contains a (slightly modified) version of the [Pysistence Landscapes package](https://gitlab.com/kfbenjamin/pysistence-landscapes) maintained by one of the authors. This can be found in the file `landscapes.py` in the root directory. We use this both to generate landscapes from diagrams, and later on to perform analysis and generate figures.

To generate landscapes, we provide the script `generate_landscapes.py`. This takes as arguments an input directory and an output directory. Then, for each persistence diagram in the input directory (and we assume that the input directory contains only persistence diagrams), it produces a corresponding persistence landscape, and saves it in the output directory.

To complete Step 3 from the above pipeline, then, requires two very similar commands:

```
python generate_landscapes.py ./data/validation/diagrams/ ./data/validation/landscapes/
python generate_landscapes.py ./data/generators/diagrams/ ./data/generators/landscapes/
```

### Distance matrices and embeddings

For Step 4 we provide a script, `generate_distances.py`, which will output the three distance matrices we use in the paper. For the first distance matrix, computed on persistence diagrams, it requires [GUDHI](https://gudhi.inria.fr). If one of these distances is not required, for instance because the user only wishes to work with one subsection of the paper, then the relevant lines are easily removed from the script.

The Isomap embeddings can then be computed with the `generate_isomap.py` script. This depends on [scikit-learn](https://scikit-learn.org/stable/). Generating both isomap embeddings requires two commands:

```
python generate_isomap.py ./data/validation/wass_dm.txt ./data/validation/wass_iso.txt
python generate_isomap.py ./data/validation/landscape_dm.txt ./data/validation/landscape_iso.txt
```

### Statistical tests

In the paper, we run permutation tests to detect differences between sequence homology clusters of trefoil-knotted proteins. We provide the `permutation_test.py` script to facilitate this. It takes as input the representatives of two sequence homology clusters, as well as a number of repetitions, and outputs an approximate p-value.

For example, to compare the 3ZNC and 6RQQ clusters with 10000 samples (as we do in the paper), one would run

```
python permutation_test.py 3ZNC 6RQQ 10000
```
and, after a while, a p-value will be returned.

### Generators

We provide a notebook `Plot generators.ipynb` to allow for representative generators for homology of AOTCase and OTCase chains to be plotted interactively. It depends on [Plotly](https://plotly.com).

### Figures

We provide a notebook which generates a large proportion of the figures. It depends on matplotlib and seaborn.

Some figures were generated by hand, rather than programmatically. In particular:

* Figure 1A was drawn in Inkscape
* Figures 1B and 3A were generated with Chimera
* Figure 3C is generated by the notebook discussed above in the Generators subsection.

We nevertheless include these figures in this repository.

These individual subfigures were compiled into three large figures for use in the manuscript. This was also carried out in Inkscape.
