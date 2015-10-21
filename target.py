"""Contains ShotTarget class."""

from __future__ import division, print_function

from vector2d import Vector2D

__author__ = "Zander Otavka"


class ShotTarget(object):

    _point1 = None
    _point2 = None
    _force = None

    name = None

    def __init__(self, point1, point2, force, name=None):
        """
        :type point1: Vector2D
        :type point2: Vector2D
        :type force: Vector2D
        """
        self._point1 = point1
        self._point2 = point2
        self._force = force
        self.name = name

    @property
    def point1(self):
        return self._point1

    @property
    def point2(self):
        return self._point2

    @property
    def force(self):
        return self._force

    def __repr__(self):
        return "ShotTarget({}, {}, {})".format(self.point1, self.point2,
                                               self.force)

    def __str__(self):
        return self.name or repr(self)
