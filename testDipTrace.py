#!/usr/bin/python3
#-*- coding: utf-8 -*-

import unittest
from DipTraceEnums import DipTrace3dModelType, DipTracePatternShapeType, DipTraceTerminalShapes, DipTraceTextRotation
from DipTraceHole import DipTraceHole
from DipTraceBool import DipTraceBool
from DipTracePoint import DipTracePoint
from DipTrace3dModel import DipTrace3dModel
from DipTraceTerminal import DipTraceTerminal
from DipTracePatternShape import DipTracePatternShape
from DipTracePatternLayer import DipTracePatternLayer

class TestDipTraceHole(unittest.TestCase):

	def test_hole(self):
		hole = DipTraceHole()
		self.assertEqual(str(hole), '(Hole "Y" "N" 0 0 0 0 0)')
		hole.locked = True
		hole.x = 2.0
		hole.y = -1.0
		hole.keepout = 4.0
		hole.hole = 3.0
		hole.group = -1
		hole.recalculate(-1.0, -1.5)
		self.assertEqual(str(hole), '(Hole "Y" "Y" 3 -1.5 12 9 -1)')


class TestDipTracePoint(unittest.TestCase):

	def test_point(self):
		point = DipTracePoint(1.0, 2.0)
		self.assertEqual(str(point), '(pt 3 -6)')
		point.x = 2.3
		point.y = 3.8
		self.assertEqual(str(point), '(pt 6.9 -11.4)')
		point.convert = False
		self.assertEqual(str(point), '(pt 2.3 -3.8)')

class TestDipTraceBool(unittest.TestCase):

	def test_bool(self):
		flag = DipTraceBool(True)
		self.assertEqual(str(flag), 'Y')
		flag.state = False
		self.assertEqual(str(flag), 'N')

class TestDipTrace3dModel(unittest.TestCase):

	def test_model(self):

		model = DipTrace3dModel()
		self.assertEqual(str(model),
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

		self.assertEqual(str(model),
			'(Model3D\n'
			'(Model3DFile "")\n'
			'(pt 45 30 -60 3 -6 -9 1 1 1 "N" "N" -1 0 0 0 4934475 1 "Y")\n'
			')\n'
		)

class TesDipTraceTerminal(unittest.TestCase):

	def test_terminal(self):

		terminal = DipTraceTerminal()

		self.assertEqual(str(terminal),
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

		self.assertEqual(str(terminal),
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
		shape.font_size = 10
		shape.line_width = 0.2
		shape.text_width = 1.0
		shape.text_rotation = DipTraceTextRotation.Rotate_90
		shape.font_line_width = -2
		shape.vector = False
		shape.text_horiz = -1
		shape.text_vert = -1
		shape.group = -1
		shape.points_new.append(DipTracePoint(-0.5, 2))
		shape.points_new.append(DipTracePoint(-2.5, 0))
		shape.points_new.append(DipTracePoint(-0.5,-2))
		shape.points_new.append(DipTracePoint( 2.5, 0))
		shape.points_new.append(DipTracePoint(   0, 2))
		shape.recalculate(0.0, 0.0, 5.0, 4.0)

		self.assertEqual(str(shape),
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
		self.assertEqual(str(shape),
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

		self.assertEqual(str(layer),
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
		layer.pads.extend([1,2,4,5,6,10])
		layer.shapes.append(2)
		layer.shapes.append(3)

		self.assertEqual(str(layer),
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

if __name__ == "__main__":
	unittest.main()