#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from pyfields import field, make_init
from DipTrace.bool import DipTraceBool
from DipTrace.units import mm2units
from DipTrace.enums import DipTracePinType, DipTracePinElectric, DipTracePinOrientation


class DipTracePin(object):

    type: DipTracePinType = field(default=DipTracePinType.Undefined, doc='Pin type')
    name: str = field(default='', doc='Pin name')
    number: int = field(default=0, doc='Pin number')
    locked: DipTraceBool = field(default=DipTraceBool(False), doc='Lock pin')
    enabled: DipTraceBool = field(default=DipTraceBool(True), doc='Enable pin')
    show: DipTraceBool = field(default=DipTraceBool(False), doc='Show pin name')
    electric: DipTracePinElectric = field(default=DipTracePinElectric.Undefined, doc='')
    orientation: DipTracePinOrientation = field(default=DipTracePinOrientation.Right, doc='Pin orientation')
    x: float = field(default=0.0, doc='X coordinate')
    y: float = field(default=0.0, doc='Y coordinate')
    length: float = field(default=0.0, doc='pin length')

    __init__ = make_init()

    def __str__(self):
        return ''.join([
            f'(Pin {"{0}"} {mm2units(self.x):.6g} {mm2units(self.y):.6g}\n',
            f'(Enabled "{self.enabled}")\n',
            f'(Locked "{self.locked}")\n',
            '(ModelSig "")\n',
            f'(Type {self.type.value})\n',
            f'(Orientation {self.orientation.value})\n',
            f'(Number {self.number})\n',
            f'(Length {mm2units(self.length):.6g})\n',
            f'(Name "{self.name if len(self.name) else str(self.number)}")\n',
            f'(StringNumber "{self.number}")\n',
            f'(ShowName "{self.show}")\n',
            '(PinNumXShift 0)\n',
            '(PinNumYShift 0)\n',
            '(PinNamexShift 0)\n',
            '(PinNameYShift 0)\n',
            f'(ElectricType {self.electric.value})\n',
            '(NameFontSize 5)\n',
            '(NameFontWidth -2)\n',
            '(NameFontScale 1)\n',
            '(SignalDelay 0)\n',
            '(Group -1)\n',
            '(PinNumRotate 0)\n',
            '(PinNameRotate 0)\n',
            ')\n',
        ])


if __name__ == "__main__":
    pass
