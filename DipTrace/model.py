#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import re
from io import TextIOWrapper
from pyfields import field, make_init
from DipTrace.reHelper import searchSingleString, reJoin, reFloat, reBool
from DipTrace.bool import DipTraceBool
from DipTrace.units import mm2units, units2mm
from DipTrace.enums import DipTrace3dModelType, DipTrace3dModelUnits


class DipTrace3dModel:

    type: DipTrace3dModelType = field(default=DipTrace3dModelType.File, doc='')
    units: DipTrace3dModelUnits = field(default=DipTrace3dModelUnits.Wings3D, doc='')
    height: float = field(default=0.0, doc='Height')
    color: int = field(default=4934475, doc='Color')
    origin_x: float = field(default=0.0, doc='Origin X coordinate')
    origin_y: float = field(default=0.0, doc='Origin Y coordinate')
    filename: str = field(default='', doc='')
    x: float = field(default=0.0, doc='X coordinate')
    y: float = field(default=0.0, doc='Y coordinate')
    z: float = field(default=0.0, doc='Z coordinate')
    rotation_x: float = field(default=0.0, doc='Rotation X coordinate')
    rotation_y: float = field(default=0.0, doc='Rotation Y coordinate')
    rotation_z: float = field(default=0.0, doc='Rotation Z coordinate')
    scale_x: float = field(default=1.0, doc='Scale X coordinate')
    scale_y: float = field(default=1.0, doc='Scale Y coordinate')
    scale_z: float = field(default=1.0, doc='Scale Z coordinate')
    search: DipTraceBool = field(default=DipTraceBool(False), doc='Search model in folders')
    flip: DipTraceBool = field(default=DipTraceBool(False), doc='Flip Z and Y axis')
    keep_pins: DipTraceBool = field(default=DipTraceBool(False), doc='Keep all model pins')

    __init__ = make_init()

    @search.converter(accepts=bool)
    @flip.converter(accepts=bool)
    @keep_pins.converter(accepts=bool)
    def toDipTraceBool(self, field, value):
        return DipTraceBool(value)

    def load(self, datafile: TextIOWrapper):
        while line := datafile.readline().strip():

            if line == ')':
                break

            if tmp := searchSingleString(r'Model3DFile', line):
                self.filename = tmp.group(1)

            elif tmp := re.search(reJoin(r'pt', reFloat, reFloat, reFloat, reFloat, reFloat, reFloat,
                                         reFloat, reFloat, reFloat, reBool, reBool, reFloat, reFloat,
                                         reFloat, reFloat, reFloat, reFloat), line):
                self.rotation_x = float(tmp.group(1))
                self.rotation_y = float(tmp.group(2))
                self.rotation_z = float(tmp.group(3))
                self.x = units2mm(float(tmp.group(4)))
                self.y = units2mm(float(tmp.group(5)))
                self.z = units2mm(float(tmp.group(6)))
                self.scale_x = float(tmp.group(7))
                self.scale_y = float(tmp.group(8))
                self.scale_z = float(tmp.group(9))
                self.flip = tmp.group(10)
                self.search = tmp.group(11)
                self.units = DipTrace3dModelUnits(int(tmp.group(12)))
                self.origin_x = float(tmp.group(13))
                self.origin_y = float(tmp.group(14))
                self.height = float(tmp.group(15))
                self.color = int(tmp.group(16))
                self.type = DipTrace3dModelType(int(tmp.group(17)))

        return self

    def __str__(self):
        return ''.join([
            '(Model3D\n',
            f'(Model3DFile "{self.filename}")\n',
            f'(pt {self.rotation_x:.4g} {self.rotation_y:.4g} {-self.rotation_z+0:.4g} ',
            f'{mm2units(self.x):.4g} {mm2units(-self.y):.4g} {mm2units(-self.z):.4g} ',
            f'{self.scale_x:.4g} {self.scale_y:.4g} {self.scale_z:.4g} ',
            f'"{self.flip}" "{self.search}" ',
            f'{self.units.value} {mm2units(self.origin_x):.5g} {mm2units(self.origin_y):.5g} {self.height:.5g} ',
            f'{self.color} {self.type.value} "{self.keep_pins}")\n',
            ')\n',
        ])


if __name__ == "__main__":
    pass
