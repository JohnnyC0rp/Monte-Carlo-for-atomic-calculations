from random import choice, uniform
from atom import *
from numpy import array


class System:

    def __init__(self, dimensions: int, ATOMS: list = None):
        self.ATOMS = ATOMS if ATOMS else []
        self.moved_atoms = []
        self.frames = []
        self.dimensions = dimensions

    def generate_atoms(self, N, position_range):
        for _ in range(N):
            self.ATOMS.append(Atom(
                Atom.generate_random_vector(
                    axes=self.dimensions,
                    min_=position_range[0],
                    max_=position_range[1])
            ))

    @staticmethod
    def get_generated_atoms(N, dimensions, position_range):

        atoms = []
        for _ in range(N):
            atoms.append(Atom(
                Atom.generate_random_vector(
                    axes=dimensions, min_=position_range[0], max_=position_range[1])
            ))

        return atoms

    def get_total_E(self):

        total_energy = 0
        for i, atom1 in enumerate(self.ATOMS):
            for atom2 in self.ATOMS[i+1:]:
                pair_energy = atom1.get_energy_with(atom2)
                total_energy += pair_energy
        return total_energy

    def move_random_atom(self, vector: tuple):
        atom = choice(self.ATOMS)
        atom.move(array(vector))
        self.moved_atoms.append(atom)

    def restore_previous_stage(self):
        last_moved_atom = self.moved_atoms.pop()
        last_moved_atom.restore_previous_pos()

    def move_last_atom(self, vector: tuple):
        self.moved_atoms[-1].move(array(vector))
        self.moved_atoms.append(self.moved_atoms[-1])

    def write_cur_state_to_f(self, filename="pos.xyz"):
        with open(filename, "w") as f:
            f.write(f"{len(self.ATOMS)}\n")
            f.write("\n")
            for atom in self.ATOMS:
                f.write(
                    f"H      {atom.position[0]}      {atom.position[1]}      {0 if self.dimensions == 2 else atom.position[2]}\n")

    def __str__(self) -> str:
        if not self.ATOMS:
            return "No atoms in system yet"
        view = ""
        for atom in self.ATOMS:
            view += str(atom)
        view += "\nTotal system energy:" + str(self.get_total_E()) + "\n"
        view += "-"*45
        return view

    from _visualize import visualize, add_frame, get_distances_bar_plot


if __name__ == '__main__':
    # TODO
    # [x] Check restore system function
    s = System(3)
    s.generate_atoms(2, (-.1, .1))
    print(s)
    s.move_random_atom((1, 1, 1))
    print(s)
    s.move_last_atom((1, 1, 1))
    print(s)
    s.move_last_atom((1, 1, 1))
    print(s)
    s.restore_previous_stage()
    s.restore_previous_stage()
    s.restore_previous_stage()
    print(s)

    print(start_e := s.get_total_E())
    print(s.ATOMS[0].get_energy_with(s.ATOMS[1]))
    print(s.ATOMS)

    for _ in range(10):
        s.move_random_atom((1, 1, 1))

    print(s.ATOMS)
    print(s.get_total_E())
    print(s.ATOMS[0].get_energy_with(s.ATOMS[1]))

    for _ in range(10):
        s.restore_previous_stage()

    print(s.ATOMS)
    print(final_e := s.get_total_E())
    print(s.ATOMS[0].get_energy_with(s.ATOMS[1]))

    assert final_e == start_e

    print(s)
    print("Tests passed")
