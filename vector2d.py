"""Contains 2D vector class."""

from __future__ import division, print_function

from math import atan2, hypot, sin, cos

from angle import positive_radians

__author__ = "Zander Otavka"


class Vector2D(object):
    """
    :type _components: list[int or float]
    """

    _components = None

    def __init__(self, x=0, y=0):
        """
        :type x: int or float
        :type y: int or float
        """
        self._components = [x, y]

    @classmethod
    def from_polar(cls, magnitude, direction):
        x = cos(direction) * magnitude
        y = sin(direction) * magnitude
        return cls(x, y)

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
        return hypot(self.x, self.y)

    @magnitude.setter
    def magnitude(self, new):
        direction = self.direction
        self.x = cos(direction) * new
        self.y = sin(direction) * new

    @property
    def direction(self):
        return positive_radians(atan2(self.y, self.x))

    @direction.setter
    def direction(self, new):
        magnitude = self.magnitude
        self.x = cos(new) * magnitude
        self.y = sin(new) * magnitude

    def normalized(self):
        return Vector2D.from_polar(1, self.direction)

    def copy(self):
        return +self

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
        return Vector2D(scalar * self.x, scalar * self.y)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self

    def __rtruediv__(self, scalar):
        return Vector2D(scalar / self.x, scalar / self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __pos__(self):
        return Vector2D(+self.x, +self.y)

    def __nonzero__(self):
        return self.x or self.y

    def __iter__(self):
        return self._components.__iter__()

    def __repr__(self):
        return "Vector2D({}, {})".format(self.x, self.y)

    def __str__(self):
        return "<{}, {}>".format(self.x, self.y)
