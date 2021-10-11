import numpy as np
import os
import requests
import sys

PROTEIN_DIR = "./data/chains/"
KNOTPROT_XYZ_URL = "https://knotprot.cent.uw.edu.pl/chains/{}/{}/chain.xyz.txt"
KNOTPROT_ERROR = "KnotProt error, status code {}"

def filename(protein, interpolation = 1):
    if interpolation == 1:
        subdir = PROTEIN_DIR
        suffix = ""
    else:
        subdir = PROTEIN_DIR + "interpolated_x{}/".format(interpolation)
        suffix = "_x{}".format(interpolation)
    return subdir + protein + suffix + ".xyz"

def interpolate(points, m):
    if m == 1:
        return points
    n, d = points.shape
    interpolated = np.empty((n*m - m + 1, d))
    for i in range(n-1):
        start = points[i]
        end = points[i+1]
        step = (end - start) / m
        interpolated[i*m] = start
        for j in range(1, m):
            interpolated[i*m + j] = start + j * step
    interpolated[n*m - m] = points[n-1]
    return interpolated

def download_coordinates(protein, timeout = 1):
    pdbid, chain = protein.split("_")
    url = KNOTPROT_XYZ_URL.format(pdbid, chain)
    response = requests.get(url, timeout = timeout)
    if response.status_code != 200:
        raise RuntimeError(KNOTPROT_ERROR.format(response.status_code))
    for line in response.text.splitlines():
        yield " ".join(line.split()[1:]) + "\n"

def save_coordinates(protein, interpolation = 1):
    uninterpolated_name = filename(protein)
    interpolated_name = filename(protein, interpolation)
    if not os.path.isfile(interpolated_name):
        if not os.path.isfile(uninterpolated_name):
            with open(uninterpolated_name, 'w') as output:
                output.writelines(download_coordinates(protein))
        coords = np.loadtxt(uninterpolated_name)
        interpolated = interpolate(coords, interpolation)
        np.savetxt(interpolated_name, interpolated, fmt='%1.3f')
       
def get_coordinates(protein, interpolation = 1):
    name = filename(protein, interpolation)
    if not os.path.isfile(name):
        save_coordinates(protein, interpolation)
    return np.loadtxt(name)

def main():
    if len(sys.argv) < 3:
        print("Too few arguments")
    else:
        csv = sys.argv[1]
        interpolation = 1 if len(sys.argv) < 3 else int(sys.argv[2])
        with open(csv, 'r') as f:
            next(f)
            for row in f:
                protein = row.split(',')[0]
                save_coordinates(protein, interpolation)

if __name__ == "__main__":
    main()
