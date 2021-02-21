#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import re
from io import TextIOWrapper
from typing import List
from pyfields import field, make_init
from DipTrace.reHelper import reJoin, searchSingleInt, searchSingleFloat, searchDoubleFloat, reInt
from DipTrace.units import deg2rad, mm2units, units2mm
from DipTrace.enums import DipTraceTerminalShapes
from DipTrace.point import DipTracePoint


class DipTraceTerminal:

    shape: DipTraceTerminalShapes = field(default=DipTraceTerminalShapes.Null, doc='Terminal shape type')
    x: float = field(default=0.0, doc='X coortinate')
    y: float = field(default=0.0, doc='Y coortinate')
    width: float = field(default=0.0, doc='Width')
    height: float = field(default=0.0, doc='Height')
    angle: float = field(default=0.0, doc='Angle')
    corner: float = field(default=0.0, doc='Corner')

    points: List[DipTracePoint] = field(default=[], doc='Shape points')

    __init__ = make_init()

    def setposition(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
        return self

    def move(self, x: float = 0.0, y: float = 0.0):
        self.x += mm2units(x)
        self.y += mm2units(y)
        return self

    def load(self, datafile: TextIOWrapper):
        while line := datafile.readline().strip():

            if line == ')':
                break

            elif tmp := re.search(reJoin(r'\(ShapePoints', reInt), line):
                while line := datafile.readline():
                    if line.strip() == ')':
                        break
                    if tmp := searchDoubleFloat(r'pt', line):
                        x = units2mm(tmp.group(1))
                        y = units2mm(tmp.group(2))
                        self.points.append(DipTracePoint(x, y))

            elif tmp := searchSingleInt(r'Type', line):
                self.shape = DipTraceTerminalShapes(int(tmp.group(1)))

            elif tmp := searchSingleFloat(r'X', line):
                self.x = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'Y', line):
                self.y = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'Angle', line):
                self.angle = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'ShapeWidth', line):
                self.width = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'ShapeHeight', line):
                self.height = float(tmp.group(1))

        return self

    def __str__(self) -> str:

        points = '\n'.join([str(point) for point in self.points])

        return ''.join([
            f'(PadTerminal\n'
            f'(Type {self.shape.value})\n',
            f'(X {mm2units(self.x):.4g})\n',
            f'(Y {mm2units(-self.y):.4g})\n',
            f'(Angle {deg2rad(self.angle):.4g})\n',
            f'(ShapeWidth {mm2units(self.width):.4g})\n',
            f'(ShapeHeight {mm2units(self.height):.4g})\n',
            f'(ShapeCorner {self.corner:.4g})\n',
            f'(ShapePoints {len(self.points)}\n{points}\n',
            ')\n',
            ')\n',
        ])


if __name__ == "__main__":
    pass
