"""Contains 2D vector class."""

from __future__ import division, print_function

from math import atan2, sqrt

__author__ = "Zander Otavka"


class Vector2D(object):

    _components = None

    def __init__(self, x=0, y=0):
        self._components = [x, y]

    @property
    def x(self):
        return self._components[0]

    @x.setter
    def x(self, new):
        self._components[0] = new

    @property
    def y(self):
        return self._components[1]

    @y.setter
    def y(self, new):
        self._components[1] = new

    @property
    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    @property
    def direction(self):
        return atan2(self.y, self.x)

    def copy(self):
        return Vector2D(self.x, self.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self

    def __rmul__(self, scalar):
        return self * scalar

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self

    def __rtruediv__(self, scalar):
        return self / scalar

    def __nonzero__(self):
        return self.x or self.y

    def __iter__(self):
        return self._components.__iter__()

    def __repr__(self):
        return "Vector2D({}, {})".format(self.x, self.y)

    def __str__(self):
        return "<{}, {}>".format(self.x, self.y)
