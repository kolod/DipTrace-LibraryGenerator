#!/usr/bin/python3
#-*- coding: utf-8 -*-


from enum import Enum


def mm2units(value):
	return value*3

def units2mm(value):
	return value/3

class DipTraceHoleTypes(Enum):
	Round     = 0
	Obround   = 1

class DipTracePadTypes(Enum):
	ThroughHole = 0
	Surface     = 1

class DipTracePadShapes(Enum):
	Ellipse   = 0
	Obround   = 1
	Rectangle = 2
	Polygon   = 3
	DShape    = 4

class DipTraceTerminalShapes(Enum):
	Null      = 0
	Obround   = 1
	Rectangle = 2
	Polygon   = 3
	DShape    = 4

class DipTraceShapeType(Enum):
	Null             = 0   # TODO:
	Line             = 1
	Rectangle        = 2
	Obround          = 3
	FilledRectangle  = 2
	FilledObround    = 5
	Arc              = 6
	Text             = 7
	Poliline         = 8
	Poligon          = 9

class DipTraceLayer(Enum):
	TopSilk          = 0
	TopAssembly      = 1
	TopMask          = 2
	TopPaste         = 3
	BottomPaste      = 4
	BottomMask       = 5
	BottomAssembly   = 6
	BottomSilk       = 7
	Top              = 8
	TopKeepout       = 9
	BottomKeepout    = 10
	Bottom           = 11
	BoardCutout      = 12
	TopCourtyard     = 16
	BottomCourtyard  = 17
	TopOutline       = 18
	BottomOutline    = 19

class DipTraceTextAlign(Enum):
	Left             = -1
	Center           = 0
	Right            = 1

class DipTracePoint:

	def __init__(self, x, y):
		self.x = mm2units( x )
		self.y = mm2units( y )

	def __str__(self):
		return '              (pt {0.x:.5g} {0.y:.5g})\n'.format(self)

class DipTrace3dModel:

	def __init__(self, filename=''):
		self.filename = filename
		self.setTranslation()
		self.setRotation()
		self.setScale()
		self.setAutomaticSearch()
		self.setFlipByZ()

	def setTranslation(self, x=0.0, y=0.0, z=0.0):
		self.x = x
		self.y = y
		self.z = z
		return self

	def setRotation(self, x=0.0, y=0.0, z=0.0):
		self.rotation_x = x
		self.rotation_y = y
		self.rotation_z = z
		return self

	def setScale(self, x=1.0, y=1.0, z=1.0):
		self.scale_x = x
		self.scale_y = y
		self.scale_z = z
		return self

	def setAutomaticSearch(self, state=False):
		self.search = 'Y' if state else 'N'
		return self

	def setFlipByZ(self, state=False):
		self.flip = 'Y' if state else 'N'
		return self

	def __str__(self):
		result = ''
		result += '        (Model3D\n'
		result += '          (Model3DFile "{0.filename}")\n'.format(self)
		result += '          (pt {0.rotation_x:.4g} {0.rotation_y:.4g} {0.rotation_z:.4g} {0.x:.4g} {0.y:.4g} {0.z:.4g} {0.scale_x:.4g} {0.scale_y:.4g} {0.scale_z:.4g} "{0.flip}" "{0.search}" 0)\n'.format(self)
		result += '        )\n'
		return result


