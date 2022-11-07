from atom import Atom
from math import cos, sin, radians
from copy import deepcopy
from system import *

s = System(2)

DST = float(input("Enter distance: "))
side = int(input("Enter side: "))

angle = radians(float(input("Enter angle(in degrees): ")))
delta_x = cos(angle) * DST
delta_y = sin(angle) * DST
delta_z = sin(angle) * DST


for i in range(side):
    a = Atom([i*DST, 0, 0])
    s.atoms.append(a)


for a in deepcopy(s.atoms):
    for i in range(1, side):
        a_ = Atom([a.position[0]+delta_x*i, a.position[1]+delta_y*i, 0])
        s.atoms.append(a_)

print(len(s.atoms))
s.visualize()
s.write_cur_state_to_f(
    f"{side**2}atoms2D.xyz")
