"""Contains Renderer classes."""

from __future__ import division

from abc import ABCMeta, abstractmethod
from math import pi, sin, cos, ceil

from pyglet.graphics import Batch, Group, OrderedGroup
from pyglet.gl import GL_POINTS, GL_TRIANGLE_FAN
from pyglet.text import Label

from angle import simplify_radians

__author__ = "Zander Otavka"


class Renderer(object):
    __metaclass__ = ABCMeta

    BATCH = Batch()

    _renderers = []

    _group = None
    _vertex_list = None
    _color = None

    def __init__(self, color, group=None):
        Renderer._renderers.append(self)
        self._group = Group(parent=group)
        self._color = color

    @staticmethod
    def update_all_vertex_lists():
        for renderer in Renderer._renderers:
            renderer.update_vertex_list()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new):
        self._color = new

    def delete(self):
        self._vertex_list.delete()
        self._vertex_list = None

    @abstractmethod
    def update_vertex_list(self):
        pass


class LineRenderer(Renderer):

    _points = None

    def __init__(self, color, points, group=None):
        super(LineRenderer, self).__init__(color, group)
        self._points = points
        self._create_vertex_list()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, new):
        self.points = new

    def _create_vertex_list(self):
        self._vertex_list = Renderer.BATCH.add(
            len(self.points), GL_POINTS, self._group,
            "v2f", "c3B"
        )

    def update_vertex_list(self):
        if self._vertex_list.get_size() != len(self.points):
            self._vertex_list.resize(len(self.points))

        self._vertex_list.vertices[:] = [number for point in self.points
                                         for number in point]
        self._vertex_list.colors[:] = self.color * len(self.points)


class CircleArc(object):

    _start_angle = None
    _end_angle = None

    def __init__(self, start_angle, end_angle):
        self._start_angle = simplify_radians(start_angle)
        self._end_angle = simplify_radians(end_angle)

    @property
    def start_angle(self):
        return self._start_angle

    @start_angle.setter
    def start_angle(self, new):
        self._start_angle = simplify_radians(new)

    @property
    def end_angle(self):
        return self._end_angle

    @end_angle.setter
    def end_angle(self, new):
        self._end_angle = simplify_radians(new)

    def get_point_count(self, resolution):
        return int(abs(ceil((self.end_angle - self.start_angle) / (2 * pi) *
                            resolution)))

    def get_points(self, radius, number, x_offset=0, y_offset=0):
        for i in range(number):
            angle = (i * ((self.end_angle - self.start_angle) % (2 * pi)) /
                     (number - 1) +
                     self.start_angle)
            x = cos(angle) * radius + x_offset
            y = sin(angle) * radius + y_offset
            yield (x, y)


class CircleRenderer(Renderer):

    CIRCLE_RESOLUTION = 50

    _x = None
    _y = None
    _radius = None
    _circle_points = None

    def __init__(self, color, x, y, radius, circle_points, group=None):
        super(CircleRenderer, self).__init__(color, group)
        self._x = x
        self._y = y
        self._radius = radius
        self._circle_points = circle_points
        self._create_vertex_list()

    @classmethod
    def new_circle(cls, color, x, y, radius, group=None):
        circle_points = [CircleArc(0, 1.99 * pi)]
        return cls(color, x, y, radius, circle_points, group)

    @classmethod
    def new_sector(cls, color, x, y, radius, start_angle, end_angle,
                   group=None):
        circle_points = [
            (0, 0),
            CircleArc(start_angle, end_angle),
            (0, 0)
        ]
        return cls(color, x, y, radius, circle_points, group)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new):
        self._x = new

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new):
        self._y = new

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, new):
        self._radius = new

    @property
    def circle_points(self):
        return self._circle_points

    @circle_points.setter
    def circle_points(self, new):
        self._circle_points = new

    @property
    def point_count(self):
        count = 0
        for point in self._circle_points:
            if isinstance(point, CircleArc):
                count += point.get_point_count(CircleRenderer.CIRCLE_RESOLUTION)
            else:
                count += 1
        return count

    def _create_vertex_list(self):
        self._vertex_list = Renderer.BATCH.add(
            50, GL_TRIANGLE_FAN, self._group,
            "v2f", "c3B"
        )

    def update_vertex_list(self):
        if self._vertex_list.get_size() != self.point_count:
            self._vertex_list.resize(self.point_count)

        points = []
        for circle_point in self.circle_points:
            if isinstance(circle_point, CircleArc):
                arc_points = list(circle_point.get_points(
                    self.radius, circle_point.get_point_count(
                        CircleRenderer.CIRCLE_RESOLUTION),
                    x_offset=self.x, y_offset=self.y))
                points.extend(arc_points)
            else:
                points.append((circle_point[0] + self.x,
                               circle_point[1] + self.y))

        assert self.point_count == len(points)
        self._vertex_list.vertices[:] = [number for point in points
                                         for number in point]

        self._vertex_list.colors[:] = self.color * self.point_count


