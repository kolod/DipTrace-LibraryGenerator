#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from typing import List
from pyfields import field, make_init

from DipTrace.bool import DipTraceBool
from DipTrace.units import mm2units
from DipTrace.enums import DipTraceComponentShapeType, DipTraceTextAlign, DipTraceTextRotation
from DipTrace.point import DipTracePoint


class DipTraceComponentShape:

    shape: DipTraceComponentShapeType = field(default=DipTraceComponentShapeType.Null, doc='Shape type')
    points: List[DipTracePoint] = field(default=[], doc='Shape points')
    enabled: DipTraceBool = field(default=DipTraceBool(True), doc='Enabling dimension')
    locked: DipTraceBool = field(default=DipTraceBool(False), doc='Locking dimension')
    group: int = field(default=-1, doc='Shape group')
    line_width: float = field(default=0.25, doc='Line width, mm')
    vector: DipTraceBool = field(default=DipTraceBool(True), doc='Use vector font')
    text: str = field(default='', doc='Text')
    text_align: DipTraceTextAlign = field(default=DipTraceTextAlign.Center, doc='Text horizontal align.')
    text_spacing: float = field(default=1.2, doc='Text spacing')
    text_rotation: DipTraceTextRotation = field(default=DipTraceTextRotation.Default, doc='Text angle')
    text_horiz: float = field(default=0.0)
    text_vert: float = field(default=0.0)
    font: str = field(default='Tahoma', doc='Text font')
    font_size: int = field(default=8, doc='Font size')

    __init__ = make_init()

    @enabled.converter(accepts=bool)
    @locked.converter(accepts=bool)
    @vector.converter(accepts=bool)
    def toDipTraceBool(self, field, value):
        return DipTraceBool(value)

    def move(self, x: float = 0.0, y: float = 0.0):
        for point in self.points:
            point.move(x, y)
        return self

    def __str__(self):

        points = '\n'.join([str(point) for point in self.points])
        points_new = '\n'.join([str(point) for point in self.points])
        text_lines = '\n'.join(f'(pt "{line}")' for line in (
            self.text if len(self.text) else "\n").splitlines())

        return ''.join([
            f'(Shape {"{0}"}\n',
            f'(Enabled "{self.enabled}")\n',
            f'(Locked "{self.locked}")\n',
            f'(VectorFont "{self.vector}")\n',
            '(FontWidth 0)\n',
            '(FontScale 0)\n',
            '(Orientation 0)\n',
            f'(Type {self.shape.value})\n',
            f'(FontSize {self.font_size})\n',
            '(FontColor 0)\n',
            '(FontType 0)\n',
            f'(FontName "{self.font}")\n',
            f'(Name "{self.text}")\n',
            f'(Width {mm2units(self.line_width):0.6g})\n',
            f'(Points\n{points}\n)\n',
            f'(TextAngle {self.text_rotation.value})\n',
            f'(TextHorz {self.text_horiz:0.6g})\n',
            f'(TextVert {self.text_vert:0.6g})\n',
            f'(TextAlign {self.text_align.value})\n',
            f'(LineSpacing {self.text_spacing})\n',
            '(Group -1)\n',
            f'(TextLines\n{text_lines}\n)\n',
            f'(Points_New\n{points_new}\n)\n',
            ')\n'
        ])


if __name__ == "__main__":
    pass
