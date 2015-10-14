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

    def __init__(self):
        super(BallGroup, self).__init__()

    def update(self, data):
        point_list = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]
        if len(point_list) != len(self):
            self[:] = [Ball(index, point[0], point[1])
                       if point[0] and point[1] else None
                       for index, point in enumerate(point_list)]
        else:
            for i, ball in enumerate(self):
                x, y = point_list[i]
                if x and y:
                    ball.x = x
                    ball.y = y
                else:
                    ball.delete()
                    self[i] = None
