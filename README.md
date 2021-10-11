# ph-knotted-proteins

This repository is a companion to the paper:

It contains the data analysed in the paper, as well as the code used to generate those data and to produce the accompanying figures.

## Usage

This repository already contains the data produced by the following steps, so it is not necessary to run them again unless desired.

1. Protein chain coordinates are downloaded from KnotProt and interpolated with the script `chains.py`. To generate the 6-fold interpolated coordinates used in the paper, one would run

`python3 chains.py trefoil_list.csv 6`

2. Persistence diagrams corresponding to each of these chains are then generated with the script `run_ripser.py`. By default, this requires Ripser to be installed in the directory `./ripser/`, but this can be amended by editing the variable `RIPSER` in the script. To generate the diagrams corresponding to the 6-fold interpolated protein chains, one would run

`python3 run_ripser.py trefoil_list.csv 6 1`,

where the `1` specifies the maximal degree of homology computed.

