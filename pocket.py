"""Contains Pocket class."""

from render import PocketRenderer

__author__ = "Zander Otavka"


class Pocket(object):

    _position = None
    _point1 = None
    _point2 = None
    _renderer = None

    def __init__(self, position, offset1, offset2):
        self._position = position
        self._point1 = offset1 + position
        self._point2 = offset2 + position
        self._renderer = PocketRenderer(position, offset1, offset2)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new):
        self._position = new
        self._renderer.position = new

    @property
    def point1(self):
        return self._point1

    @point1.setter
    def point1(self, new):
        self._point1 = new
        self._renderer.offset1 = new - self.position

    @property
    def point2(self):
        return self._point2

    @point2.setter
    def point2(self, new):
        self._point2 = new
        self._renderer.offset2 = new - self.position

    def delete(self):
        self._renderer.delete()
