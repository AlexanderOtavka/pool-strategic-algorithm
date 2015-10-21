"""Interface between the XBee and the algorithm."""

from __future__ import division, print_function

from serial import Serial
from xbee import XBee

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
    # 200, 200,
    # 400, 250,
    # 600, 100,
    # 800, 204,
    # 230, 250,
    # 120, 200,
    # 110, 230,
]


class PortManager(object):

    _serial_port = None
    _xbee = None
    _on_get_data = None

    def __init__(self, port):
        """
        :type port: unicode
        """
        # self._serial_port = Serial(port, 9600)
        print("open port: {}".format(port))
        self._serial_port = Serial()

    def _send_data(self, data):
        """
        :type data: tuple
        """
        # TODO: implement PortManager._send_data
        print("send data: {} to xbee: {}".format(data, self._xbee))

    def event(self, func):
        """
        :type func: (list[int]) -> tuple
        """
        if func.__name__ == "on_get_data":
            def on_get_data(data):
                # TODO: parse the data into an array
                self._send_data(func(data))
            self._on_get_data = on_get_data
            return on_get_data

    def open(self):
        assert self._on_get_data is not None

        # self._xbee = XBee(self._serial_port, callback=self._on_get_data)
        self._on_get_data(FAKE_DATA)

    def close(self):
        print("closing port {}".format(self._serial_port))
        self._xbee.halt()
        self._serial_port.close()
