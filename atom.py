from dataclasses import dataclass
from random import uniform
from copy import deepcopy
from math import dist
from numpy import array


@dataclass
class Atom:

    position: array
    A: int = 0.5  # ???? How are these coefficients exactly working?
    B: int = 0.5

    def __post_init__(self) -> None:

        self.old_positions = []

    def get_distance_to(self, atom: "Atom") -> float:
        return dist(self.position,
                    atom.position)

    def get_energy_with(self, atom: "Atom") -> float:
        A_general = self.A + atom.A
        B_general = self.B + atom.B
        r = self.get_distance_to(atom)

        U = (A_general / (r**12)) - (B_general / (r**6))

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


if __name__ == '__main__':
    a = Atom(Atom.generate_random_vector(axes=3))
    start_pos = deepcopy(a.position)
    a.move((1, 1, 1))
    a.restore_previous_pos()
    print(a.position, start_pos)
    assert all(a.position == start_pos)
    print("Tests passed")
    print(a)
