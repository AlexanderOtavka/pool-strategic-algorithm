"""Utilities for calculating angles."""

from math import pi

__author__ = "Zander Otavka"


def simplify_radians(radians):
    radians %= 2 * pi
    if radians < 0:
        radians += pi
    return radians

