"""Randomly generate an arrangement of balls."""

from __future__ import division, print_function

from random import randint, random
from math import ceil

from ball import Ball
from pocket import Pocket
from vector2d import Vector2D

__author__ = "Zander Otavka"


def get_ball_positions(number, width, height, pockets, chance_of_death=.2,
                       unkillable_balls=(0, 8)):
    """
    :type number: int
    :type width: int
    :type height: int
    :type pockets: list[Pocket]
    :type chance_of_death: float
    :type unkillable_balls: tuple[int]
    """
    points = []
    for i in range(number):
        while len(points) <= i:
            if i not in unkillable_balls and random() < chance_of_death:
                points.append(Vector2D())
            else:
                point = Vector2D((randint(ceil(Ball.RADIUS),
                                          int(width - Ball.RADIUS)),
                                  randint(ceil(Ball.RADIUS),
                                          int(height - Ball.RADIUS))))
                for other_point in points:
                    if (other_point - point).magnitude < Ball.RADIUS * 2:
                        break
                else:
                    points.append(point)
    return sum((list(point) for point in points), list())
