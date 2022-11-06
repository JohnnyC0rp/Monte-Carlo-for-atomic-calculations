from dataclasses import dataclass
from random import uniform
from copy import deepcopy
from math import dist
from numpy import array


@dataclass
class Atom:

    position: array
    A: float = 1
    B: float = 1

    def __post_init__(self) -> None:

        self.old_positions = []

    def get_distance_to(self, atom: "Atom") -> float:
        return dist(self.position,
                    atom.position)

    def get_energy_with(self, atom: "Atom") -> float:
        A_total = self.A + atom.A
        B_total = self.B + atom.B
        r = self.get_distance_to(atom)
        if r == 0:
            return float("inf")

        U = (A_total / (r**12)) - (B_total / (r**6))

        return float(U)

    def move(self, vector: array) -> None:
        self.old_positions.append(deepcopy(self.position))
        self.position += vector

    def restore_previous_pos(self):
        self.position = self.old_positions.pop()

    @staticmethod
    def generate_random_vector(min_=-.1, max_=.1, axes=2):

        return array([uniform(min_, max_) for _ in range(axes)])

    def __str__(self: "Atom") -> str:
        return (f"[Pos] \n {self.position}\n")
