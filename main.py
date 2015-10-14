"""
Find the best shot on the pool table.

Pool table is 54 x 108 inches.
"""

from __future__ import division

from pyglet.window import Window
from pyglet.clock import schedule_interval
from pyglet.app import run
from pyglet.gl import glClearColor

from portmanager import PortManager
from shot import Shot
from ball import BallGroup
from render import Renderer

# import pyglet

__author__ = "Zander Otavka"


window = Window(1080, 540)
port_manager = PortManager("/dev/foo", 9000)
balls = None


@window.event
def on_draw():
    glClearColor(0.2, 0.6, 0.3, 1)
    window.clear()
    # vlist = pyglet.graphics.vertex_list(
    #     2,
    #     ("v2i", ())
    # )
    Renderer.update_all_vertex_lists()
    Renderer.BATCH.draw()


@port_manager.event
def on_get_data(data):
    global balls
    balls = BallGroup.from_data(data)
    print balls
    port_manager.send_shot_data(Shot(angle=0, elevation=0, force=10))


schedule_interval(lambda dt: port_manager.listen(), 1/60)
run()
