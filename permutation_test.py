import sys
import random
import landscapes as pl
import pandas as pd

LANDSCAPE_FILE = './data/validation/landscapes/interpolated_x{}/{}.lan'

def get_landscapes(df, representative, interpolation):
    chains = df[df.Representative == representative].Chain
    return [pl.load(LANDSCAPE_FILE.format(interpolation, chain)) for chain in chains]

def permutation_test(sample1, sample2, reps):
    
    n1 = len(sample1)
    n2 = len(sample2)
    N = n1 + n2
    combined = sample1 + sample2
    
    # A naive approach would be to simply shuffle the combined list
    # and take slices. However, this generates duplicates which are
    # hard to check for. We'd like to record which shuffles (up to
    # permutation) we've already used, and one way is to shuffle
    # the indices and store them as sets.
    
    observed_shuffles = set()
    indices = list(range(N))
    
    baseline = None
    obs = 0
    
    # We don't shuffle to start, since we want to start by recording
    # the actual test statistic as our baseline t
    for i in range(reps):
        if i % 10 == 0:
            print("Test {}, {} positive trials".format(i, obs))
        # Find a shuffle that hasn't been tested before
        first_indices = frozenset(indices[:n1])
        while first_indices in observed_shuffles:
            random.shuffle(indices)
            first_indices = frozenset(indices[:n1])
        second_indices = frozenset(indices[n1:])

        # Record this new shuffle. Note the special case that
        # n1=n2 requires special attention because of symmetry.
        observed_shuffles.add(first_indices)
        if n1 == n2:
            observed_shuffles.add(second_indices)

        # Compute the test statistics on this shuffle
        mean1 = pl.average([combined[i] for i in first_indices])
        mean2 = pl.average([combined[i] for i in second_indices])
        t = pl.distance(mean1, mean2, 1)

        # Update observations
        if baseline is None:
            baseline = t
        if t >= baseline:
            obs += 1
            
    return obs / reps

def main():

    trefoil_df = pd.read_csv("./trefoil_list.csv")

    rep1 = sys.argv[1]
    rep2 = sys.argv[2]
    repetitions = int(sys.argv[3])
    interpolation = sys.argv[4]

    landscapes1 = get_landscapes(trefoil_df, rep1, interpolation)
    landscapes2 = get_landscapes(trefoil_df, rep2, interpolation)

    t = permutation_test(landscapes1, landscapes2, repetitions)

    print("p-value: {}".format(t))

if __name__ == "__main__":
    main()
