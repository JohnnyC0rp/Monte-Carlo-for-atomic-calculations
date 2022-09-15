from FindingBestCrystal import *
from sys import argv


def read_atoms(file):
    from atom import Atom
    atoms = []
    with open(file, "r") as f:
        for line in f:
            if line[0] == "H":
                l = line.split()
                atoms.append(Atom(
                    [float(l[1]), float(l[2])]
                ))
    return atoms

ITERS = 10000
K = .001
T = int(argv[1])
FRAMES = 10
ATOMS = read_atoms("xyz/pos_atoms=100_iters=200000_KT=0.0000001.xyz")
AFFECTING_RADIUS = 2
DIMENSIONS = 2
SIZE = (-1, 1)

find_best_structure(ITERS, K, T, FRAMES, AFFECTING_RADIUS,
                    ATOMS, DIMENSIONS, SIZE)
