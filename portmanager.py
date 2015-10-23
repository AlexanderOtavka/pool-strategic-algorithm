"""Interface between the XBee and the algorithm."""

from __future__ import division, print_function

from serial import Serial
from xbee import XBee
from pyglet.event import EventDispatcher

__author__ = "Zander Otavka"


FAKE_DATA = [
    200, 100,
    400, 285,
    600, 200,
    800, 400,
    # 230, 450,
    # 120, 300,
    # 110, 130,
    # 345, 139,
    # 824, 460,
    # 000, 000,
    # 400, 250,
    # 600, 100,
    # 800, 204,
    # 230, 250,
    # 120, 200,
    # 110, 230,
]


class PortManager(EventDispatcher):
    """
    :type _serial_port: Serial
    :type _xbee: XBee
    """

    _serial_port = None
    _xbee = None

    def __init__(self, port):
        """
        :type port: unicode
        """
        # self._serial_port = Serial(port, 9600)
        print("open port: {}".format(port))
        self._serial_port = Serial()

    def send_data(self, data):
        """
        :type data: tuple
        """
        # TODO: implement PortManager.send_data
        print("send data: {} to xbee: {}".format(data, self._xbee))

    def open(self):
        def on_get_data_callback(data):
            # TODO: parse the data into an array
            array = data
            self.dispatch_event("on_get_data", array)
        # self._xbee = XBee(self._serial_port, callback=on_get_data_callback)
        on_get_data_callback(FAKE_DATA)

    def close(self):
        print("closing port {}".format(self._serial_port))
        self._xbee.halt()
        self._serial_port.close()

    # noinspection PyMethodMayBeStatic
    def on_get_data(self, data):
        """
        :type data: list[int]
        """
        pass

PortManager.register_event_type("on_get_data")
