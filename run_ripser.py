import os
import sys
import time
import chains
import ripser_reformat_output as rro

RIPSER = "./ripser/ripser"

def read(dict_file):
    with open(dict_file, 'r') as s:
        f = s.read()
        proteins = eval(f)
        return proteins

def diagrams_prefix(protein, interpolation):
    pdbid, chain = protein.split("_")
    if interpolation == 1:
        return "data/diagrams/{}_{}".format(pdbid, chain)
    else:
        return "data/diagrams/interpolated_x{}/{}_{}".format(interpolation, pdbid, chain)

def computed_already(protein, interpolation, dim):
    pref = diagrams_prefix(protein, interpolation)
    return os.path.isfile(pref + "_{}.txt".format(dim))

def main():
    csv = sys.argv[1]
    interpolation = int(sys.argv[2])
    dim = sys.argv[3]
    with open(csv, 'r') as f:
        next(f)
        for row in f:
            protein = row.split(',')[0]
            start_time = time.time()
            print("Processing chain:", protein)
            if computed_already(protein, interpolation, dim):
                print("Already computed")
            else:
                print("Computing homology...")
                cmd = RIPSER + " --format point-cloud " + ("--dim {} ".format(dim)) + chains.filename(protein, interpolation) + " > ripser_output"
                os.system(cmd)
                print("Convering to standard format...")
                rro.reformat("ripser_output", diagrams_prefix(protein, interpolation))
            elapsed_time = time.time() - start_time
            print("Done, time elapsed:", elapsed_time)

if __name__ == "__main__":
    main()
