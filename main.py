"""
Find the best shot on the pool table.

Pool table is 54 x 108 inches.
"""

from __future__ import division

import json

from pyglet.window import Window
from pyglet.clock import schedule_interval
from pyglet.app import run, event_loop
from pyglet.gl import glClearColor

from portmanager import PortManager
from shot import Shot
from ball import BallGroup
from render import Renderer

__author__ = "Zander Otavka"

with open("port.json", "r") as f:
    json_data = json.load(f)
port_manager = PortManager(json_data["device"], json_data["port"])

window = Window(1080, 540)
balls = None

glClearColor(0.2, 0.6, 0.3, 1)


@window.event
def on_draw():
    window.clear()
    Renderer.update_all_vertex_lists()
    Renderer.BATCH.draw()


@port_manager.event
def on_get_data(data):
    global balls
    balls = BallGroup.from_data(data)
    print balls
    port_manager.send_shot_data(Shot(angle=0, elevation=0, force=10))


@event_loop.event
def on_exit():
    port_manager.close()


schedule_interval(lambda dt: port_manager.listen(), 1/60)
run()
