#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use the vector class to do something simple."""

import math
import vector as vec

# Adding vlues to the components

v1 = vec.Vector(2, 10, -7)
v2 = vec.Vector(5, -2, 9)
# v1 = vec.Vector(3, 4, 5)
# v2 = vec.Vector(1, -2, 2)
v3 = vec.Vector(2.47, 2.47, 6.06)
v4 = v1 + v2
v5 = v1 - v2

# Print values for task 1a-e
print("First vector", v1)
print("Second vector", v2)
print("Sum of vectors:", v1 + v2)
print("Difference of vectors:", v1 - v2)
print("Magnitude vector 1 = ", v1.mag())
print("Magnitude vector 2 = ", v2.mag())
print("Dot product = ", v1.dot(v2))
print("Cross product = ", v1.cross(v2))

# Spherical coordinate test

# New spherical vectors
# vsph1 = vec.VectorSpherical(7, math.radians(30), math.radians(45))
# vsph1 = vec.VectorSpherical(7, 0.53, 0.79)  # Version with inputing radians
vsph2 = vec.VectorSpherical.to_sph(v1)  # Convert v1 to spherical coordinates
vsph3 = vec.VectorSpherical(23, math.radians(15), math.radians(75))

# Print values for task 2
# print("\nSpherical Vector vsph1 ", vsph1)
# print("\nVector vsph1 in Cartesian coordinates:", vsph1.to_cart())
print("\nVector v1 in Spherical coordinates:", vsph2)

print("\nvsph3 spherical", vsph3)
# print("\nSum of vectors:", vsph1 + vsph2)


vsph4 = vec.VectorSpherical.to_sph(v1)
vsph5 = vec.VectorSpherical.to_sph(v2)
vsph6 = vec.VectorSpherical.to_sph(v4)
vsph7 = vec.VectorSpherical.to_sph(v5)

print("\nSpherical Vector vsph4", vsph4)
print("\nSpherical Vector vsph5", vsph5)
print("\nSpherical Vector vsph6", vsph6)
print("\nSpherical Vector vsph7", vsph7)

print("\nSum of vectors:", vsph4 + vsph5)
# print("Difference of vectors:", vsph4 - vsph5)
# print("Magnitude vector 1 = ", v1.mag())
# print("Magnitude vector 2 = ", v2.mag())
# print("Dot product = ", v1.dot(v2))
# print("Cross product = ", v1.cross(v2))
