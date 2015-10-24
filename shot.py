"""Contains the Shot class."""

from __future__ import division, print_function

from math import pi, tan, cos

from vector2d import Vector2D
from angle import Hemisphere
from ball import Ball, BallGroup
from render import ShotSegmentRenderer, ShotRenderer
from target import ShotTarget
from pocket import Pocket

__author__ = "Zander Otavka"


class ImpossibleShotError(Exception):
    pass


class ShotSegment(object):
    """
    :type _position: Vector2D
    :type _vector1: Vector2D
    :type _vector2: Vector2D
    :type _target: ShotTarget
    :type _renderer: ShotSegmentRenderer
    """

    _position = None
    _vector1 = None
    _vector2 = None
    _target = None
    _renderer = None

    def __init__(self, target, actor_ball, balls):
        """
        :type target: ShotTarget
        :type actor_ball: Ball
        :type balls: BallGroup
        """
        self._position = actor_ball.position

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
                ((Vector2D((x, y)) - self.position).direction.quadrant in hem)
                if hem is not None else True
            )
            return (cmp(y - p1.y, tan(v1.direction) * (x - p1.x)) == cmp1 and
                    cmp(y - p2.y, tan(v2.direction) * (x - p2.x)) == cmp2 and
                    in_correct_hemisphere)

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

        # calculate necessary force to transfer to target, and sum with the
        # length of the shot
        v1_v2_avg = Vector2D(v1 + v2) / 2
        force_offset_angle = abs(target.force.direction - v1_v2_avg.direction)
        if force_offset_angle > pi / 2:
            raise ImpossibleShotError("Positive force cannot be applied due to "
                                      "shot angle.")
        force_magnitude = (target.force.magnitude / cos(force_offset_angle) +
                           v1_v2_avg.magnitude)

        # calculate target from shot vectors and necessary force
        target_p1 = self.position + Vector2D.from_polar(-Ball.RADIUS * 2,
                                                        v1.direction)
        target_p2 = self.position + Vector2D.from_polar(-Ball.RADIUS * 2,
                                                        v2.direction)
        target_force = Vector2D.from_polar(force_magnitude, v1_v2_avg.direction)
        self._target = ShotTarget(target_p1, target_p2, target_force)

        # save shot vectors
        self._vector1 = v1
        self._vector2 = v2

        # create renderer
        self._renderer = ShotSegmentRenderer(actor_ball.number,
                                             self.position, self.target,
                                             self.vector1, self.vector2)

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
        return self._target

    def highlight(self):
        self._renderer.highlight()

    def delete(self):
        self._renderer.delete()


class Shot(object):
    """
    :type _segments: list(ShotSegment)
    """

    _segments = None
    _renderer = None

    def __init__(self, target, target_ball, cue, balls):
        """
        :type target: ShotTarget
        :type target_ball: Ball
        :type cue: Ball
        :type balls: BallGroup
        """
        self._segments = []
        try:
            self._segments.append(ShotSegment(target, target_ball, balls))
            self._segments.append(ShotSegment(self._segments[0].target, cue,
                                              balls))
        except ImpossibleShotError:
            self.delete()
            raise

    @property
    def angle(self):
        return self._segments[-1].target.force.direction

    @property
    def elevation(self):
        return 0

    @property
    def force_strength(self):
        return self._segments[-1].target.force.magnitude

    @property
    def rating(self):
        """
        :rtype: float
        """
        target = self._segments[-1].target
        dist = (target.point1 - target.point2).magnitude
        return dist

    def highlight(self):
        for segment in self._segments:
            segment.highlight()

    def to_array(self):
        return self.angle, self.force_strength, self.elevation

    def delete(self):
        for segment in self._segments:
            segment.delete()
        self._segments = None

    def __str__(self):
        return "<shot.Shot - {}>".format(self.rating)


class ShotGroup(list):

    def __init__(self):
        super(ShotGroup, self).__init__()

    @property
    def best_shot(self):
        """
        :rtype: Shot
        """
        assert len(self) > 0
        sorted_list = sorted(self, key=lambda s: s.rating)
        return sorted_list[-1]

    def update(self, pockets, balls):
        """
        :type pockets: list[Pocket]
        :type balls: BallGroup
        """
        self.delete()
        balls = balls.copy()
        cue = balls.pop(0)
        for target_ball in balls:
            obstacle_balls = balls.copy()
            obstacle_balls.remove(target_ball)
            for pocket in pockets:
                try:
                    self.append(Shot(pocket.target, target_ball, cue,
                                     obstacle_balls))
                except ImpossibleShotError:
                    continue

    def delete(self):
        for shot in self:
            shot.delete()
        self[:] = []
