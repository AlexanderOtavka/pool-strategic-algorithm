"""Contains Pocket class."""

from __future__ import division, print_function

from render import PocketRenderer
from target import ShotTarget

__author__ = "Zander Otavka"


class Pocket(object):

    _position = None
    _offset1 = None
    _offset2 = None
    _renderer = None

    name = None

    def __init__(self, position, offset1, offset2, name=None):
        self._position = position
        self._offset1 = offset1
        self._offset2 = offset2
        self._renderer = PocketRenderer(position, offset1, offset2)
        self.name = name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new):
        self._position = new
        self._renderer.position = new

    @property
    def offset1(self):
        return self._offset1

    @offset1.setter
    def offset1(self, new):
        self._offset1 = new
        self._renderer.offset1 = new

    @property
    def offset2(self):
        return self._offset2

    @offset2.setter
    def offset2(self, new):
        self._offset2 = new
        self._renderer.offset2 = new

    @property
    def target(self):
        p1 = self.position + self.offset1
        p2 = self.position + self.offset2
        # noinspection PyTypeChecker
        return ShotTarget(p1, p2, self.position - (p1 + p2) / 2, name=self.name)

    def delete(self):
        self._renderer.delete()
