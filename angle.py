"""Contains Angle class as well as utilities for calculating angles."""

from __future__ import division, print_function

from math import pi, ceil

__author__ = "Zander Otavka"


class Quadrant(object):
    FIRST = 0
    SECOND = 1
    THIRD = 2
    FOURTH = 3


class Hemisphere(object):
    EAST = (Quadrant.FIRST, Quadrant.FOURTH)
    NORTH = (Quadrant.FIRST, Quadrant.SECOND)
    WEST = (Quadrant.SECOND, Quadrant.THIRD)
    SOUTH = (Quadrant.THIRD, Quadrant.FOURTH)


class Angle(float):

    def __new__(cls, radians=None):
        """
        :type radians: int or float or Angle
        """
        if radians is None:
            radians = 0.0
        if isinstance(radians, Angle):
            return radians
        radians %= 2 * pi
        if radians < 0:
            radians += 2 * pi
        return super(Angle, cls).__new__(cls, radians)

    @property
    def quadrant(self):
        """
        :rtype: int
        """
        return int(ceil(self / (pi / 2)) % 4)

    @property
    def hemispheres(self):
        """
        :rtype: collections.Iterable[(int, int)]
        """
        q = self.quadrant
        for h in (Hemisphere.EAST, Hemisphere.NORTH, Hemisphere.WEST,
                  Hemisphere.SOUTH):
            if q in h:
                yield h

    def __invert__(self):
        return float(self) - 2 * pi

    def __abs__(self):
        return min(self, -(~self))

    def __pos__(self):
        return Angle(super(Angle, self).__pos__())

    def __neg__(self):
        return Angle(super(Angle, self).__neg__())

    def __add__(self, other):
        return Angle(super(Angle, self).__add__(other))

    def __radd__(self, other):
        return Angle(super(Angle, self).__radd__(other))

    def __sub__(self, other):
        return Angle(super(Angle, self).__sub__(other))

    def __rsub__(self, other):
        return Angle(super(Angle, self).__rsub__(other))

    def __mul__(self, other):
        return Angle(super(Angle, self).__mul__(other))

    def __rmul__(self, other):
        return Angle(super(Angle, self).__rmul__(other))

    def __div__(self, other):
        return Angle(super(Angle, self).__div__(other))

    def __rdiv__(self, other):
        return Angle(super(Angle, self).__rdiv__(other))

    def __floordiv__(self, other):
        return Angle(super(Angle, self).__floordiv__(other))

    def __rfloordiv__(self, other):
        return Angle(super(Angle, self).__rfloordiv__(other))

    def __truediv__(self, other):
        return Angle(super(Angle, self).__truediv__(other))

    def __rtruediv__(self, other):
        return Angle(super(Angle, self).__rtruediv__(other))

    def __divmod__(self, other):
        return Angle(super(Angle, self).__divmod__(other))

    def __rdivmod__(self, other):
        return Angle(super(Angle, self).__rdivmod__(other))

    def __mod__(self, other):
        return Angle(super(Angle, self).__mod__(other))

    def __rmod__(self, other):
        return Angle(super(Angle, self).__rmod__(other))

    def __pow__(self, other):
        return Angle(super(Angle, self).__pow__(other))

    def __rpow__(self, other):
        return Angle(super(Angle, self).__rpow__(other))

    def __repr__(self):
        return "Angle({})".format(super(Angle, self).__repr__())

    def __str__(self):
        return "{}pi".format(float(self) / pi)
