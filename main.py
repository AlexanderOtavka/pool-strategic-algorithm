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
port_manager = PortManager(json_data["port"])

window = Window(TABLE_WIDTH, TABLE_HEIGHT)
balls = BallGroup()

CORNER_POCKET_OFFSET = sqrt(CORNER_POCKET_OPENING ** 2 / 2)
pockets = [
    Pocket(Vector2D(0, 0),
           Vector2D(0, CORNER_POCKET_OFFSET),
           Vector2D(CORNER_POCKET_OFFSET, 0)),

    Pocket(Vector2D(TABLE_WIDTH, 0),
           Vector2D(-CORNER_POCKET_OFFSET, 0),
           Vector2D(0, CORNER_POCKET_OFFSET)),

    Pocket(Vector2D(TABLE_WIDTH, TABLE_HEIGHT),
           Vector2D(-CORNER_POCKET_OFFSET, 0),
           Vector2D(0, -CORNER_POCKET_OFFSET)),

    Pocket(Vector2D(0, TABLE_HEIGHT),
           Vector2D(0, -CORNER_POCKET_OFFSET),
           Vector2D(CORNER_POCKET_OFFSET, 0)),

    Pocket(Vector2D(TABLE_WIDTH / 2, 0),
           Vector2D(-SIDE_POCKET_OPENING / 2, 0),
           Vector2D(SIDE_POCKET_OPENING / 2, 0)),

    Pocket(Vector2D(TABLE_WIDTH / 2, TABLE_HEIGHT),
           Vector2D(-SIDE_POCKET_OPENING / 2, 0),
           Vector2D(SIDE_POCKET_OPENING / 2, 0)),
]

glClearColor(0.2, 0.6, 0.3, 1)


@window.event
def on_draw():
    window.clear()
    batch.draw()


@port_manager.event
def on_get_data(data):
    balls.update(data)

    possible_shots = []
    for ball in balls:
        possible_shots.extend(ball.get_possible_shots(balls, pockets))
    best_shot = sorted(possible_shots, key=lambda s: s.rating)[0]

    PrimitiveRenderer.update_all_vertex_lists()

    return best_shot.serialize()


@event_loop.event
def on_exit():
    port_manager.close()


if __name__ == "__main__":
    port_manager.open()
    run()
