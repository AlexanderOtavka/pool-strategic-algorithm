#!/usr/bin/env python
"""
Find the best shot on the pool table.

Each pixel is .1 inches.
"""

from __future__ import division, print_function

import json
from math import sqrt

from pyglet.window import Window
from pyglet.app import run, event_loop
from pyglet.gl import glClearColor

from portmanager import PortManager
from ball import BallGroup
from shot import ShotGroup
from render import PrimitiveRenderer, batch
from pocket import Pocket
from vector2d import Vector2D

__author__ = "Zander Otavka"


TABLE_WIDTH = 1080
TABLE_HEIGHT = 540

CORNER_POCKET_OPENING = 45
SIDE_POCKET_OPENING = 50


with open("config.json", "r") as f:
    json_data = json.load(f)
port = PortManager(json_data["port"])

window = Window(TABLE_WIDTH, TABLE_HEIGHT)
balls = BallGroup()
shots = ShotGroup()

CORNER_POCKET_OFFSET = sqrt(CORNER_POCKET_OPENING ** 2 / 2)
SIDE_POCKET_DEPTH = sqrt(CORNER_POCKET_OFFSET ** 2 / 2)
pockets = [
    Pocket(Vector2D(0, 0),
           Vector2D(0, CORNER_POCKET_OFFSET),
           Vector2D(CORNER_POCKET_OFFSET, 0),
           name="Bottom Left"),

    Pocket(Vector2D(TABLE_WIDTH, 0),
           Vector2D(-CORNER_POCKET_OFFSET, 0),
           Vector2D(0, CORNER_POCKET_OFFSET),
           name="Bottom Right"),

    Pocket(Vector2D(TABLE_WIDTH, TABLE_HEIGHT),
           Vector2D(-CORNER_POCKET_OFFSET, 0),
           Vector2D(0, -CORNER_POCKET_OFFSET),
           name="Top Right"),

    Pocket(Vector2D(0, TABLE_HEIGHT),
           Vector2D(0, -CORNER_POCKET_OFFSET),
           Vector2D(CORNER_POCKET_OFFSET, 0),
           name="Top Left"),

    Pocket(Vector2D(TABLE_WIDTH / 2, -SIDE_POCKET_DEPTH),
           Vector2D(-SIDE_POCKET_OPENING / 2, SIDE_POCKET_DEPTH),
           Vector2D(SIDE_POCKET_OPENING / 2, SIDE_POCKET_DEPTH),
           name="Bottom Center"),

    Pocket(Vector2D(TABLE_WIDTH / 2, TABLE_HEIGHT + SIDE_POCKET_DEPTH),
           Vector2D(-SIDE_POCKET_OPENING / 2, -SIDE_POCKET_DEPTH),
           Vector2D(SIDE_POCKET_OPENING / 2, -SIDE_POCKET_DEPTH),
           name="Top Center"),
]

glClearColor(0.2, 0.6, 0.3, 1)


@window.event
def on_draw():
    window.clear()
    batch.draw()


@port.event
def on_get_data(data):
    balls.update(data)
    shots.update(pockets, balls)
    PrimitiveRenderer.update_all_vertex_lists()
    return shots.best_shot.to_array()


@event_loop.event
def on_exit():
    port.close()
    balls.delete()
    shots.delete()


if __name__ == "__main__":
    port.open()
    run()
