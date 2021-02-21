#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from typing import List
from pyfields import field, make_init
from DipTrace.pin import DipTracePin
from DipTrace.units import mm2units
from DipTrace.bool import DipTraceBool
from DipTrace.enums import DipTraceComponentPartType
from DipTrace.componentLayer import DipTraceComponentLayer
from DipTrace.componentShape import DipTraceComponentShape


class DipTraceComponentPart:

    shapes: List[DipTraceComponentShape] = field(default=[], doc='Shapes')
    layers: List[DipTraceComponentLayer] = field(default=[], doc='Layers')
    pins: List[DipTracePin] = field(default=[], doc='Pins')
    name: str = field(default='', doc='Component name')
    part_name: str = field(default='', doc='Part name')
    ref: str = field(default='', doc='Part ref')
    value: str = field(default='', doc='Part value')
    type: DipTraceComponentPartType = field(default=DipTraceComponentPartType.Normal, doc='Part type')
    enabled: DipTraceBool = field(default=DipTraceBool(True), doc='Is part enabled')
    show_numbers: int = field(default=0, doc='Show pin numbers')
    origin_x: float = field(default=0.0, doc='Origin X')
    origin_y: float = field(default=0.0, doc='Origin Y')
    width: float = field(default=0.0, doc='Width')
    height: float = field(default=0.0, doc='Height')

    __init__ = make_init()

    def setOrigin(self, x: float = 0.0, y: float = 0.0):
        self.origin_x = mm2units(x)
        self.origin_y = mm2units(y)
        return self

    def setSize(self, width: float = 0.0, height: float = 0.0):
        self.width = mm2units(width)
        self.height = mm2units(height)
        return self

    def __str__(self) -> str:

        pins = '\n'.join([str(self.pins[i]).format(i) for i in range(len(self.pins))])
        shapes = '\n'.join([str(self.shapes[i]).format(i) for i in range(len(self.shapes))])
        groups = '\n'
        layers = '\n'.join([str(layer) for layer in self.layers])
        user_fields = '\n'

        return ''.join([
            f'(Part "{self.name}" "{self.ref}"\n',
            f'(Enabled "{self.enabled}")\n',
            f'(PartType {self.type.value})\n',
            f'(PartName "{self.part_name}")\n',
            f'(ShowNumbers {self.show_numbers})\n',
            f'(Type {self.type.value})\n',
            '(Number1 0)\n',
            '(Number2 0)\n',
            f'(Width {mm2units(self.width)})\n',
            f'(Height {mm2units(self.height)})\n',
            f'(Value "{self.value}")\n',
            '(LockProperties "N")\n',
            '(OriginX {mm2units(self.origin_x):.6g})\n',
            f'(OriginY {mm2units(self.origin_y):.6g})\n',
            '(Datasheet "")\n',
            '(ModelType 0)\n',
            '(ModelString "")\n',
            '(ModelBody\n)\n',
            '(Manufacturer "")\n',
            '(CategoryName "Connectors")\n',
            '(CategoryIndex -1)\n',
            '(CategoryTypes 0\n)\n',
            '(SubfolderIndex 1)\n',
            '(Verification "N" "N" "N" "N" "N" "N" "N")\n',
            f'(Pins\n{pins}\n)\n' if len(self.pins) else '',
            f'(Shapes\n{shapes}\n)\n' if len(self.shapes) else '',
            f'(Groups\n{groups}\n)\n',
            f'(Layers\n{layers}\n)\n',
            f'(UserFields\n{user_fields}\n)\n',
            ')\n'
        ])


if __name__ == "__main__":
    pass
