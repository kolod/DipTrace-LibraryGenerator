#!/usr/bin/python3
#-*- coding: utf-8 -*-


from enum import Enum
from DipTraceUnits import *
from DipTraceEnums import *
from DipTracePatternShape import *

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




class DipTraceTerminal:

	def __init__(self, x=0.0, y=0.0):
		self.x      = x
		self.y      = y
		self.points = []
		self.setShape()
		self.setAngle()
		self.setSize()
		self.setCorner()

	def move(self, x=0.0, y=0.0):
		self.x += mm2units( x )
		self.y += mm2units( y )
		return self

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
		self.setSize()
		self.setLocked()
		self.setSided()
		self.setStandart()
		self.setPadMask()
		self.setShape()
		self.setHole()

	def setStandart(self, state=False):
		self.standart = 'Y' if state else 'N'
		return self

	def setPosition(self, x=0.0, y=0.0):
		self.x = mm2units( x )
		self.y = mm2units( y )
		return self

	def move(self, x=0.0, y=0.0):
		self.x += mm2units( x )
		self.y += mm2units( y )
		return self

	def setSize(self, width=0.0, height=0.0):
		self.width  = mm2units( width )
		self.height = mm2units( height )
		return self

	def setHole(self, hole_type=DipTraceHoleTypes.Round, width=0.0, height=0.0):
		self.hole_type   = hole_type
		self.hole_width  = mm2units( width )
		self.hole_height = mm2units( height )
		return self

	def setLocked(self, state=False):
		self.locked = 'Y' if state else 'N'
		return self

	def setSided(self, state=False):
		self.sided = 'Y' if state else 'N'
		return self

	def setShape(self, shape=DipTracePadShapes.Ellipse):
		self.shape = shape
		return self

	def setPadMask(self, percent=0, edge_gap=0, segment_gap=0, segment_side=0):
		self.mask_percent         = percent
		self.mask_edge_gap        = edge_gap
		self.mask_segment_gap     = segment_gap
		self.mask_segment_side    = segment_side
		self.mask_top_segments    = []
		self.mask_bottom_segments = []
		return self

	def setPadMaskTopSegments(self, segments=[]):
		self.mask_top_segments = segments
		return self

	def setPadMaskBottomSegments(self, segments=[]):
		self.mask_bottom_segments = segments
		return self

	def addTerminal(self, terminal:DipTraceTerminal):
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
		result += '            (PadMask_Percent {0.mask_percent})\n'.format(self)
		result += '            (PadMask_EdgeGap {0.mask_edge_gap})\n'.format(self)
		result += '            (PadMask_SegmentGap {0.mask_segment_gap})\n'.format(self)
		result += '            (PadMask_SegmentSide {0.mask_segment_side})\n'.format(self)
		result += '            (PadMask_TopSegments {0}\n'.format(len(self.mask_top_segments))
		# TODO: add top segments
		result += '            )\n'
		result += '            (PadMask_BotSegments {0}\n'.format(len(self.mask_bottom_segments))
		# TODO: add bottom segments
		result += '            )\n'
		result += '            (PadTerminalCount {0}\n'.format(len(self.terminals))
		for terminal in self.terminals: result += str(terminal)
		result += '            )\n'
		result += '          )\n'

		return result


class DipTracePattern:

	isComponent = False

	def __init__(self, name, ref:str=None, value:str=None):
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
		if type(pad) is list:
			self.pads.extend(pad)
		else:
			self.pads.append(pad)
		return self

	def addShape(self, shape):
		if type(shape) is list:
			self.shapes.extend(shape)
		else:
			self.shapes.append(shape)
		return self

	def move(self, x=0.0, y=0.0):
		for pad in self.pads: pad.move(x, y)
		for shape in self.shapes: shape.move(x, y)
		return self

	def add3dModel(self, model:DipTrace3dModel):
		self.model = model
		return self

	def setVariableParameter(self, vars=None):
		self.variableParameter = vars or ['N', 'N', 'N', 'N', 'N']
		return self

	def __str__(self) -> str:
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
			if DipTracePattern.isComponent: result += str(DipTracePad(0))
			for pad in self.pads: result += str(pad)
			if DipTracePattern.isComponent: result += str(DipTracePad(len(self.pads) + 1))
			result += '        )\n'

		if len(self.shapes):
			result += '        (Shapes\n'
			result += str(DipTracePatternShape(DipTracePatternShapeType.Null).setGroup(0))
			for shape in self.shapes: result += str(shape)
			result += str(DipTracePatternShape(DipTracePatternShapeType.Null).setGroup(0))
			result += '        )\n'

		if self.model:
			result += str(self.model)

		result +='      )\n'

		return result


class DipTracePatternLibrary:

	def __init__(self, name:str, hint=None):

		self.name = name
		self.hint = hint or name
		self.patterns = []

	def addPattern(self, pattern:DipTracePattern):
		self.patterns.append(pattern)
		return self

	def __str__(self) -> str:
		DipTracePattern.isComponent = False # Fix for DipTracePattern

		result  = '(Source "DipTrace-ComLibrary" 21)\n'
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


	def save(self, filename:str) -> None:
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(str(self))


if __name__ == "__main__":
	pass