"""Contains Ball and BallGroup classes."""

from render import BallRenderer

__author__ = "Zander Otavka"


class Ball(object):

    RADIUS = 11.25

    _number = None
    _x = None
    _y = None
    _renderer = None

    def __init__(self, number, x, y):
        self._number = number
        self._x = x
        self._y = y
        self._renderer = BallRenderer(number, x, y, Ball.RADIUS)

    @property
    def number(self):
        return self._number

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new):
        self._x = new
        self._renderer.x = new

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new):
        self._y = new
        self._renderer.y = new

    def __repr__(self):
        return "Ball({}, {}, {})".format(self.number, self.x, self.y)
    __str__ = __repr__

    def delete(self):
        self._renderer.delete()


class BallGroup(list):

    def __init__(self, balls):
        super(BallGroup, self).__init__(balls)

    @classmethod
    def from_data(cls, data):
        return cls(Ball(i // 2, data[i], data[i + 1])
                   for i in range(0, len(data), 2))
