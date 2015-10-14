"""Contains Renderer classes."""

from __future__ import division

from abc import ABCMeta, abstractmethod, abstractproperty
from math import pi, sin, cos, ceil

from pyglet.graphics import Batch, Group, OrderedGroup
from pyglet.gl import GL_LINES, GL_TRIANGLE_FAN
from pyglet.text import Label

from angle import simplify_radians

__author__ = "Zander Otavka"


batch = Batch()


class Renderer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def delete(self):
        pass


class PrimitiveRenderer(Renderer):
    __metaclass__ = ABCMeta

    _renderers = []

    _group = None
    _vertex_list = None
    _color = None

    def __init__(self, color, group=None):
        PrimitiveRenderer._renderers.append(self)
        self._group = Group(parent=group)
        self._color = color

    @staticmethod
    def update_all_vertex_lists():
        for renderer in PrimitiveRenderer._renderers:
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


class LineRenderer(PrimitiveRenderer):

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
        self._vertex_list = batch.add(len(self.points), GL_LINES, self._group,
                                      "v2f", "c3B")

    def update_vertex_list(self):
        if self._vertex_list.get_size() != len(self.points):
            self._vertex_list.resize(len(self.points))

        self._vertex_list.vertices[:] = [number for point in self.points
                                         for number in point]
        self._vertex_list.colors[:] = self.color * len(self.points)

    def delete(self):
        super(LineRenderer, self).delete()


class CirclePointGroup(object):
    __metaclass__ = ABCMeta

    _circle_renderer = None

    def __init__(self, circle_renderer=None):
        self._circle_renderer = circle_renderer

    @property
    def circle_renderer(self):
        return self._circle_renderer

    @circle_renderer.setter
    def circle_renderer(self, new):
        self._circle_renderer = new

    @abstractproperty
    def point_count(self):
        pass

    @abstractproperty
    def points(self):
        pass

    def delete(self):
        self.circle_renderer = None


class CirclePoint(CirclePointGroup):

    _x = None
    _y = None

    def __init__(self, x, y, circle_renderer=None):
        super(CirclePoint, self).__init__(circle_renderer)
        self._x = x
        self._y = y

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
    def point_count(self):
        return 1

    @property
    def points(self):
        return [(self.x + self.circle_renderer.x,
                 self.y + self.circle_renderer.y)]


class CircleArc(CirclePointGroup):

    _start_angle = None
    _end_angle = None

    def __init__(self, start_angle, end_angle, circle_renderer=None):
        super(CircleArc, self).__init__(circle_renderer)
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

    @property
    def point_count(self):
        return int(abs(ceil((self.end_angle - self.start_angle) / (2 * pi) *
                            self.circle_renderer.resolution)))

    @property
    def points(self):
        for i in range(self.point_count):
            angle = (i * ((self.end_angle - self.start_angle) % (2 * pi)) /
                     (self.point_count - 1) + self.start_angle)
            x = (cos(angle) * self.circle_renderer.radius +
                 self.circle_renderer.x)
            y = (sin(angle) * self.circle_renderer.radius +
                 self.circle_renderer.y)
            yield (x, y)


class CircleRenderer(PrimitiveRenderer):

    DEFAULT_RESOLUTION = 50

    _x = None
    _y = None
    _radius = None
    _circle_points = None
    _resolution = None

    def __init__(self, color, x, y, radius, circle_points, resolution=None,
                 group=None):
        super(CircleRenderer, self).__init__(color, group)
        self._x = x
        self._y = y
        self._radius = radius
        for point in circle_points:
            point.circle_renderer = self
        self._circle_points = circle_points
        if resolution is not None:
            self._resolution = resolution
        else:
            self._resolution = CircleRenderer.DEFAULT_RESOLUTION
        self._create_vertex_list()

    @classmethod
    def new_circle(cls, color, x, y, radius, resolution=None, group=None):
        circle_points = [CircleArc(0, 1.99 * pi)]
        return cls(color, x, y, radius, circle_points, resolution, group)

    @classmethod
    def new_sector(cls, color, x, y, radius, start_angle, end_angle,
                   resolution=None, group=None):
        circle_points = [CirclePoint(0, 0), CircleArc(start_angle, end_angle)]
        return cls(color, x, y, radius, circle_points, resolution, group)

    @classmethod
    def new_segment(cls, color, x, y, radius, start_angle, end_angle,
                    resolution=None, group=None):
        circle_points = [CircleArc(start_angle, end_angle)]
        return cls(color, x, y, radius, circle_points, resolution, group)

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
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, new):
        self._resolution = new

    @property
    def point_count(self):
        count = 0
        for point in self._circle_points:
            count += point.point_count
        return count

    def _create_vertex_list(self):
        self._vertex_list = batch.add(self.point_count, GL_TRIANGLE_FAN,
                                      self._group, "v2f", "c3B")

    def update_vertex_list(self):
        if self._vertex_list.get_size() != self.point_count:
            self._vertex_list.resize(self.point_count)

        points = []
        for circle_point in self.circle_points:
            points.extend(list(circle_point.points))

        assert self.point_count == len(points)
        self._vertex_list.vertices[:] = [number for point in points
                                         for number in point]

        self._vertex_list.colors[:] = self.color * self.point_count

    def delete(self):
        super(CircleRenderer, self).delete()
        for point in self.circle_points:
            point.delete()


class BallRenderer(Renderer):

    COLORS = [
        (255, 255, 255),  # cue- white
        (230, 200, 100),  # 1  - yellow
        (100, 100, 200),  # 2  - blue
        (220,  80,  60),  # 3  - red
        (160, 100, 200),  # 4  - purple
        (210, 130,  70),  # 5  - orange
        (20,  110,  60),  # 6  - green
        (130,  90,  30),  # 7  - brown
        (0,     0,   0),  # 8  - black
        (230, 200, 100),  # 9  - yellow
        (100, 100, 200),  # 10 - blue
        (220,  80,  60),  # 11 - red
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

    _CIRCLE_RESOLUTION = 30
    _BALL_BG_RESOLUTION = 20

    _circle = None
    _top_stripe = None
    _bottom_stripe = None
    _number_bg = None
    _number = None

    def __init__(self, number, x, y, radius):
        self._circle = CircleRenderer.new_circle(
            BallRenderer.COLORS[number], x, y, radius,
            BallRenderer._CIRCLE_RESOLUTION, BallRenderer._CIRCLE_GROUP)
        if number > 8:
            self._top_stripe = CircleRenderer.new_segment(
                (255, 255, 255), x, y, radius, pi / 4, 3 * pi / 4,
                BallRenderer._CIRCLE_RESOLUTION, BallRenderer._STRIPE_GROUP)
            self._bottom_stripe = CircleRenderer.new_segment(
                (255, 255, 255), x, y, radius, -3 * pi / 4, -pi / 4,
                BallRenderer._CIRCLE_RESOLUTION, BallRenderer._STRIPE_GROUP)
        if number > 0:
            self._number_bg = CircleRenderer.new_circle(
                (255, 255, 255), x, y, 6, BallRenderer._BALL_BG_RESOLUTION,
                BallRenderer._NUMBER_BG_GROUP)
            self._number = Label(str(number), font_name="Times New Roman",
                                 font_size=9, color=(0, 0, 0, 255),
                                 x=x, y=y, anchor_x="center", anchor_y="center",
                                 batch=batch, group=BallRenderer._NUMBER_GROUP)

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
