"""Contains the Shot class."""

__author__ = "Zander Otavka"


class Shot(object):

    _angle = None
    _elevation = None
    _force = None

    def __init__(self, angle=0, elevation=0, force=0):
        self._angle = angle
        self._elevation = elevation
        self._force = force

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new):
        self._angle = new

    @property
    def elevation(self):
        return self._elevation

    @elevation.setter
    def elevation(self, new):
        self._elevation = new

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, new):
        self._force = new

    @property
    def rating(self):
        return 0

    def serialize(self):
        return self.angle, self.elevation, self.force
