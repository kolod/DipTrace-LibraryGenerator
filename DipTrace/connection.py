#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from pyfields import field, make_init
from DipTrace.bool import DipTraceBool


class DipTraceConnection:

    connected: DipTraceBool = field(default=DipTraceBool(True), doc='')
    object: int = field(default=0, doc='')
    sub_object: int = field(default=0, doc='')
    point: int = field(default=0, doc='')

    __init__ = make_init()

    @connected.converter(accepts=bool)
    def toDipTraceBool(self, field, value):
        return DipTraceBool(value)

    def __str__(self) -> str:
        return ''.join([
            f'(Connected{"{0}"} {self.connected})\n',
            f'(Object{"{0}"} {self.object})\n',
            f'(SubObject{"{0}"} {self.sub_object})\n',
            f'(Point{"{0}"} {self.point})\n',
        ])


if __name__ == "__main__":
    pass
