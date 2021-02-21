#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import unittest
import re
from DipTrace.pad import DipTracePad
from DipTrace.model import DipTrace3dModelType
from DipTrace.enums import DipTracePadShapesNew, DipTracePatternShapeType, DipTraceTerminalShapes, DipTraceTextRotation
from DipTrace.hole import DipTraceHole
from DipTrace.bool import DipTraceBool
from DipTrace.point import DipTracePoint
from DipTrace.model import DipTrace3dModel
from DipTrace.terminal import DipTraceTerminal
from DipTrace.patternShape import DipTracePatternShape
from DipTrace.patternLayer import DipTracePatternLayer
from DipTrace.pattern import DipTracePattern


class TestPad(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        self.pad = DipTracePad()
        super().__init__(methodName=methodName)

    def test_calculateOld(self):

        self.maxDiff = None

        self.pad.shape_new = DipTracePadShapesNew.Rectangle
        self.pad.width = 2.5
        self.pad.height = 1.5
        self.pad.pad_corner = 10
        self.pad.calculateOld()

        if match := re.search(r'\(Points((?:\n.+)*)\n\)$', str(self.pad), re.M):

            print(str(self.pad))
            self.assertEqual(
                match.group(1),
                '\n'
                '(pt -3.3 -2.25)\n'
                '(pt 3.3 -2.25)\n'
                '(pt 3.4165 -2.2347)\n'
                '(pt 3.525 -2.1897)\n'
                '(pt 3.6182 -2.1182)\n'
                '(pt 3.6897 -2.025)\n'
                '(pt 3.7347 -1.9165)\n'
                '(pt 3.75 -1.8)\n'
                '(pt 3.75 1.8)\n'
                '(pt 3.7347 1.9165)\n'
                '(pt 3.6897 2.025)\n'
                '(pt 3.6182 2.1182)\n'
                '(pt 3.525 2.1897)\n'
                '(pt 3.4165 2.2347)\n'
                '(pt 3.3 2.25)\n'
                '(pt -3.3 2.25)\n'
                '(pt -3.4165 2.2347)\n'
                '(pt -3.525 2.1897)\n'
                '(pt -3.6182 2.1182)\n'
                '(pt -3.6897 2.025)\n'
                '(pt -3.7347 1.9165)\n'
                '(pt -3.75 1.8)\n'
                '(pt -3.75 -1.8)\n'
                '(pt -3.7347 -1.9165)\n'
                '(pt -3.6897 -2.025)\n'
                '(pt -3.6182 -2.1182)\n'
                '(pt -3.525 -2.1897)\n'
                '(pt -3.4165 -2.2347)'
            )


class TestDipTraceHole(unittest.TestCase):

    def __init__(self, methodName: str) -> None:
        self.hole = DipTraceHole()
        super().__init__(methodName=methodName)

    def test_hole_1(self):
        self.assertEqual(str(self.hole), '(Hole "Y" "N" 0 0 0 0 0)')

    def test_hole_2(self):
        self.hole.locked = True
        self.hole.x = 2.0
        self.hole.y = -1.0
        self.hole.keepout = 4.0
        self.hole.hole = 3.0
        self.hole.group = -1
        self.hole.recalculate(-1.0, -1.5)
        self.assertEqual(str(self.hole), '(Hole "Y" "Y" 3 -1.5 12 9 -1)')


class TestDipTracePoint(unittest.TestCase):

    def __init__(self, methodName: str) -> None:
        self.point = DipTracePoint()
        super().__init__(methodName=methodName)

    def test_point_1(self):
        self.assertEqual(str(self.point), '(pt 0 0)')

    def test_point_2(self):
        self.point.x = 1.0
        self.point.y = 2.0
        self.point.convert = True
        self.assertEqual(str(self.point), '(pt 3 -6)')

    def test_point_3(self):
        self.point.x = 2.3
        self.point.y = 3.8
        self.point.convert = True
        self.assertEqual(str(self.point), '(pt 6.9 -11.4)')

    def test_point_4(self):
        self.point.x = 2.3
        self.point.y = 3.8
        self.point.convert = False
        self.assertEqual(str(self.point), '(pt 2.3 -3.8)')


class TestDipTraceBool(unittest.TestCase):

    def test_bool(self):
        flag = DipTraceBool(True)
        self.assertEqual(str(flag), 'Y')
        flag.state = False
        self.assertEqual(str(flag), 'N')


class TestDipTrace3dModel(unittest.TestCase):

    def test_model(self):

        model = DipTrace3dModel()
        self.assertEqual(
            str(model),
            '(Model3D\n'
            '(Model3DFile "")\n'
            '(pt 0 0 0 0 0 0 1 1 1 "N" "N" -1 0 0 0 4934475 0 "N")\n'
            ')\n'
        )

        model.x = 1
        model.y = 2
        model.z = 3
        model.rotation_x = 45
        model.rotation_y = 30
        model.rotation_z = 60
        model.keep_pins = True
        model.type = DipTrace3dModelType.Generator

        self.assertEqual(
            str(model),
            '(Model3D\n'
            '(Model3DFile "")\n'
            '(pt 45 30 -60 3 -6 -9 1 1 1 "N" "N" -1 0 0 0 4934475 1 "Y")\n'
            ')\n'
        )


class TesDipTraceTerminal(unittest.TestCase):

    def test_terminal(self):

        terminal = DipTraceTerminal()

        self.assertEqual(
            str(terminal),
            '(PadTerminal\n'
            '(Type 0)\n'
            '(X 0)\n'
            '(Y 0)\n'
            '(Angle 0)\n'
            '(ShapeWidth 0)\n'
            '(ShapeHeight 0)\n'
            '(ShapeCorner 0)\n'
            '(ShapePoints 0\n\n'
            ')\n'
            ')\n'
        )

        terminal.shape = DipTraceTerminalShapes.Rectangle
        terminal.width = 0.64
        terminal.height = 0.64
        terminal.x = 0.1
        terminal.y = 0.2
        terminal.corner = 10.0
        terminal.angle = 15.0

        self.assertEqual(
            str(terminal),
            '(PadTerminal\n'
            '(Type 2)\n'
            '(X 0.3)\n'
            '(Y -0.6)\n'
            '(Angle 0.2618)\n'
            '(ShapeWidth 1.92)\n'
            '(ShapeHeight 1.92)\n'
            '(ShapeCorner 10)\n'
            '(ShapePoints 0\n\n'
            ')\n'
            ')\n'
        )


class TesDipTracePatternShape(unittest.TestCase):

    def test_pattern_shape(self):
        shape = DipTracePatternShape()
        shape.shape = DipTracePatternShapeType.Poliline
        shape.width = 0.2
        shape.font_size = 10
        shape.line_width = 0.2
        shape.text_width = 1.0
        shape.text_rotation = DipTraceTextRotation.Rotate_90
        shape.font_line_width = -2
        shape.vector = False
        shape.text_horiz = -1
        shape.text_vert = -1
        shape.group = -1
        shape.points_new.append(DipTracePoint(x=-0.5, y=2))
        shape.points_new.append(DipTracePoint(x=-2.5, y=0))
        shape.points_new.append(DipTracePoint(x=-0.5, y=-2))
        shape.points_new.append(DipTracePoint(x=2.5, y=0))
        shape.points_new.append(DipTracePoint(x=0, y=2))
        shape.recalculate(0.0, 0.0, 5.0, 4.0)

        self.assertEqual(
            str(shape),
            '(Shape 8 "N" 0 -0.1 -0.5 -0.5 0 -0.1 0.5 "" "Tahoma" "N" 10 1 -2 1 0.6 0)\n'
            '(Points\n'
            '(pt -0.1 -0.5)\n'
            '(pt -0.5 0)\n'
            '(pt -0.1 0.5)\n'
            '(pt 0.5 0)\n'
            '(pt 0 -0.5)\n'
            ')\n'
            '(Width 0.6)\n'
            '(Layer 0)\n'
            '(TextHorz -1)\n'
            '(TextVert -1)\n'
            '(TextAlign -1)\n'
            '(LineSpacing 1.2)\n'
            '(TextAngle 1)\n'
            '(Points_New\n'
            '(pt -1.5 -6)\n'
            '(pt -7.5 0)\n'
            '(pt -1.5 6)\n'
            '(pt 7.5 0)\n'
            '(pt 0 -6)\n'
            ')\n'
            '(AllLayers "N")\n'
            '(Group -1)\n'
        )

        DipTracePatternShape.isComponent = True
        self.assertEqual(
            str(shape),
            '(Shape 8 "N" 0 -0.1 -0.5 -0.5 0 -0.1 0.5 "" "Tahoma" "N" 10 1 -2 1 0.6 0)\n'
            '(Point\n'
            '(pt -0.1 -0.5)\n'
            '(pt -0.5 0)\n'
            '(pt -0.1 0.5)\n'
            '(pt 0.5 0)\n'
            '(pt 0 -0.5)\n'
            ')\n'
            '(Width 0.6)\n'
            '(Layer 0)\n'
            '(TextHorz -1)\n'
            '(TextVert -1)\n'
            '(TextAlign -1)\n'
            '(LineSpacing 1.2)\n'
            '(TextAngle 1)\n'
            '(Points_New\n'
            '(pt -1.5 -6)\n'
            '(pt -7.5 0)\n'
            '(pt -1.5 6)\n'
            '(pt 7.5 0)\n'
            '(pt 0 -6)\n'
            ')\n'
            '(AllLayers "N")\n'
            '(Group -1)\n'
        )


class TestDipTracePatternLayer(unittest.TestCase):

    def test_pattern_layer(self):

        layer = DipTracePatternLayer()

        self.assertEqual(
            str(layer),
            '(Layer\n'
            '(Enabled "Y")\n'
            '(Number 0)\n'
            '(Pads\n\n)\n'
            '(Shapes\n\n)\n'
            '(Holes\n\n)\n'
            ')\n'
        )

        layer.number = 1
        layer.holes.append(2)
        layer.pads.extend([1, 2, 4, 5, 6, 10])
        layer.shapes.append(2)
        layer.shapes.append(3)

        self.assertEqual(
            str(layer),
            '(Layer\n'
            '(Enabled "Y")\n'
            '(Number 1)\n'
            '(Pads\n'
            '(pt 1)\n'
            '(pt 2)\n'
            '(pt 4)\n'
            '(pt 5)\n'
            '(pt 6)\n'
            '(pt 10)\n'
            ')\n'
            '(Shapes\n'
            '(pt 2)\n'
            '(pt 3)\n'
            ')\n'
            '(Holes\n'
            '(pt 2)\n'
            ')\n'
            ')\n'
        )


class TestDipTracePattern(unittest.TestCase):

    def test_pattern(self):

        self.maxDiff = None

        pattern = DipTracePattern()

        self.assertEqual(
            str(pattern),
            '(Pattern "" ""\n'
            '(Value "")\n'
            '(VariableParameter1 "N")\n'
            '(VariableParameter2 "N")\n'
            '(VariableParameter3 "N")\n'
            '(VariableParameter4 "N")\n'
            '(Width 0)\n'
            '(Height 0)\n'
            '(Spacing1 0)\n'
            '(Spacing2 0)\n'
            '(VariableParameter5 "N")\n'
            '(Spacing3 0)\n'
            '(LockProperties "N")\n'
            '(PatternOrientation 0)\n'
            '(Number1 0.0)\n'
            '(Number2 0.0)\n'
            '(Type 0)\n'
            '(PadWidth 0)\n'
            '(PadHeight 0)\n'
            '(PadShape 1)\n'
            '(SurfacePad "N")\n'
            '(PadHole 0)\n'
            '(PadHoleH 0)\n'
            '(PadHoleType 0)\n'
            '(PadPoints\n'
            '\n'
            ')\n'
            '(PadShape_New 0)\n'
            '(PadAngle 0)\n'
            '(PadShape_X 0)\n'
            '(PadShape_Y 0)\n'
            '(PadCorner 0)\n'
            '(PadWidth_New 0)\n'
            '(PadHeight_New 0)\n'
            '(PadTerminalCount 0\n'
            '\n'
            ')\n'
            '(PadMask_Percent 0)\n'
            '(PadMask_EdgeGap 0)\n'
            '(PadMask_SegmentGap 0)\n'
            '(PadMask_SegmentSide 0)\n'
            '(TopMask_State 0)\n'
            '(BotMask_State 0)\n'
            '(TopPaste_State 0)\n'
            '(BotPaste_State 0)\n'
            '(CustomSwell_New 0)\n'
            '(RecoveryCode 0)\n'
            '(PadMask_TopSegments 0\n'
            ')\n'
            '(PadMask_BotSegments 0\n'
            ')\n'
            '(OriginX 0)\n'
            '(OriginY 0)\n'
            '(OriginCross "N")\n'
            '(OriginCircle "N")\n'
            '(OriginCommon 0)\n'
            '(OriginCourtyard 0)\n'
            '(Name_Description "")\n'
            '(Name_Unique "")\n'
            '(RecoveryCode "")\n'
            '(RecoveryCode_Generator "N")\n'
            '(RecoveryCode_Model "N")\n'
            '(Manufacturer "")\n'
            '(Pattern_Groups\n'
            ')\n'
            '(Layers\n'
            '\n'
            ')\n'
            '(UserFields\n'
            '\n'
            ')\n'
            '(Dimensions\n'
            '\n'
            ')\n'
            '\n'
            '(Mounting 0)\n'
            '(Datasheet "")\n'
            '(CategoryName "")\n'
            '(CategoryIndex 0)\n'
            '(CategoryTypes 0\n'
            '\n'
            ')\n'
            '(PossibleNames 0\n'
            ')\n'
            '(Verification "N" "N" "N" "N")\n'
            ')'
        )


if __name__ == "__main__":
    unittest.main()
