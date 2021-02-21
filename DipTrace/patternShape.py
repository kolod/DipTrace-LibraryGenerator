#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import re
from io import TextIOWrapper
from typing import Literal, List, AnyStr
from pyfields import field
from pyfields.init_makers import init_fields

from DipTrace import reJoin, reInt, reFloat, reBool, reString, searchSingleBool, searchSingleFloat, searchSingleInt, searchDoubleFloat
from DipTrace.bool import DipTraceBool
from DipTrace.enums import DipTracePatternShapeType, DipTraceLayerType, DipTraceTextAlign, DipTraceMarkingType, DipTraceTextRotation
from DipTrace.units import units2mm, mm2units_p, units2mm_p
from DipTrace.point import DipTracePoint


class DipTracePatternShape(object):

    isComponent: bool = False

    shape: DipTracePatternShapeType = field(native=True, default=DipTracePatternShapeType.Null, doc='Shape type')
    enabled: DipTraceBool = field(default=DipTraceBool(True), doc='Enabling shape')
    locked: DipTraceBool = field(default=DipTraceBool(False), doc='Locking shape')
    vector: DipTraceBool = field(default=DipTraceBool(True), doc='Use vector font')
    all_layers: DipTraceBool = field(default=DipTraceBool(False), doc='Show the shape on the all layers.')
    layer: DipTraceLayerType = field(default=DipTraceLayerType.TopSilk, doc='Layer')
    width: float = field(default=-1.0, doc='Shape width')
    group: int = field(default=0, doc='Group number')
    line_width: float = field(default=0.25, doc='Line width (Set -1 for the layer default width).')
    text: str = field(default='', doc='Text')
    font: str = field(default='Tahoma', doc='Text font')
    font_size: int = field(default=8, doc='Font size')
    text_align: DipTraceTextAlign = field(default=DipTraceTextAlign.Left, doc='Text horizontal align.')
    text_rotation: DipTraceTextRotation = field(default=DipTraceTextRotation.Default, doc='Text angle')
    text_spacing: float = field(default=1.2, doc='Text spacing')
    text_horiz: float = field(default=0.0)
    text_vert: float = field(default=0.0)
    text_width: float = field(default=0.0)
    text_marking: DipTraceMarkingType = field(default=DipTraceMarkingType.Text, doc='Text marking type')
    font_line_width: float = field(default=0.0, doc='Vector line width:\n\t-1 = Bold\n\t-2 = Normal\n\t-3 = Thin\n\tPositive value = actual width in mm * 3')
    points: List[DipTracePoint] = field(default=[], doc='Points for DipTrace format lower then version 4.0.')
    points_new: List[DipTracePoint] = field(default=[], doc='Points for DipTrace format version 4.0 or above.')

    @enabled.converter(accepts=bool)
    @locked.converter(accepts=bool)
    @vector.converter(accepts=bool)
    def toDipTraceBool(self, field, value):
        return DipTraceBool(value)

    @init_fields
    def __init__(self, match: re.Match[AnyStr] = None):
        if match:
            self.shape = DipTracePatternShapeType(int(match.group(1)))
            self.locked = match.group(2)
            self.text = match.group(10)
            self.font = match.group(11)
            self.vector = match.group(12)
            self.font_size = int(match.group(13))
            self.text_width = units2mm_p(float(match.group(14)))
            self.line_width = units2mm_p(float(match.group(15)))
        super().__init__()

    def recalculate(self, origin_x: float, origin_y: float, width: float, height: float):
        self.points = []
        for point in self.points_new:
            self.points.append(DipTracePoint(
                x=(point.x + origin_x) / width,
                y=(point.y + origin_y) / height,
                convert=False
            ))

            point.x, point.y = point.x + origin_x, point.y + origin_y

        return self

    def move(self, x: float = 0.0, y: float = 0.0):
        for point in self.points:
            point.move(x, y)
        return self

    @staticmethod
    def pattern() -> Literal:
        return reJoin(r'Shape', reInt, reBool,
                      reFloat, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat,
                      reString, reString, reBool, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat)

    def load(self, datafile: TextIOWrapper):
        pos = datafile.tell()

        while line := datafile.readline().strip():

            if tmp := searchSingleFloat(r'Width', line):
                self.width = float(tmp.group(1))

            elif tmp := searchSingleInt(r'Layer', line):
                self.layer = DipTraceLayerType(int(tmp.group(1)))

            elif tmp := searchSingleFloat(r'TextHorz', line):
                self.text_horiz = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'TextVert', line):
                self.text_vert = float(tmp.group(1))

            elif tmp := searchSingleInt(r'TextAlign', line):
                self.text_align = DipTraceTextAlign(int(tmp.group(1)))

            elif tmp := searchSingleInt(r'Group', line):
                self.group = int(tmp.group(1))

            elif tmp := searchSingleFloat(r'LineSpacing', line):
                self.text_spacing = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'TextAngle', line):
                self.text_rotation = DipTraceTextRotation(float(tmp.group(1)))

            elif tmp := searchSingleBool(r'AllLayers', line):
                self.all_layers = tmp.group(1)

            elif line == '(Points':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if tmp := searchDoubleFloat(r'pt', line):
                        self.points.append(DipTracePoint(
                            x=float(tmp.group(1)),
                            y=float(tmp.group(2)),
                            convert=False
                        ))

            elif line == '(Points_New':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if tmp := searchDoubleFloat(r'pt', line):
                        self.points_new.append(DipTracePoint(
                            x=units2mm(float(tmp.group(1))),
                            y=units2mm(float(tmp.group(2))),
                            convert=True
                        ))

            elif line.startswith('(Shape ') or line == ')':
                datafile.seek(pos)  # Save position
                break

            pos = datafile.tell()   # Restore last position

        return self

    def __str__(self):

        s = [
            round(self.points[0].x, 4) + 0 if len(self.points) >= 1 else 0,
            round(-self.points[0].y, 4) + 0 if len(self.points) >= 1 else 0,
            round(self.points[1].x, 4) + 0 if len(self.points) >= 2 else 0,
            round(-self.points[1].y, 4) + 0 if len(self.points) >= 2 else 0,
            round(self.points[2].x, 4) + 0 if len(self.points) >= 3 else 0,
            round(-self.points[2].y, 4) + 0 if len(self.points) >= 3 else 0,
        ]

        layer = self.layer.value
        if layer > 10:
            layer = 1

        points = '\n'.join([str(point) for point in self.points])
        points_new = '\n'.join([str(point) for point in self.points_new])

        if self.isComponent:
            return ''.join([
                f'(Shape {self.shape.value} "{self.locked}" {layer} {s[0]:.6g} {s[1]:.6g} {s[2]:.6g} {s[3]:.6g} {s[4]:.6g} {s[5]:.6g} ',
                f'"{self.text}" "{self.font}" "{self.vector}" {self.font_size} {self.text_width:.6g} {mm2units_p(self.font_line_width):.6g} ',
                f'{self.text_rotation.value} {mm2units_p(self.line_width):.6g} {self.text_marking.value})\n',
                f'(Point\n{points}\n)\n' if len(self.points) else '',
                f'(Width {mm2units_p(self.line_width):.6g})\n',
                f'(Layer {self.layer.value})\n',
                f'(TextHorz {self.text_horiz:.6g})\n',
                f'(TextVert {self.text_vert:.6g})\n',
                f'(TextAlign {self.text_align.value})\n',
                f'(LineSpacing {self.text_spacing:.6g})\n',
                f'(TextAngle {self.text_rotation.value:.6g})\n',
                f'(Points_New\n{points_new}\n)\n' if len(
                    self.points_new) else '',
                f'(AllLayers "{self.all_layers}")\n',
                f'(Group {self.group})\n'
            ])
        else:
            return ''.join([
                f'(Shape {self.shape.value} "{self.locked}" {layer} {s[0]:.6g} {s[1]:.6g} {s[2]:.6g} {s[3]:.6g} {s[4]:.6g} {s[5]:.6g} ',
                f'"{self.text}" "{self.font}" "{self.vector}" {self.font_size} {self.text_width:.6g} {mm2units_p(self.font_line_width):.6g} ',
                f'{self.text_rotation.value} {mm2units_p(self.line_width):.6g} {self.text_marking.value})\n',
                f'(Points\n{points}\n)\n' if len(self.points) else '',
                f'(Width {mm2units_p(self.width):.6g})\n',
                f'(Layer {self.layer.value})\n',
                f'(TextHorz {self.text_horiz:.6g})\n',
                f'(TextVert {self.text_vert:.6g})\n',
                f'(TextAlign {self.text_align.value})\n',
                f'(LineSpacing {self.text_spacing:.6g})\n',
                f'(TextAngle {self.text_rotation.value:.6g})\n',
                f'(Points_New\n{points_new}\n)\n' if len(
                    self.points_new) else '',
                f'(AllLayers "{self.all_layers}")\n',
                f'(Group {self.group})\n'
            ])


if __name__ == "__main__":
    pass
