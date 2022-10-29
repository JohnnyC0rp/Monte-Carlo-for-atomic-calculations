from main import *

calculation_way = input(
    "Enter calculation way:\n'with given num of iters' or 'via counting useless iters' (first is set by default)\n")
ITERS = int(input(
    "Enter num iterations:\n(in second case it will considered as num of useless iterations)\n"))
K = float(input("Enter KT: \n"))
T = 1
FRAMES = int(input(
    "Enter num of frames in animation:\n(This will considered for all animations including rdf animation)\n"))
ATOMS = input("Enter file from which read atoms:\n(skip, if u want to generate them randomly; this feature is recommended for calculating melting)")
if not ATOMS:
    ATOMS = []
    while atoms := input("Enter num of atoms:\n(they wil be generated randomly; skip to continue)\n"):
        SIZE = tuple(map(float, input(
            "Enter space borders in which atoms will be generated separated by space:\n(example: '-1 1')\n").split()))
        A, B = list(map(float, input(
            "Enter A and B for atoms: \n(for example: '0.5 0.5')\n").split()))
        ATOMS.append([int(atoms), SIZE, [A, B]])
AFFECTING_RADIUS = input(
    "Enter affecting radius:\n(this is just an optimization feature, skip for disable; attention: it may seriously affect on synthesis calculations)\n")
if not AFFECTING_RADIUS:
    AFFECTING_RADIUS = float("inf")
else:
    AFFECTING_RADIUS = float(AFFECTING_RADIUS)
DIMENSIONS = int(input("Enter 2 or 3 for specifying dimensions: \n"))

show_automatically = bool(int(input(
    "Do u want to see all received data immediately after finishing:\n(0 or 1; not recommended when running on remote server)\n")))


group = input(
    "Enter calculation group:\n(it will be saved in separate folder)\n")
name = input(
    "Enter name of this calculation so u can find it easily in future:\n")

print("Please wait...")
run(ITERS, K, T, FRAMES,
    AFFECTING_RADIUS, ATOMS, DIMENSIONS, calculation_way, show_automatically, name, group)

input("Done.")
