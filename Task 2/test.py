#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use the vector class to do something simple."""

import math
import vector as vec

# Task 1a-e
# Adding vlues to the components

# v1 = vec.Vector(2, 10, -7)
# v2 = vec.Vector(5, -2, 9)
v1 = vec.Vector(7.07, 45, 5)
v2 = vec.Vector(1, -2, 2)
v3 = vec.Vector(2.47, 2.47, 6.06)
v4 = v1 + v2
v5 = v1 - v2
v6 = v1.dot(v2)
v7 = v1.cross(v2)

# Print values for task 1a-e
print("Tasks 1 a-e ..............................................")
print("\nFirst vector", v1)
print("Second vector", v2)
print("Sum of vectors:", v1 + v2)
print("Difference of vectors:", v1 - v2)
print("Magnitude vector 1 = ", v1.mag())
print("Magnitude vector 2 = ", v2.mag())
print("Dot product = ", v1.dot(v2))
print("Cross product = ", v1.cross(v2))

# Task 2a-e

# New spherical vectors
vsph1 = vec.VectorSpherical(1, math.radians(0), math.radians(0))
vsph2 = vec.VectorSpherical(1, math.radians(45), math.radians(0))
vsph3 = vec.VectorSpherical(1, math.radians(90), math.radians(0))
vsph4 = vec.VectorSpherical(1, math.radians(135), math.radians(0))
# vsph1 = vec.VectorSpherical(7, 0.53, 0.79)  # Version with inputing radians

# Converted cartesian vectors to spherical
vsph5 = vec.VectorSpherical.to_sph(v1)  # Convert v1 to spherical coordinates

# Print results for task 2a-e
print("\nTasks 2 a-e ..............................................")
print("\nVector vsph1 in Cartesian coordinates:", vsph1.to_cart())
print("\nSpherical Vector vsph1", vsph1)
print("\nSpherical Vector vsph2", vsph2)
print("\nSpherical Vector vsph3 check", vsph3)
print("Sum of vectors:", vsph1 + vsph2)
print("\nSpherical Vector vsph4 check", vsph4)
print("Difference of vectors:", vsph1 - vsph2)
print("Cross product of vectors:", vsph1.cross(vsph2))
print("Dot product of vectors:", vsph1.dot(vsph2))
print("Magnitude:", vsph1.mag())


# Task 3 a

def tri_area(A, B, C):
    """Get area of given triangle with three vectors."""
    # AB = Vector(C.x_arg, B.z_)
    AB = B - A
    AC = C - A
    cross = AB.cross(AC)
    return 0.5*cross.mag()


def tri_angle(A, B, C):
    """Get angles of the triangle."""
    AB = B - A
    AC = C - A
    BA = C - B
    # BC = C - B
    # CA = A - C
    # CB = B - C

    ang_A = AB.ang(AC)
    ang_B = (-AB).ang(BA)
    ang_C = (-AC).ang(-BA)
    # ang_D = BC.ang(CA)
    # ang_E = BC.ang(CB)
    # ang_F = CA.ang(CB)

    return ang_A, ang_B, ang_C  #, ang_D, ang_E, ang_F


# Triangle 1
A_1, B_1, C_1 = [vec.Vector(0, 0, 0), vec.Vector(1, 0, 0), vec.Vector(0, 1, 0)]
area1 = tri_area(A_1, B_1, C_1)
ang1 = tri_angle(A_1, B_1, C_1)

# Triangle 1
A_2, B_2, C_2 = [vec.Vector(-1, -1, -1), vec.Vector(0, -1, -1), vec.Vector(-1, 0, -1)]
area2 = tri_area(A_2, B_2, C_2)
ang2 = tri_angle(A_2, B_2, C_2)

# Triangle 1
A_3, B_3, C_3 = [vec.Vector(1, 0, 0), vec.Vector(0, 0, 1), vec.Vector(0, 0, 0)]
area3 = tri_area(A_3, B_3, C_3)
ang3 = tri_angle(A_3, B_3, C_3)

# Triangle 1
A_4, B_4, C_4 = [vec.Vector(0, 0, 0), vec.Vector(1, -1, 0), vec.Vector(0, 0, 1)]
area4 = tri_area(A_4, B_4, C_4)
ang4 = tri_angle(A_4, B_4, C_4)



# Print results for task 3
print("\nTasks 3  ..............................................")
print(f"""\nTriangle 1 Area: {area1:.4f}
Angles: {ang1[0]:.2f}°, {ang1[1]:.2f}°, {ang1[2]:.2f}°""")
print(f"\nTriangle 2 Area: {area2:.4f} \nAngles: {ang2[0]:.2f}°, {ang2[1]:.2f}°, {ang2[2]:.2f}°")
print(f"\nTriangle 3 Area: {area3:.4f} \nAngles: {ang3[0]:.2f}°, {ang3[1]:.2f}°, {ang3[2]:.2f}°")
print(f"\nTriangle 4 Area: {area4:.4f} \nAngles: {ang4[0]:.2f}°, {ang4[1]:.2f}°, {ang4[2]:.2f}°")
# print(f"\nTriangle Area:{tri_area(tri_1):.4f}")




