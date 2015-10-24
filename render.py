"""Abstracts away rendering using subclasses of `Renderer`."""

from __future__ import division, print_function

from abc import ABCMeta, abstractmethod, abstractproperty
from math import pi, sin, cos, ceil, copysign

from pyglet.graphics import Batch, Group, OrderedGroup
from pyglet.graphics.vertexdomain import VertexList
from pyglet.gl import GL_LINE_LOOP, GL_TRIANGLE_FAN, GL_QUADS
from pyglet.text import Label

from angle import Angle
from vector2d import Vector2D
from target import ShotTarget

__author__ = "Zander Otavka"


batch = Batch()


class Renderer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def delete(self):
        pass


class PrimitiveRenderer(Renderer):
    """
    :type _vertex_list: VertexList
    """
    __metaclass__ = ABCMeta

    _renderers = []

    _group = None
    _vertex_list = None
    _color = None

    def __init__(self, color, group=None):
        """
        :type color: (int, int, int)
        :type group: Group
        """
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

    @abstractproperty
    def mode(self):
        """
        :rtype: int
        """
        pass

    def delete(self):
        self._vertex_list.delete()
        self._vertex_list = None
        PrimitiveRenderer._renderers.remove(self)

    def set_group(self, group):
        batch.migrate(self._vertex_list, self.mode, Group(parent=group), batch)

    @abstractmethod
    def update_vertex_list(self):
        pass


class PolygonRenderer(PrimitiveRenderer):

    _points = None
    _mode = None

    def __init__(self, color, points, mode=None, group=None):
        """
        :type color: (int, int, int)
        :type points: tuple[Vector2D]
        :type mode: int
        :type group: Group
        """
        super(PolygonRenderer, self).__init__(color, group)
        self._points = points
        if mode is None:
            mode = GL_LINE_LOOP
        self._mode = mode
        self._create_vertex_list()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, new):
        self._points = new

    @property
    def mode(self):
        return self._mode

    def _create_vertex_list(self):
        self._vertex_list = batch.add(len(self.points), self._mode, self._group,
                                      "v2f", "c3B")

    def update_vertex_list(self):
        if self._vertex_list.get_size() != len(self.points):
            self._vertex_list.resize(len(self.points))

        self._vertex_list.vertices[:] = [number for point in self.points
                                         for number in point]
        self._vertex_list.colors[:] = self.color * len(self.points)

    def delete(self):
        super(PolygonRenderer, self).delete()


class CirclePointGroup(object):
    __metaclass__ = ABCMeta

    _circle_renderer = None

    def __init__(self, circle_renderer=None):
        """
        :type circle_renderer: CircleRenderer
        """
        self._circle_renderer = circle_renderer

    @property
    def circle_renderer(self):
        return self._circle_renderer

    @circle_renderer.setter
    def circle_renderer(self, new):
        self._circle_renderer = new

    @abstractproperty
    def point_count(self):
        """
        :rtype: int
        """
        pass

    @abstractproperty
    def points(self):
        """
        :rtype: collections.Iterable[Vector2D]
        """
        pass

    def delete(self):
        self.circle_renderer = None


class CirclePoint(CirclePointGroup):

    _offset = None

    def __init__(self, offset, circle_renderer=None):
        """
        :type offset: Vector2D
        :type circle_renderer: CircleRenderer
        """
        super(CirclePoint, self).__init__(circle_renderer)
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, new):
        self._offset = new

    @property
    def point_count(self):
        return 1

    @property
    def points(self):
        return [self.offset + self.circle_renderer.position]


class CircleArc(CirclePointGroup):

    _start_angle = None
    _end_angle = None

    def __init__(self, start_angle, end_angle, circle_renderer=None):
        """
        :type start_angle: Angle
        :type end_angle: Angle
        :type circle_renderer: CircleRenderer
        """
        super(CircleArc, self).__init__(circle_renderer)
        self._start_angle = start_angle
        self._end_angle = end_angle

    @property
    def start_angle(self):
        return self._start_angle

    @start_angle.setter
    def start_angle(self, new):
        self._start_angle = new

    @property
    def end_angle(self):
        return self._end_angle

    @end_angle.setter
    def end_angle(self, new):
        self._end_angle = new

    @property
    def point_count(self):
        return int(abs(ceil(float(self.end_angle - self.start_angle) /
                            (2 * pi) * self.circle_renderer.resolution)))

    @property
    def points(self):
        for i in range(max(self.point_count, 2)):
            angle = (i * ((self.end_angle - self.start_angle) /
                          (self.point_count - 1)) +
                     self.start_angle)
            x = cos(angle) * self.circle_renderer.radius
            y = sin(angle) * self.circle_renderer.radius
            yield Vector2D((x, y)) + self.circle_renderer.position


