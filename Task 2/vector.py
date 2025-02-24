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
        return f"Vector:({self.x_arg:.2f}, {self.y_arg:.2f}, {self.z_arg:.2f})"

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
        return (self.x_arg * other.x_arg + self.y_arg * other.y_arg +
                self.z_arg * other.z_arg)

    def cross(self, other):
        """Obtain vector (cross) product of 2 vectors."""
        cross_x = (self.y_arg * other.z_arg) - (self.z_arg * other.y_arg)
        cross_y = (self.z_arg * other.x_arg) - (self.x_arg * other.z_arg)
        cross_z = (self.x_arg * other.y_arg) - (self.y_arg * other.x_arg)
        return Vector(cross_x, cross_y, cross_z)

    def ang(self, other):
        """Get angle between two vectors."""
        dot = self.dot(other)
        mags = self.mag() * other.mag()
        ang_rad = math.acos(dot / mags)
        return math.degrees(ang_rad)

    # def tri_area(A, B, C):
    #     """Get area of given triangle with three vectors."""
    #     # AB = Vector(C.x_arg, B.z_)
    #     AB = B - A
    #     AC = C - A
    #     area = 0.5*AB.cross(AC)
    #     return area

    def tri_angle(A, B, C):
        """Get angles of the triangle."""
        AB = B - A
        AC = C - A
        BA = A - B
        BC = C - B
        CA = A - C
        CB = B - C

        ang_A = AB.ang(AC)
        ang_B = AB.ang(BA)
        ang_C = AC.ang(BA)
        ang_D = BC.ang(CA)
        ang_E = BC.ang(CB)
        ang_F = CA.ang(CB)

        return ang_A, ang_B, ang_C, ang_D, ang_E, ang_F

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

        # x_arg = r_mag * math.sin(theta) * math.cos(phi)
        # y_arg = r_mag * math.sin(theta) * math.sin(phi)
        # z_arg = r_mag * math.cos(theta)

        x_arg, y_arg, z_arg = self.to_cart()
        # Initialize with super to avoid referring to base class explocotly and
        # to make the child class inherit all the methods and properties.
        # from its parent
        super().__init__(x_arg, y_arg, z_arg)

    # Degrees version
    def __str__(self):
        """Return the spherical coordinates with theta and phi in degrees."""
        return f"({self.r_mag:.2f}, {math.degrees(self.theta):.2f}, {math.degrees(self.phi):.2f})"

    # def __str__(self):
    #     """Return spherical coordinates with theta and phi in radians."""
    #     return f"({self.r_mag:.2f}, {self.theta:.2f}, {self.phi:.2f})"

    def to_cart(self):
        """Convert to cartesian coordintes."""
        x_arg = self.r_mag * math.sin(self.theta) * math.cos(self.phi)
        y_arg = self.r_mag * math.sin(self.theta) * math.sin(self.phi)
        z_arg = self.r_mag * math.cos(self.theta)
        return (x_arg, y_arg, z_arg)
        # return Vector(self.x_arg, self.y_arg, self.z_arg)
        # Inherited from Vector class so need to use _arg version
        # return Vector(self.x, self.y, self.z)

    # Dont want to use self - i want to refer to the class itself
    @classmethod  # converts function to be a class method. This is the new
    # version. Previous: classmethod(function).
    def to_sph(cls, vector):
        """Convert to spherical coordinates. Classmethod (cls, arg1, ...)."""
        r_mag = vector.mag()
        # r_mag = math.sqrt(vector.x_arg**2 + vector.y_arg**2 + vector.z_arg**2)
        theta = math.acos(vector.z_arg / r_mag)
        phi = math.atan2(vector.y_arg, vector.x_arg)
        return cls(r_mag, theta, phi)

    # def mag_sph(self):
    #    """Return r_mag - the magnitude of the spherical vector."""
    #    return self.r_mag

    def __add__(self, other):
        """Convert spherical to cartesian then add two spherical vectors."""
        v1 = Vector(*self.to_cart())
        v2 = Vector(*other.to_cart())
        cart_sum = v1 + v2
        return VectorSpherical.to_sph(cart_sum)

        # Adding individual arguments. Is it adding in spherical?
        # cart_sum = Vector(self.x_arg + other.x_arg,
        #                           self.y_arg + other.y_arg,
        #                           self.z_arg + other.z_arg)
        # return VectorSpherical.to_sph(cart_sum)

    def __sub__(self, other):
        """Convert sphercal to cartesian then subtract the convert back."""
        v1 = Vector(*self.to_cart())
        v2 = Vector(*other.to_cart())
        cart_diff = v1 - v2
        return VectorSpherical.to_sph(cart_diff)

    def mag(self):
        """Obtain the magnitude of vector."""
        return math.sqrt(self.x_arg**2 + self.y_arg**2 + self.z_arg**2)

    # def dot(self, other):
    #     """Obtain scalar (dot) product of 2 vectors."""
    #     v1 = Vector(*self.to_cart())
    #     v2 = Vector(*other.to_cart())
    #     return VectorSpherical.to_sph(v1.dot(v2))

    def cross(self, other):
        """Obtain vector (cross) product of 2 vectors."""
        v1 = Vector(*self.to_cart())
        v2 = Vector(*other.to_cart())
        cart_cross = v1.cross(v2)
        return VectorSpherical.to_sph(cart_cross)














