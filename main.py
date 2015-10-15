#!/usr/bin/env python
"""
Find the best shot on the pool table.

Pool table is 54 x 108 inches.  Each pixel is .1 inches.
"""

from __future__ import division

import json

from pyglet.window import Window
from pyglet.app import run, event_loop
from pyglet.gl import glClearColor

from portmanager import PortManager
from shot import Shot
from ball import BallGroup
from render import PrimitiveRenderer, batch

__author__ = "Zander Otavka"


with open("config.json", "r") as f:
    json_data = json.load(f)
port_manager = PortManager(json_data["port"])

window = Window(1080, 540)
balls = BallGroup()

glClearColor(0.2, 0.6, 0.3, 1)


@window.event
def on_draw():
    window.clear()
    batch.draw()


@port_manager.event
def on_get_data(data):
    balls.update(data)
    shot = Shot(angle=0, elevation=0, force=10)
    PrimitiveRenderer.update_all_vertex_lists()
    return shot.serialize()


@event_loop.event
def on_exit():
    port_manager.close()


port_manager.open()
run()