class CircleRenderer(PrimitiveRenderer):

    DEFAULT_RESOLUTION = 50

    _position = None
    _radius = None
    _circle_points = None
    _resolution = None

    def __init__(self, color, position, radius, circle_points, resolution=None,
                 group=None):
        """
        :type color: (int, int, int)
        :type position: Vector2D
        :type radius: float or int
        :type circle_points: list[CirclePointGroup]
        :type resolution: int
        :type group: Group
        """
        super(CircleRenderer, self).__init__(color, group)
        self._position = position
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
    def new_circle(cls, color, position, radius, resolution=None, group=None):
        """
        :type color: (int, int, int)
        :type position: Vector2D
        :type radius: float or int
        :type resolution: int
        :type group: Group
        """
        circle_points = [CircleArc(Angle(0), Angle(1.99 * pi))]
        return cls(color, position, radius, circle_points, resolution, group)

    @classmethod
    def new_sector(cls, color, position, radius, start_angle, end_angle,
                   resolution=None, group=None):
        """
        :type color: (int, int, int)
        :type position: Vector2D
        :type radius: float or int
        :type start_angle: Angle
        :type end_angle: Angle
        :type resolution: int
        :type group: Group
        """
        circle_points = [CirclePoint(Vector2D()),
                         CircleArc(start_angle, end_angle)]
        return cls(color, position, radius, circle_points, resolution, group)

    @classmethod
    def new_segment(cls, color, position, radius, start_angle, end_angle,
                    resolution=None, group=None):
        """
        :type color: (int, int, int)
        :type position: Vector2D
        :type radius: float or int
        :type start_angle: Angle
        :type end_angle: Angle
        :type resolution: int
        :type group: Group
        """
        circle_points = [CircleArc(start_angle, end_angle)]
        return cls(color, position, radius, circle_points, resolution, group)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new):
        self._position = new

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

    @property
    def mode(self):
        return GL_TRIANGLE_FAN

    def _create_vertex_list(self):
        self._vertex_list = batch.add(self.point_count, self.mode,
                                      self._group, "v2f", "c3B")

    def update_vertex_list(self):
        if self._vertex_list.get_size() != self.point_count:
            self._vertex_list.resize(self.point_count)

        points = []
        for circle_point in self.circle_points:
            # noinspection PyTypeChecker
            points.extend(circle_point.points)

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
        (255, 255, 255),  # Q  - white
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

    _BALL_GROUP = OrderedGroup(3)
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

    def __init__(self, number, position, radius):
        """
        :type number: int
        :type position: Vector2D
        :type radius: int or float
        """
        self._circle = CircleRenderer.new_circle(
            BallRenderer.COLORS[number], position, radius,
            BallRenderer._CIRCLE_RESOLUTION, BallRenderer._CIRCLE_GROUP)
        if number > 8:
            self._top_stripe = CircleRenderer.new_segment(
                (255, 255, 255), position, radius,
                Angle(pi / 4), Angle(3 * pi / 4),
                BallRenderer._CIRCLE_RESOLUTION, BallRenderer._STRIPE_GROUP)
            self._bottom_stripe = CircleRenderer.new_segment(
                (255, 255, 255), position, radius,
                Angle(-3 * pi / 4), Angle(-pi / 4),
                BallRenderer._CIRCLE_RESOLUTION, BallRenderer._STRIPE_GROUP)
        if number > 0:
            self._number_bg = CircleRenderer.new_circle(
                (255, 255, 255), position, 6, BallRenderer._BALL_BG_RESOLUTION,
                BallRenderer._NUMBER_BG_GROUP)
            self._number = Label(str(number), font_name="Times New Roman",
                                 font_size=9, color=(0, 0, 0, 255),
                                 x=position.x, y=position.y,
                                 anchor_x="center", anchor_y="center",
                                 batch=batch, group=BallRenderer._NUMBER_GROUP)

    @property
    def position(self):
        return self._circle.position

    @position.setter
    def position(self, new):
        self._circle.position = new
        if self._top_stripe is not None:
            self._top_stripe.position = new
        if self._bottom_stripe is not None:
            self._bottom_stripe.position = new
        if self._number is not None:
            self._number.x, self._number.y = new
            self._number_bg.position = new

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


