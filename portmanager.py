"""Interface between the XBee and the algorithm."""

from serial import Serial
from xbee import XBee

__author__ = "Zander Otavka"


class PortManager(object):

    _serial = None
    _xbee = None
    _on_get_data = None
    _old_data = None

    def __init__(self, device, port):
        # ser = Serial(device, port)
        self._serial = Serial()
        self._xbee = XBee(self._serial)

    def _get_data(self):
        data = [
            200, 100,
            400, 300,
            600, 200,
            800, 400,
            230, 450,
            120, 300,
            110, 130,
            345, 139,
            824, 460,
            200, 200,
            400, 250,
            600, 100,
            800, 204,
            230, 250,
            120, 200,
            110, 230,
        ]
        if data == self._old_data:
            return None
        else:
            print "load data from xbee: {}".format(self._xbee)
            self._old_data = data
            return data

    def send_shot_data(self, shot):
        print "send data to xbee: {}".format(self._xbee)
        print shot.serialize()

    def event(self, func):
        if func.__name__ == "on_get_data":
            self._on_get_data = func
        return func

    def listen(self):
        assert self._on_get_data is not None

        data = self._get_data()
        if data is not None:
            self._on_get_data(data)

    def close(self):
        self._serial.close()