class DipTraceShape:

	def __init__(self, shape):
		self.shape  = shape
		self.points = []
		self.setLineWidth()
		self.setLocked()
		self.setLayer()
		self.setText()
		self.setGroup()

	def setLocked(self, state=True):
		self.locked = 'Y' if state else 'N'
		return self

	def setGroup(self, group=-1):
		self.group = group
		return self

	def setLineWidth(self, width=0.25):
		self.line_width = mm2units( width )
		return self

	def setLayer(self, layer=DipTraceLayer.TopSilk):
		self.layer = layer
		return self

	def addPoint(self, x, y):
		self.points.append(DipTracePoint(x, y))
		return self

	def setText(self, text='', font='Tahoma', vector=True, size=8, align=DipTraceTextAlign.Left, angle=0.0, spacing=1.2, horizontal=0, vertical=0):
		self.text         = text
		self.font         = font
		self.vector       = 'Y' if vector else 'N'
		self.font_size    = size
		self.text_angle   = angle
		self.text_align   = align
		self.tine_spacing = spacing
		self.text_horiz   = horizontal
		self.text_vert    = vertical
		return self

	def __str__(self):
		result = ''

		result += '          (Shape {0.shape.value} "{0.locked}" 0 -0.5 -0.5 0.5 0.5 0 0 "{0.text}" "{0.font}" "{0.vector}" {0.font_size} 0 0 0 {0.line_width} 0)\n'.format(self)

		result += '            (Width -1)\n'
		result += '            (Layer {0.layer.value})\n'.format(self)
		result += '            (TextHorz {0.text_horiz})\n'.format(self)
		result += '            (TextVert {0.text_vert})\n'.format(self)
		result += '            (TextAlign {0.text_align.value})\n'.format(self)
		result += '            (LineSpacing {0.tine_spacing})\n'.format(self)
		result += '            (TextAngle {0.text_angle})\n'.format(self)
		result += '            (AllLayers "N")\n'
		result += '            (Group {0.group})\n'.format(self)

		if len(self.points):
			result += '            (Points_New\n'
			for point in self.points: result += str(point)
			result += '            )\n'

		return result

class DipTraceTerminal:

	def __init__(self, x=0.0, y=0.0):
		self.x      = x
		self.y      = y
		self.points = []
		self.setShape()
		self.setAngle()
		self.setSize()
		self.setCorner()

	def setSize(self, width=0.0, height=0.0):
		self.width  = mm2units( width )
		self.height = mm2units( height )
		return self

	def setShape(self, shape=DipTraceTerminalShapes.Null):
		self.shape = shape
		return self

	def setAngle(self, angle=0.0):
		self.angle = angle
		return self

	def setCorner(self, corner=0.0):
		self.corner = corner
		return self

	def __str__(self):
		result = ''

		result += '              (PadTerminal\n'

		result += '                (Type {0.shape.value})\n'.format(self)
		result += '                (X {0.x:.4g})\n'.format(self)
		result += '                (Y {0.y:.4g})\n'.format(self)
		result += '                (Angle {0.angle:.4g})\n'.format(self)
		result += '                (ShapeWidth {0.width:.4g})\n'.format(self)
		result += '                (ShapeHeight {0.height:.4g})\n'.format(self)
		result += '                (ShapeCorner {0.corner:.4g})\n'.format(self)

		result += '                (ShapePoints {0}\n'.format(len(self.points))
		result += '                )\n'

		result += '              )\n'

		return result


class DipTracePad:

	def __init__(self, number, x=0.0, y=0.0, name=None, note=''):
		self.number    = number
		self.name      = name or str(number)
		self.note      = note
		self.terminals = []
		self.setPosition(x, y)
		self.setLocked()
		self.setSided()
		self.setStandart()
		self.setPadMask()

	def setStandart(self, state=True):
		self.standart = 'Y' if state else 'N'
		return self

	def setPosition(self, x=0.0, y=0.0):
		self.x = mm2units( x )
		self.y = mm2units( y )
		return self

	def setSize(self, width, height=None):
		self.width  = mm2units( width )
		self.height = mm2units( height or width )
		return self

	def setHole(self, hole_type, width, height=None):
		self.hole_type   = hole_type
		self.hole_width  = mm2units( width )
		self.hole_height = mm2units( height or 0)
		return self

	def setLocked(self, state=True):
		self.locked = 'Y' if state else 'N'
		return self

	def setSided(self, state=False):
		self.sided = 'Y' if state else 'N'
		return self

	def setShape(self, shape):
		self.shape = shape
		return self

	def setPadMask(self, percent=50.0, edge_gap=0.9, segment_gap=0.6, segment_side=3, top_segments=[], bottom_segments=[]):
		self.mask_percent         = percent
		self.mask_edge_gap        = edge_gap
		self.mask_segment_gap     = segment_gap
		self.mask_segment_side    = segment_side
		self.mask_top_segments    = top_segments
		self.mask_bottom_segments = bottom_segments
		return self

	def addTerminal(self, terminal):
		self.terminals.append(terminal)
		return self

	def __str__(self):
		result = ''
		result += '          (Pad {0.number} "{0.name}" "{0.note}" {0.x:.4g} {0.y:.4g}\n'.format(self)
		result += '            (Number {0.number})\n'.format(self)
		result += '            (Number_New {0.number})\n'.format(self)
		result += '            (Locked "{0.locked}")\n'.format(self)
		result += '            (Sided "{0.sided}")\n'.format(self)
		result += '            (Standard "{0.standart}")\n'.format(self)
		result += '            (PadShape {0.shape.value})\n'.format(self)
		result += '            (PadShape_New {0.shape.value})\n'.format(self)
		result += '            (PadWidth {0.width:.5g})\n'.format(self)
		result += '            (PadHeight {0.height:.5g})\n'.format(self)
		result += '            (PadWidth_New {0.width:.5g})\n'.format(self)
		result += '            (PadHeight_New {0.height:.5g})\n'.format(self)
		result += '            (PadHole {0.hole_width:.5g})\n'.format(self)
		result += '            (PadHoleH {0.hole_height:.5g})\n'.format(self)
		result += '            (PadHoleType {0.hole_type.value})\n'.format(self)

		if len(self.terminals) > 0:
			result += '            (PadTerminalCount {0}\n'.format(len(self.terminals))
			for terminal in self.terminals: result += str(terminal)
			result += '            )\n'

		result += '            (PadMask_Percent {0.mask_percent})\n'.format(self)
		result += '            (PadMask_EdgeGap {0.mask_edge_gap})\n'.format(self)
		result += '            (PadMask_SegmentGap {0.mask_segment_gap})\n'.format(self)
		result += '            (PadMask_SegmentSide {0.mask_segment_side})\n'.format(self)
		result += '            (PadMask_TopSegments {0}\n'.format(len(self.mask_top_segments))
		result += '            )\n'
		result += '            (PadMask_BotSegments {0}\n'.format(len(self.mask_bottom_segments))
		result += '            )\n'


		result += '          )\n'

		return result


