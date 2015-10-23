"""Contains Ball and BallGroup classes."""

from __future__ import division, print_function

from render import BallRenderer
from vector2d import Vector2D

__author__ = "Zander Otavka"


class Ball(object):
    """
    :type _number: int
    :type _position: Vector2D
    :type _renderer: BallRenderer
    """

    RADIUS = 11.25

    _number = None
    _position = None
    _renderer = None

    def __init__(self, number, position):
        self._number = number
        self._position = position
        self._renderer = BallRenderer(number, position, Ball.RADIUS)

    @property
    def number(self):
        return self._number

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new):
        self._position = new
        self._renderer.position = new

    def __repr__(self):
        return "Ball({}, {})".format(self.number, self.position)

    def delete(self):
        self._renderer.delete()


class BallGroup(list):
    """
    :type _size: int
    """

    _size = None

    def __init__(self):
        super(BallGroup, self).__init__()
        self._size = 0

    def update(self, data):
        """
        :type data: list[int]
        """
        point_list = [Vector2D(data[i:i + 2])
                      for i in range(0, len(data), 2)]
        if len(point_list) != self._size:
            self.delete()
            for index, point in enumerate(point_list):
                if point:
                    self.append(Ball(index, point))
            self._size = len(point_list)
        else:
            for ball in self:
                point = point_list[ball.number]
                if point:
                    ball.offset = point
                else:
                    ball.delete()
                    self.remove(ball)

    def copy(self):
        """
        :rtype: BallGroup
        """
        clone = BallGroup()
        clone[:] = self[:]
        return clone

    def delete(self):
        for ball in self:
            ball.delete()
        self[:] = []
