#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use the vector class to do something simple."""

import vector as vec

# Adding vlues to the components

v1 = vec.Vector(2, 10)
v2 = vec.Vector(5, -2)


# Print values
print("first vector", v1)
print("second vector", v2)
print("sum of vectors:", v1 + v2)
