#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.


from pyfields import field, make_init
from DipTrace.units import mm2units


class DipTracePoint(object):

    x: float = field(native=True, default=0.0, doc='X coortinate')
    y: float = field(native=True, default=0.0, doc='Y coortinate')
    convert: bool = field(native=True, default=True, doc='If the conversion flag set to the "True" str() method do coordinates conversion.')

    __init__ = make_init()

    def move(self, x: float = 0.0, y: float = 0.0):
        self.x += x
        self.y += y
        return self

    def __str__(self) -> str:
        x = mm2units(self.x) if self.convert else self.x
        y = mm2units(self.y) if self.convert else self.y
        return f'(pt {round(x, 4):g} {round(-y+0, 4):g})'


if __name__ == "__main__":
    pass