class DipTracePattern:

	def __init__(self, name, ref=None, value=None):
		self.name   = name
		self.ref    = ref
		self.value  = value or name
		self.pads   = []
		self.shapes = []
		self.setSize()
		self.setVariableParameter()

	def setSize(self, width=0.0, height=0.0):
		self.width  = mm2units(width)
		self.height = mm2units(height)
		return self

	def addPad(self, pad):
		self.pads.append(pad)
		return self

	def addShape(self, shape):
		if type(shape) is list:
			self.shapes.extend(shape)
		else:
			self.shapes.append(shape)
		return self

	def add3dModel(self, model):
		self.model = model
		return self

	def setVariableParameter(self, vars=None):
		self.variableParameter = vars or ['N', 'N', 'N', 'N', 'N']
		return self

	def __str__(self):
		result = ''
		result +='      (Pattern "{0.name}" "{0.ref}"\n'.format(self)
		result +='        (Value "{0.value}")\n'.format(self)
		result +='        (Width {0.width:.5g})\n'.format(self)
		result +='        (Height {0.height:.5g})\n'.format(self)

		if type(self.variableParameter) is list:
			i = 1
			for variable in self.variableParameter:
				result += '        (VariableParameter{0} "{1}")\n'.format(i, variable)
				i += 1

		if len(self.pads):
			result += '        (Pads\n'
			for pad in self.pads: result += str(pad)
			result += '        )\n'

		if len(self.shapes):
			result += '        (Shapes\n'
			result += str(DipTraceShape(DipTraceShapeType.Null).setGroup(0))
			for shape in self.shapes: result += str(shape)
			result += str(DipTraceShape(DipTraceShapeType.Null).setGroup(0))
			result += '        )\n'

		if self.model:
			result += str(self.model)

		result +='      )\n'

		return result


class DipTracePatternLibrary:

	def __init__(self, name, hint=None):

		self.name = name
		self.hint = hint or name
		self.patterns = []

	def addPattern(self, pattern):
		self.patterns.append(pattern)
		return self

	def __str__(self):
		result = ''

		result += '(Source "DipTrace-ComLibrary" 21)\n'
		result += '  (Library\n'
		result += '    (Size {})\n'.format(len(self.patterns))
		result += '    (Name "{}")\n'.format(self.name)
		result += '    (Hint "{}")\n'.format(self.hint)
		result += '    (Categories 0\n'
		result += '    )\n'

		if len(self.patterns):
			result += '    (Patterns\n'
			for pattern in self.patterns: result += str(pattern)
			result += '    )\n'

		result += '  )\n'
		result += '()\n'

		return result


	def save(self, filename):
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(str(self))


if __name__ == "__main__":
	pass