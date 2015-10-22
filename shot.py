"""Contains the Shot class."""

from __future__ import division, print_function

from math import pi, tan

from vector2d import Vector2D
from angle import Hemisphere
from ball import Ball, BallGroup
from render import ShotSegmentRenderer
from target import ShotTarget
from pocket import Pocket

__author__ = "Zander Otavka"


class ImpossibleShotError(Exception):
    pass


class ShotSegment(object):
    """
    :type _position: Vector2D
    :type _radius: float
    :type _vector1: Vector2D
    :type _vector2: Vector2D
    :type _renderer: ShotSegmentRenderer
    """

    _position = None
    _radius = None
    _vector1 = None
    _vector2 = None
    _renderer = None

    def __init__(self, target, actor_ball, balls):
        """
        :type target: ShotTarget
        :type actor_ball: Ball
        :type balls: BallGroup
        """
        self._position = actor_ball.position
        self._radius = actor_ball.RADIUS

        # get a pair of vectors pointing at the pocket
        v1 = target.point1 - actor_ball.position
        v2 = target.point2 - actor_ball.position

        # find ball radius offsets
        if (abs(v2.direction - (v1.direction + pi / 2)) <
                abs(v2.direction - (v1.direction - pi / 2))):
            sign = 1
        else:
            sign = -1
        off1 = Vector2D.from_polar(Ball.RADIUS * 2,
                                   v1.direction - sign * pi / 2)
        off2 = Vector2D.from_polar(Ball.RADIUS * 2,
                                   v2.direction + sign * pi / 2)

        # derive a system of inequalities from the vectors and offsets
        p1 = actor_ball.position + off1
        p2 = actor_ball.position + off2
        v1quad = v1.direction.quadrant
        v2quad = v2.direction.quadrant
        hem = None

        def get_east_west_cmp():
            if v1.normalized().y < v2.normalized().y:
                return 1, -1
            else:
                return -1, 1
        if v1quad in Hemisphere.EAST and v2quad in Hemisphere.EAST:
            hem = Hemisphere.EAST
            cmp1, cmp2 = get_east_west_cmp()
        elif v1quad in Hemisphere.WEST and v2quad in Hemisphere.WEST:
            hem = Hemisphere.WEST
            cmp1, cmp2 = get_east_west_cmp()
        elif (v1.direction - v2.direction > pi / 2 ==
              v1quad in Hemisphere.WEST):
            cmp1 = cmp2 = 1
        else:
            cmp1 = cmp2 = -1

        def is_possible_collision(x, y):
            in_correct_hemisphere = (
                (Vector2D(x, y) - self.position).direction.quadrant in hem)
            return (cmp(y - p1.y, tan(v1.direction) * (x - p1.x)) == cmp1 and
                    cmp(y - p2.y, tan(v2.direction) * (x - p2.x)) == cmp2 and
                    (in_correct_hemisphere if hem is not None else True))

        # restrict shot angles based on obstacles
        for other_ball in balls:
            if is_possible_collision(*other_ball.position):
                p1_to_ball = other_ball.position - p1
                p2_to_ball = other_ball.position - p2
                a1 = abs(p1_to_ball.direction - v1.direction)
                a2 = abs(p2_to_ball.direction - v2.direction)
                if min(a1, a2) > abs(v1.direction - v2.direction):
                    raise ImpossibleShotError("Shot fully obstructed by balls.")
                if a1 < a2:
                    v1.direction = p1_to_ball.direction
                else:
                    v2.direction = p2_to_ball.direction
                # assert not is_possible_collision(*other_ball.position)

        # save shot vectors
        self._vector1 = v1
        self._vector2 = v2
        self._renderer = ShotSegmentRenderer(
            actor_ball.number, self.position, v1, v2)

    @property
    def position(self):
        return self._position

    @property
    def vector1(self):
        return self._vector1

    @property
    def vector2(self):
        return self._vector2

    @property
    def target(self):
        """
        :rtype: ShotTarget
        """
        p1 = self.position + Vector2D.from_polar(-self._radius * 2,
                                                 self.vector1.direction)
        p2 = self.position + Vector2D.from_polar(-self._radius * 2,
                                                 self.vector2.direction)
        f = (self.vector1 + self.vector2) / 2
        # noinspection PyTypeChecker
        return ShotTarget(p1, p2, f)

    def delete(self):
        self._renderer.delete()


class Shot(object):

    _segments = None

    def __init__(self, *segments):
        """
        :type segments: tuple[ShotSegment]
        """
        self._segments = segments

    @property
    def angle(self):
        return 0

    @property
    def elevation(self):
        return 0

    @property
    def force(self):
        return 10

    @property
    def rating(self):
        return 0

    def to_array(self):
        """
        :rtype: tuple
        """
        return self.angle, self.force, self.elevation

    def delete(self):
        for segment in self._segments:
            segment.delete()


class ShotGroup(list):

    def __init__(self):
        super(ShotGroup, self).__init__()

    @property
    def best_shot(self):
        """
        :rtype: Shot
        """
        assert len(self) > 0
        return sorted(self, key=lambda s: s.rating)[0]

    def update(self, pockets, balls):
        """
        :type pockets: list[Pocket]
        :type balls: BallGroup
        """
        self.delete()
        balls = balls.copy()
        cue = balls.pop(0)
        for actor_ball in balls:
            obstacle_balls = balls.copy()
            obstacle_balls.remove(actor_ball)
            for pocket in pockets:
                try:
                    self.append(Shot(
                        ShotSegment(pocket.target, actor_ball, obstacle_balls)
                    ))
                except ImpossibleShotError:
                    continue

    def delete(self):
        for shot in self:
            shot.delete()
        self[:] = []
