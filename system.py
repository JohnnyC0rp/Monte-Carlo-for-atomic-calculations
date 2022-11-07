from random import choice
from atom import *
from numpy import array
from math import dist
from collections import defaultdict


class System:

    def __init__(self, dimensions: int, affecting_radius: int = 2, atoms: list = None):
        self.atoms = atoms if atoms else []
        self.atoms_colors = defaultdict(list)
        self.moved_atoms = []
        self.frames = []
        self.rdf_frames = []
        self.energies = []
        self.marked_atom = None
        self.dimensions = dimensions
        self.affecting_radius = affecting_radius

    def colorize_atoms(self):
        self.atoms_colors = defaultdict(list)
        for a in self.atoms:
            key = f"{a.A}|{a.B}"
            self.atoms_colors[key].append(a)

    def generate_atoms(self, N, position_range, A, B):
        for _ in range(N):
            self.atoms.append(Atom(
                Atom.generate_random_vector(
                    axes=self.dimensions,
                    min_=position_range[0],
                    max_=position_range[1]), A, B))

    def read_atoms_from_file(self, file: str):

        with open(file, "r") as f:
            for line in f:
                if line[0] == "A":
                    l = line.split()
                    self.atoms.append(Atom(
                        [float(l[j]) for j in range(1, self.dimensions+1)
                         ], float(l[3]), float(l[4])
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

    def get_total_E(self, consider_change=False):

        total_energy = 0
        for i, atom1 in enumerate(self.atoms):
            for atom2 in self.atoms[i+1:]:
                if dist(atom1.position, atom2.position) < self.affecting_radius:
                    pair_energy = atom1.get_energy_with(atom2)
                    total_energy += pair_energy
        if consider_change:
            self.energies.append(total_energy)
        return total_energy

    def move_random_atom(self, vector: tuple):
        atom = choice(self.atoms)
        atom.move(array(vector))
        self.moved_atoms.append(atom)

    def restore_previous_stage(self):
        self.energies.pop()
        last_moved_atom = self.moved_atoms.pop()
        last_moved_atom.restore_previous_pos()

    def move_last_atom(self, vector: tuple):
        self.moved_atoms[-1].move(array(vector))
        self.moved_atoms.append(self.moved_atoms[-1])

    def mark_atom(self, atom):
        self.marked_atom = atom

    def write_cur_state_to_f(self, filename="pos.xyz"):
        with open(filename, "w") as f:
            f.write(f"{len(self.atoms)}\n")
            f.write("\n")
            for atom in self.atoms:
                f.write(
                    f"A      {atom.position[0]}      {atom.position[1]}      {'' if self.dimensions == 2 else atom.position[2]}      {atom.A}      {atom.B}\n")

    def __str__(self) -> str:
        if not self.atoms:
            return "No atoms in system yet"
        view = ""
        for atom in self.atoms:
            view += str(atom)
        view += "\nTotal system energy:" + str(self.get_total_E()) + "\n"
        view += "-"*45
        return view

    from _visualize import visualize, add_frame, get_rdf, add_cur_state_to_rdf, get_totalE_plot, add_rdf_frame
