import os
import sys
import numpy as np

def add_noise(array, sigma):
    M, N = array.shape
    noise = np.random.normal(0, sigma, [M,N])
    return array + noise

def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    sigma = float(sys.argv[3])

    for filename in os.listdir(input_dir):
        if os.path.isfile(input_dir + filename):
            print(filename)
            new_filename = output_dir + filename
            if not os.path.isfile(new_filename):
                xyz = np.loadtxt(input_dir + filename)
                noisy = add_noise(xyz, sigma)
                np.savetxt(new_filename, noisy, fmt='%1.3f')

if __name__ == "__main__":
    main()
