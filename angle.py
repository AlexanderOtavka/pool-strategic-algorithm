"""Utilities for calculating angles."""

from __future__ import division, print_function

from math import pi, ceil

__author__ = "Zander Otavka"


def positive_radians(radians):
    """
    :type radians: int or float
    :rtype: int or float
    """
    radians %= 2 * pi
    if radians < 0:
        radians += 2 * pi
    return radians


def negative_radians(radians):
    """
    :type radians: int or float
    :rtype: int or float
    """
    radians %= 2 * pi
    if radians > 0:
        radians -= 2 * pi
    return radians


def abs_radians(radians):
    """
    :type radians: int or float
    :rtype: int or float
    """
    return min(positive_radians(radians), -negative_radians(radians))


class Quadrant(object):
    FIRST = 0
    SECOND = 1
    THIRD = 2
    FOURTH = 3


class Hemisphere(object):
    EAST = (Quadrant.FIRST, Quadrant.FOURTH)
    NORTH = (Quadrant.FIRST, Quadrant.SECOND)
    WEST = (Quadrant.SECOND, Quadrant.THIRD)
    SOUTH = (Quadrant.THIRD, Quadrant.FOURTH)


def get_quadrant(angle):
    """
    :type angle: int or float
    :rtype: int
    """
    return int(ceil(angle / (pi / 2)) % 4)


def get_hemispheres(angle):
    """
    :type angle: int or float
    :rtype: collections.Iterable[(int, int)]
    """
    q = get_quadrant(angle)
    for h in (Hemisphere.EAST, Hemisphere.NORTH, Hemisphere.WEST,
              Hemisphere.SOUTH):
        if q in h:
            yield h
