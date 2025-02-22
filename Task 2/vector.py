#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Toy example code for a very simple object oriented class of vectors."""

# Add postponed annotations feature to use something in an annotation even if
# it hasnt been defined yet.
from __future__ import annotations

# Import math
import math


class Vector:
    """Vector class for three dimensional quantities (3D vector)."""

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

    def __sub__(self, other):
        """Overloads subtraction for the elements of two instances."""
        return Vector(self.x_arg - other.x_arg, self.y_arg - other.y_arg,
                      self.z_arg - other.z_arg)

    def mag(self):
        """Obtain the magnitude of vector."""
        return math.sqrt(self.x_arg**2 + self.y_arg**2 + self.z_arg**2)

    def dot(self, other):
        """Obtain scalar (dot) product of 2 vectors."""
        return self.x_arg * other.x_arg + self.y_arg * other.y_arg + self.z_arg * other.z_arg

    def cross(self, other):
        """Obtain vector (cross) product of 2 vectors."""
        cross_x = (self.y_arg * other.z_arg) - (self.z_arg * other.y_arg)
        cross_y = (self.z_arg * other.x_arg) - (self.x_arg * other.z_arg)
        cross_z = (self.x_arg * other.y_arg) - (self.y_arg * other.x_arg)
        return (cross_x, cross_y, cross_z)


# Spherical Vector ############################################################

# Spherical-Polar form

class VectorSpherical(Vector):
    """
    Spherical vector class for 3D vector in spherical-polar cooridanates.

    Coordinates:
        r_mag: magnitude of radius
        theta: polar angle in radians
        phi: azimuthal angle in radians
    """

    def __init__(self, r_mag, theta, phi):
        """Initialize a vector with spherical coordinates."""
        self.r_mag = r_mag
        self.theta = theta
        self.phi = phi

        # Change to cartesian coordinates
        x = r_mag * math.sin(theta) * math.cos(phi)
        y = r_mag * math.sin(theta) * math.sin(phi)
        z = r_mag * math.cos(theta)

        # Initialize
        super().__init__(x, y, z)

    def __str__(self):
        """Return the spherical coordinates."""
        return f"VectorSpherical(r_mag={self.r_mag:.2f}, theta={math.degrees(self.theta):.2f}, phi={math.degrees(self.phi):.2f})"

    def to_cart(self):
        """Convert to cartesian coordintes."""
        return Vector(self.x_arg, self.y_arg, self.z_arg)

    def from_cart(cls, vector: Vector):
        """Convert to spherical coordinates."""
        r_mag = vector.magnitude
        theta = math.acos(vector.z / r_mag) if r_mag!=0 else 0
        phi = math.atan2(vector.y, vector.x)
        return cls(r_mag, theta, phi)













