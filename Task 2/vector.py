"""
   Toy example code for a very simple object oriented class of vectors
"""

class Vector:
    """
       Vector class for two dimensional quantities
    """
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        """
        Assumes floating point when printing
        """
        return f"Vector: ({self.a:.2f}, {self.b:.2f})"

    def __add__(self,other):
        """
        Overloads addition for the elements of two instances

        """
        return Vector(self.a + other.a, self.b + other.b)