class BallRenderer(object):

    COLORS = [
        (255, 255, 255),  # cue- white
        (230, 200, 100),  # 1  - yellow
        (100, 100, 200),  # 2  - blue
        (240,  80,  60),  # 3  - red
        (160, 100, 200),  # 4  - purple
        (210, 130,  70),  # 5  - orange
        (20,  110,  60),  # 6  - green
        (130,  90,  30),  # 7  - brown
        (0,     0,   0),  # 8  - black
        (230, 200, 100),  # 9  - yellow
        (100, 100, 200),  # 10 - blue
        (200, 100, 100),  # 11 - red
        (160, 100, 200),  # 12 - purple
        (210, 130,  70),  # 13 - orange
        (20,  110,  60),  # 14 - green
        (130,  90,  30),  # 15 - brown
    ]

    _BALL_GROUP = Group()
    _CIRCLE_GROUP = OrderedGroup(0, _BALL_GROUP)
    _STRIPE_GROUP = OrderedGroup(1, _BALL_GROUP)
    _NUMBER_BG_GROUP = OrderedGroup(2, _BALL_GROUP)
    _NUMBER_GROUP = OrderedGroup(3, _BALL_GROUP)

    _circle = None
    _top_stripe = None
    _bottom_stripe = None
    _number_bg = None
    _number = None

    def __init__(self, number, x, y, radius):
        self._circle = CircleRenderer.new_circle(BallRenderer.COLORS[number],
                                                 x, y, radius,
                                                 BallRenderer._CIRCLE_GROUP)
        if number > 8:
            self._top_stripe = CircleRenderer(
                (255, 255, 255), x, y, radius, [CircleArc(pi / 4, 3*pi / 4)],
                BallRenderer._STRIPE_GROUP)
            self._bottom_stripe = CircleRenderer(
                (255, 255, 255), x, y, radius, [CircleArc(-3*pi / 4, -pi / 4)],
                BallRenderer._STRIPE_GROUP)
        if number > 0:
            self._number_bg = CircleRenderer.new_circle(
                (255, 255, 255), x, y, 6, BallRenderer._NUMBER_BG_GROUP)
            self._number = Label(str(number), font_name="Times New Roman",
                                 font_size=9, color=(0, 0, 0, 255),
                                 x=x, y=y, anchor_x="center", anchor_y="center",
                                 batch=Renderer.BATCH,
                                 group=BallRenderer._NUMBER_GROUP)

    @property
    def x(self):
        return self._circle.x

    @x.setter
    def x(self, new):
        self._circle.x = new
        if self._top_stripe is not None:
            self._top_stripe.x = new
        if self._bottom_stripe is not None:
            self._bottom_stripe.x = new
        if self._number is not None:
            self._number.x = new
            self._number_bg.x = new

    @property
    def y(self):
        return self._circle.y

    @y.setter
    def y(self, new):
        self._circle.y = new
        if self._top_stripe is not None:
            self._top_stripe.y = new
        if self._bottom_stripe is not None:
            self._bottom_stripe.y = new
        if self._number is not None:
            self._number.y = new
            self._number_bg.y = new

    def delete(self):
        self._circle.delete()
        self._circle = None
        if self._top_stripe is not None:
            self._top_stripe.delete()
            self._top_stripe = None
        if self._bottom_stripe is not None:
            self._bottom_stripe.delete()
            self._bottom_stripe = None
        self._number = None
        if self._number_bg is not None:
            self._number_bg.delete()
            self._number_bg = None
