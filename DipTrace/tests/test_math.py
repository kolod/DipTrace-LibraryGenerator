#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import unittest
from DipTrace.math import getArcSize, isAngleCrossArc
from DipTrace.point import DipTracePoint
from DipTrace.units import units2mm


class TestMath(unittest.TestCase):

    def test_isAngleCrossArc(self):
        self.assertEqual(isAngleCrossArc(15, 45, -45), True)
        self.assertEqual(isAngleCrossArc(15, -45, 45), False)
        self.assertEqual(isAngleCrossArc(170, 135, -135), False)
        self.assertEqual(isAngleCrossArc(170, -135, 135), True)

    def test_getSize_SWN(self):
        print('\ntest_getSize_SWN')

        points = [
            DipTracePoint(x=units2mm(2.5607), y=units2mm(2.1213)),
            DipTracePoint(x=units2mm(-2.5607), y=units2mm(0)),
            DipTracePoint(x=units2mm(2.5607), y=units2mm(-2.1213)),
        ]

        shape_max_x, shape_min_x, shape_max_y, shape_min_y = getArcSize(points)
        width = shape_max_x - shape_min_x
        height = shape_max_y - shape_min_y
        print(width, height)

        self.assertAlmostEqual(width, units2mm(5.1213), delta=0.001)
        self.assertAlmostEqual(height, units2mm(6.0), delta=0.001)

    def test_getSize_E(self):
        print('\ntest_getSize_E')

        points = [
            DipTracePoint(x=units2mm(-0.4393), y=units2mm(2.1213)),
            DipTracePoint(x=units2mm(0.4393), y=units2mm(0)),
            DipTracePoint(x=units2mm(-0.4393), y=units2mm(-2.1213)),
        ]

        shape_max_x, shape_min_x, shape_max_y, shape_min_y = getArcSize(points)
        width = shape_max_x - shape_min_x
        height = shape_max_y - shape_min_y
        print(width, height)

        self.assertAlmostEqual(width, units2mm(0.8787), delta=0.001)
        self.assertAlmostEqual(height, units2mm(4.2426), delta=0.001)


if __name__ == "__main__":
    unittest.main()
