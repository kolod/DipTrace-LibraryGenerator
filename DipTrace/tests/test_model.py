#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from DipTrace.enums import DipTrace3dModelUnits
import unittest
from DipTrace.model import DipTrace3dModel


class TestModel(unittest.TestCase):

    def test_1(self):
        model = DipTrace3dModel()
        model.filename = "LED-5mm-clear.step"
        model.origin_x = -0.175
        model.rotation_x = 90.0
        model.units = DipTrace3dModelUnits.Meters

        self.assertEqual(
            str(model),
            '(Model3D\n'
            '(Model3DFile "LED-5mm-clear.step")\n'
            '(pt 90 0 0 0 0 0 1 1 1 "N" "N" 0 -0.525 0 0 4934475 0 "N")\n'
            ')\n'
        )

    def test_2(self):
        model = DipTrace3dModel(
            filename="LED-5mm-clear.step",
            origin_x=-0.175,
            rotation_x=90.0,
            units=DipTrace3dModelUnits.Meters
        )

        self.assertEqual(
            str(model),
            '(Model3D\n'
            '(Model3DFile "LED-5mm-clear.step")\n'
            '(pt 90 0 0 0 0 0 1 1 1 "N" "N" 0 -0.525 0 0 4934475 0 "N")\n'
            ')\n'
        )


if __name__ == "__main__":
    unittest.main()
