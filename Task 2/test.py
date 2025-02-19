#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use the vector class to do something simple."""

import vector as vec

# Adding vlues to the components

v1 = vec.Vector(2, 10, -7)
v2 = vec.Vector(5, -2, 9)


# Print values
print("First vector", v1)
print("Second vector", v2)
print("Sum of vectors:", v1 + v2)
print("Difference of vectors:", v1 - v2)
print("Magnitude vector 1 = ", v1.mag())
print("Magnitude vector 2 = ", v2.mag())
print("Dot product = ", v1.dot(v2))
print("Cross product = ", v1.cross(v2))
