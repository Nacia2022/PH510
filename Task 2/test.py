#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use the vector class to do something simple."""

import math
import vector as vec

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

# Spherical coordinate test

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
print("\nVector v1 in Spherical coordinates:", vsph5)

# print("\nvsph3 spherical", vsph3)
# print("\nSum of vectors:", vsph1 + vsph2)

# vsph8 = vec.VectorSpherical.to_sph(v7)
# v8 = vsph4.dot(vsph5)
# v9 = vsph1.cross(vsph5)

# Printing results for task 2a-e

print("\nSpherical Vector vsph1", vsph1)
print("\nSpherical Vector vsph2", vsph2)
print("\nSpherical Vector vsph3 check", vsph3)
print("Sum of vectors:", vsph1 + vsph2)
print("\nSpherical Vector vsph4 check", vsph4)
print("Difference of vectors:", vsph1 - vsph2)
print("Cross product of vectors:", vsph1.cross(vsph2))
print("Dot product of vectors:", vsph1.dot(vsph2))
print("Magnitude:", vsph1.mag())
