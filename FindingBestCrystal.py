from system import *
from random import random
from atom import *
from math import e


def find_best_structure(ITERS, K, T, FRAMES, affecting_radius, ATOMS, dimensions, space_size):

    def monte_carlo(deltaU, K, T):
        acception_probability = e ** ((-deltaU)/(K*T))
        return bool(random() < acception_probability)

    system = System(dimensions, affecting_radius=affecting_radius)

    if type(ATOMS) == int:
        system.generate_atoms(ATOMS, space_size)
    else:
        system.ATOMS = ATOMS

    system.add_frame()

    for i in range(ITERS):

        if i % (ITERS//FRAMES) == 0:
            system.add_frame()

        old_energy = system.get_total_E()
        system.move_random_atom(Atom.generate_random_vector(axes=system.dimensions,
                                                            min_=-.5,
                                                            max_=.5))

        new_energy = system.get_total_E()

        if new_energy > old_energy:
            if not monte_carlo(new_energy-old_energy, K, T):
                system.restore_previous_stage()

    # uselessiters = 0
    # minenergy = float("inf")
    # while uselessiters < 10000:

    #     old_energy = system.get_total_E()
    #     system.move_random_atom(Atom.generate_random_vector(axes=system.dimensions,
    #                                                         min_=-.05,
    #                                                         max_=.05))

    #     new_energy = system.get_total_E()
    #     if new_energy<minenergy:
    #         minenergy=new_energy
    #         uselessiters = 0
    #     else:
    #         uselessiters+=1
    #     if new_energy > old_energy:
    #         if not monte_carlo(new_energy-old_energy, K, T):
    #             system.restore_previous_stage()

    # Saving and visualizing
    system.add_frame()
    system.visualize(
        f"output/animation_kt={K*T}_numatoms={len(system.ATOMS)}iters={ITERS}.html")
    system.get_distances_bar_plot()
    system.get_RDF_plot(
        f"output/rdf_kt={K*T}_numatoms={len(system.ATOMS)}iters={ITERS}.html")
    system.write_cur_state_to_f(
        f"xyz/{len(system.ATOMS)}atoms_{ITERS}iterations.xyz")

    print("Atoms", ATOMS)
    print("Iterations:", ITERS)
    print(system)

if __name__ == '__main__':
    ITERS = 10000
    K =   .001 
    T = 1
    FRAMES = 10
    ATOMS = 15
    AFFECTING_RADIUS = 1.5
    DIMENSIONS = 3
    SIZE = (-1,1)

    find_best_structure(ITERS,K,T,FRAMES,AFFECTING_RADIUS,ATOMS,DIMENSIONS,SIZE)

