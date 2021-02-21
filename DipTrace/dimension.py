#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from io import TextIOWrapper
from pyfields import field, make_init
from typing import List

from DipTrace.reHelper import searchSingleBool, searchSingleString, searchSingleInt, searchSingleFloat, searchSingleIntlList, searchSingleFloatList
from DipTrace.bool import DipTraceBool
from DipTrace.units import mm2units
from DipTrace.enums import DipTraceDimentionType, DipTraceDimentionUnits, DipTraceLayerType, DipTraceDimensionPointerType
from DipTrace.connection import DipTraceConnection


class DipTraceDimension:

    enabled: DipTraceBool = field(default=DipTraceBool(True), doc='Enabling dimension')
    locked: DipTraceBool = field(default=DipTraceBool(False), doc='Locking dimension')
    type: DipTraceDimentionType = field(default=DipTraceDimentionType.Free, doc='')
    layer: DipTraceLayerType = field(default=DipTraceLayerType.TopDimension, doc='')
    units: DipTraceDimentionUnits = field(default=DipTraceDimentionUnits.Default, doc='')
    show_units: DipTraceBool = field(default=DipTraceBool(False), doc='Show units')
    arrow_size: float = field(default=1.0, doc='')
    text: str = field(default='', doc='Text')
    vector: DipTraceBool = field(default=DipTraceBool(True), doc='Use vector font')
    font: str = field(default='Tahoma', doc='Text font')
    font_size: int = field(default=8, doc='Font size')
    font_width: float = field(default=1.0)
    font_scale: float = field(default=1.0)
    angle: float = field(default=0.0)
    group: int = field(default=0, doc='Group number')
    radius: float = field(default=0.0)
    pointer_mode: DipTraceDimensionPointerType = field(default=DipTraceDimensionPointerType.Coordinates)
    point_1_x: float = field(default=0.0, doc='Point 1 X coortinate')
    point_1_y: float = field(default=0.0, doc='Point 1 Y coortinate')
    point_2_x: float = field(default=0.0, doc='Point 2 X coortinate')
    point_2_y: float = field(default=0.0, doc='Point 2 Y coortinate')
    point_d_x: float = field(default=0.0, doc='Point D X coortinate')
    point_d_y: float = field(default=0.0, doc='Point D Y coortinate')
    connections: List[DipTraceConnection] = field(default=[])

    __init__ = make_init()

    @enabled.converter(accepts=bool)
    @locked.converter(accepts=bool)
    @show_units.converter(accepts=bool)
    @vector.converter(accepts=bool)
    def toDipTraceBool(self, field, value):
        return DipTraceBool(value)

    def move(self, x: float = 0.0, y: float = 0.0):
        self.point_d['x'] += mm2units(x)
        self.point_d['y'] += mm2units(y)
        for point in self.points:
            point['x'] += mm2units(x)
            point['y'] += mm2units(y)
        return self

    def load(self, datafile: TextIOWrapper):
        while line := datafile.readline().strip():

            if line == ')':
                break

            elif tmp := searchSingleBool(r'Enabled', line):
                self.enabled = tmp.group(1)

            elif tmp := searchSingleBool(r'Locked', line):
                self.locked = tmp.group(1)

            elif tmp := searchSingleInt(r'Type', line):
                self.type = DipTraceDimentionType(int(tmp.group(1)))

            elif tmp := searchSingleIntlList(r'Connected', line):
                id = int(tmp.group(1)) - 1
                value = int(tmp.group(2))
                while len(self.connections) < (id + 1):
                    self.addConnection()
                self.connections[id]['connected'] = value

            elif tmp := searchSingleIntlList(r'Object', line):
                id = int(tmp.group(1)) - 1
                value = int(tmp.group(2))
                while len(self.connections) < (id + 1):
                    self.addConnection()
                self.connections[id]['object'] = value

            elif tmp := searchSingleIntlList(r'SubObject', line):
                id = int(tmp.group(1)) - 1
                value = int(tmp.group(2))
                while len(self.connections) < (id + 1):
                    self.addConnection()
                self.connections[id]['sub_object'] = value

            elif tmp := searchSingleIntlList(r'Point', line):
                id = int(tmp.group(1)) - 1
                value = int(tmp.group(2))
                while len(self.connections) < (id + 1):
                    self.addConnection()
                self.connections[id]['point'] = value

            elif tmp := searchSingleInt(r'Layer', line):
                self.layer = DipTraceLayerType(int(tmp.group(1)))

            elif tmp := searchSingleFloatList(r'X', line):
                id = int(tmp.group(1)) - 1
                if id == 1:
                    self.point_1_x = float(tmp.group(2))
                elif id == 2:
                    self.point_2_x = float(tmp.group(2))

            elif tmp := searchSingleFloatList(r'Y', line):
                id = int(tmp.group(1)) - 1
                if id == 1:
                    self.point_1_y = float(tmp.group(2))
                elif id == 2:
                    self.point_2_y = float(tmp.group(2))

            elif tmp := searchSingleFloat(r'XD', line):
                self.point_d_x = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'YD', line):
                self.point_d_y = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'ArrowSize', line):
                self.arrow_size = float(tmp.group(1))

            elif tmp := searchSingleInt(r'Units', line):
                self.units = DipTraceDimentionUnits(int(tmp.group(1)))

            elif tmp := searchSingleBool(r'VectorFont', line):
                self.vector = tmp.group(1)

            elif tmp := searchSingleString(r'FontName', line):
                self.font_name = tmp.group(1)

            elif tmp := searchSingleInt(r'FontSize', line):
                self.font_size = int(tmp.group(1))

            elif tmp := searchSingleFloat(r'FontScale', line):
                self.font_scale = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'FontWidth', line):
                self.font_width = float(tmp.group(1))

            elif tmp := searchSingleBool(r'ShowUnits', line):
                self.show_units = tmp.group(1)

            elif tmp := searchSingleFloat(r'Angle', line):
                self.angle = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'ExternalRadius', line):
                self.radius = float(tmp.group(1))

            elif tmp := searchSingleInt(r'PointerMode', line):
                self.pointer_mode = DipTraceDimensionPointerType(
                    int(tmp.group(1)))

            elif tmp := searchSingleString(r'PointerText', line):
                self.text = tmp.group(1)

            elif tmp := searchSingleInt(r'Group', line):
                self.group = int(tmp.group(1))

        return self

    def __str__(self) -> str:

        connections = '\n'.join([str(self.connection[i]).format(
            i+1) for i in range(len(self.connections))])

        return ''.join([
            '(Dimension\n',
            f'(Enabled "{self.enabled}")\n',
            f'(Locked "{self.locked}")\n',
            f'(Type {self.type.value})\n',
            f'{connections}\n',
            f'(Layer {self.layer.value})\n',
            f'(X1 {self.point_1_x:.6g})\n(Y1 {self.point_1_y:.6g})\n',
            f'(X2 {self.point_2_x:.6g})\n(Y2 {self.point_2_y:.6g})\n',
            f'(XD {self.point_d_x:.6g})\n(YD {self.point_d_y:.6g})\n',
            f'(ArrowSize {self.arrow_size:.5g})\n',
            f'(Units {self.units.value})\n',
            f'(VectorFont "{self.vector}")\n',
            f'(FontName "{self.font_name}")\n',
            f'(FontSize {self.font_size})\n',
            f'(FontScale {self.font_scale:.5g})\n',
            f'(FontWidth {self.font_width:.5g})\n',
            f'(ShowUnits "{self.show_units}")\n',
            f'(Angle {self.angle:.5g})\n',
            f'(ExternalRadius {self.radius:.6g})\n',
            f'(PointerMode {self.pointer_mode.value})\n',
            f'(PointerText "{self.text}")\n',
            f'(Group {self.group})\n',
            ')'
        ])


if __name__ == "__main__":
    pass
