from atom import Atom
from math import cos, sin, radians
from copy import deepcopy
from system import *

s = System(2)

DST = 1.12

angle = radians(60)
delta_x = cos(angle) * DST
delta_y = sin(angle) * DST
delta_z = sin(angle) * DST


for i in range(10):
    a = Atom([i*DST, 0, 0])
    s.atoms.append(a)


for a in deepcopy(s.atoms):
    for i in range(1, 10):
        a_ = Atom([a.position[0]+delta_x*i, a.position[1]+delta_y*i, 0])
        s.atoms.append(a_)

print(len(s.atoms))
s.visualize()
s.write_cur_state_to_f(
    "Ready structures for calculating melting/100atoms2D.xyz")
