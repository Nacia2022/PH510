#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Toy example code for a very simple object oriented class of vectors."""

# Add postponed annotations feature to use something in an annotation even if
# it hasnt been defined yet.
from __future__ import annotations

# Import math
import math


class Vector:
    """Vector class for two dimensional quantities (2D vector)."""

    def __init__(self, x_arg, y_arg, z_arg):
        """Initialize a vector with components x and b."""
        self.x_arg = x_arg
        self.y_arg = y_arg
        self.z_arg = z_arg

    def __str__(self):
        """Assumes floating point when printing."""
        return f"Vector: ({self.x_arg:.2f}, {self.y_arg:.2f}, {self.z_arg:.2f})"

    def __add__(self, other):
        """Overloads addition for the elements of two instances."""
        return Vector(self.x_arg + other.x_arg, self.y_arg + other.y_arg,
                      self.z_arg + other.z_arg)

    def __mag__(self):
        """Obtain the magnitude of vector."""
        return math.sqrt(self.x_arg**2 + self.y_arg**2 + self.z_arg**2)

    def __dot__(self, other):
        """Obtain scalar (dot) ptoduct of 2 vectors."""
        return self.x_arg * other.x_arg + self.y_arg * other.y_arg + self.z_arg * other.z_arg