class PocketRenderer(PrimitiveRenderer):

    COLOR = (0, 0, 0)
    FRONT_DISTANCE = 3

    _POCKET_GROUP = OrderedGroup(0)

    _position = None
    _offset1 = None
    _offset2 = None

    def __init__(self, position, offset1, offset2):
        """
        :type position: Vector2D
        :type offset1: Vector2D
        :type offset2: Vector2D
        """
        super(PocketRenderer, self).__init__(PocketRenderer.COLOR,
                                             PocketRenderer._POCKET_GROUP)
        self._position = position
        self._offset1 = offset1
        self._offset2 = offset2
        self._create_vertex_list()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new):
        self._position = new

    @property
    def offset1(self):
        return self._offset1

    @offset1.setter
    def offset1(self, new):
        self._offset1 = new

    @property
    def offset2(self):
        return self._offset2

    @offset2.setter
    def offset2(self, new):
        self._offset2 = new

    @property
    def mode(self):
        return GL_QUADS

    def _create_vertex_list(self):
        self._vertex_list = batch.add(4, self.mode, self._group, "v2f", "c3B")

    def update_vertex_list(self):
        offset_angle = (self.offset2 - self.offset1).direction
        p1_to_back = -self.offset1
        p1_to_back.direction -= offset_angle
        back_distance = p1_to_back.y
        back_offset_vector = Vector2D.from_polar(back_distance,
                                                 offset_angle + pi / 2)
        front_distance = -copysign(PocketRenderer.FRONT_DISTANCE, back_distance)
        front_offset_vector = Vector2D.from_polar(front_distance,
                                                  offset_angle + pi / 2)
        points = [self.offset1 + back_offset_vector + self.position,
                  self.offset2 + back_offset_vector + self.position,
                  self.offset2 + front_offset_vector + self.position,
                  self.offset1 + front_offset_vector + self.position]
        self._vertex_list.vertices[:] = [number for point in points
                                         for number in point]
        self._vertex_list.colors[:] = self.color * 4

    def delete(self):
        super(PocketRenderer, self).delete()


class ShotSegmentRenderer(Renderer):

    HIGHLIGHT_COLOR = (50, 50, 50)

    _SHOT_SEGMENT_GROUP = OrderedGroup(1)
    _HIGHLIGHTED_GROUP = OrderedGroup(2)

    _renderer = None

    def __init__(self, ball_number, position, target, vector1, vector2):
        """
        :type ball_number: int
        :type position: Vector2D
        :type target: ShotTarget
        :type vector1: Vector2D
        :type vector2: Vector2D
        """
        color = BallRenderer.COLORS[ball_number]
        self._renderer = PolygonRenderer(
            color, (position + vector1, target.point1,
                    target.point2, position + vector2),
            GL_LINE_LOOP, ShotSegmentRenderer._SHOT_SEGMENT_GROUP)

    def highlight(self):
        self._renderer.color = ShotSegmentRenderer.HIGHLIGHT_COLOR
        self._renderer.set_group(ShotSegmentRenderer._HIGHLIGHTED_GROUP)
        # new_renderer = PolygonRenderer(
        #     ShotSegmentRenderer.HIGHLIGHT_COLOR,
        #     self._renderer.points,
        #     GL_TRIANGLE_FAN,
        #     ShotSegmentRenderer._SHOT_SEGMENT_GROUP
        # )
        # self._renderer.delete()
        # self._renderer = new_renderer

    def delete(self):
        self._renderer.delete()
