from typing import Literal
from system import *
from random import random, choice
from atom import *
from math import e
from os import makedirs
from atom import Atom


def run(ITERS, K, T, FRAMES, affecting_radius, atoms, dimensions, calculation_way: Literal["with given num of iters", "via counting useless iters"] = "with given num of iters", show_results_automatically: bool = True, calculation_name: str = "", calculation_group: str = ""):

    path = f"output/{calculation_group}/{calculation_name}_KT={K*T}/"
    makedirs(path)
    makedirs(path+"html/")
    makedirs(path+"png/")
    makedirs(path+"xyz/")

    def monte_carlo(deltaU, K, T):
        acception_probability = e ** ((-deltaU)/(K*T))
        return bool(random() < acception_probability)

    system = System(dimensions, affecting_radius=affecting_radius)

    if type(atoms[0]) == list:
        for i in atoms:
            system.generate_atoms(i[0], i[1], i[2][0], i[2][1])
    elif type(atoms) == str:
        system.read_atoms_from_file(atoms)
    else:
        system.atoms = atoms

    system.write_cur_state_to_f(path+"xyz/start.xyz")
    system.add_cur_state_to_rdf(
        title="start for all pairs")
    system.add_cur_state_to_rdf(
        (rdf_main_atom := choice(system.atoms)).position, "start from one atom", "from certain atom")
    system.mark_atom(rdf_main_atom)
    system.add_frame()
    system.add_rdf_frame()

    if calculation_way == "with given num of iters" or calculation_way == "":
        for i in range(ITERS):

            if i % (ITERS//FRAMES) == 0:
                system.add_frame()
                system.add_rdf_frame()
                print(f"Completed on {round(i/(ITERS/FRAMES)/FRAMES*100,5)}%")

            old_energy = system.get_total_E(consider_change=True)
            system.move_random_atom(Atom.generate_random_vector(axes=system.dimensions,
                                                                min_=-.5,
                                                                max_=.5))

            new_energy = system.get_total_E()

            if new_energy > old_energy:
                if not monte_carlo(new_energy-old_energy, K, T):
                    system.restore_previous_stage()

    elif calculation_way == "via counting useless iters":
        uselessiters = 0
        while uselessiters < ITERS:

            if uselessiters % (ITERS//FRAMES) == 0:
                system.add_frame()
                system.add_rdf_frame()

            old_energy = system.get_total_E(consider_change=True)
            system.move_random_atom(Atom.generate_random_vector(axes=system.dimensions,
                                                                min_=-.05,
                                                                max_=.05))

            new_energy = system.get_total_E()
            if new_energy > old_energy:
                if not monte_carlo(new_energy-old_energy, K, T):
                    system.restore_previous_stage()
                    uselessiters += 1
                else:
                    uselessiters = 0

    else:
        raise ValueError(
            f"Incorrect argument given. '{calculation_way}' was given. 'with given num of iters' or 'via counting useless iters' was expected.")

    # Saving and visualizing

    system.add_cur_state_to_rdf(rdf_main_atom.position, "end for all pairs")
    system.add_cur_state_to_rdf(
        rdf_main_atom.position, "end from one ceratin atom", "from certain atom")
    system.add_frame()
    system.add_rdf_frame()

    system.visualize(
        show=show_results_automatically,
        html=path+"html/animation.html",
        img=path+"png/animation.png")
    system.get_totalE_plot(
        show=show_results_automatically,
        html=path+"html/energy.html",
        img=path+"png/energy.png")
    system.get_rdf(
        show=show_results_automatically,
        html=path+"html/rdf.html",
        img=path+"png/rdf.png")
    system.write_cur_state_to_f(path+"xyz/end.xyz")

    print("Atoms", atoms)
    print("Iterations:", ITERS)
    print(system)


if __name__ == "__main__":
    run(50000, 0.001, 1, 15, float('inf'), 10, 2, (-1, 1),
        "with given num of iters", True, input("Name: "), "test")
