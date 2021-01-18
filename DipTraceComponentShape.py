#!/usr/bin/python3
#-*- coding: utf-8 -*-


from enum import Enum
from DipTraceUnits import *
from DipTraceEnums import *


class DipTracePoint:

	def __init__(self, x, y):
		self.x = mm2units( x )
		self.y = mm2units( y )

	def move(self, x=0.0, y=0.0):
		self.x += mm2units( x )
		self.y += mm2units( y )
		return self

	def __str__(self):
		return '                (pt {0.x:.5g} {0.y:.5g})\n'.format(self)


class DipTraceComponentShape:

	def __init__(self, shape:DipTraceComponentShapeType=DipTraceComponentShapeType.Null):
		self.shape  = shape
		self.points = []
		self.setLocked()
		self.setEnabled()
		self.setLineWidth()
		self.setText()
		self.setGroup()
		self.setText()
		self.setTextPosition()
		self.setTextAlign()
		self.setFont()
		self.setVector()

	def setLocked(self, state=False):
		self.locked = 'Y' if state else 'N'
		return self

	def setEnabled(self, state=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def setGroup(self, group=-1):
		self.group = group
		return self

	def setLineWidth(self, width=0.25):
		self.line_width = mm2units( width )
		return self

	def addPoint(self, x, y):
		self.points.append(DipTracePoint(x, y))
		return self

	def move(self, x=0.0, y=0.0):
		for point in self.points:
			point.move(x, y)
		return self

	def setText(self, text=''):
		self.text = text
		return self

	def setTextAlign(self, align=DipTraceTextAlign.Center):
		self.text_align = align
		return self

	def setFont(self, font='Tahoma', size=8, spacing=1.2, angle=0.0):
		self.font         = font
		self.font_size    = size
		self.text_spacing = spacing
		self.text_angle   = angle
		return self

	def setVector(self, state=True):
		self.vector = 'Y' if state else 'N'
		return self

	def setTextPosition(self, x=0.0, y=0.0):
		self.text_horiz   = x
		self.text_vert    = y
		return self

	def __str__(self):
		result  = '            (Shape {0}\n'
		result += '              (Enabled "{0.enabled}")\n'.format(self)
		result += '              (Locked "{0.locked}")\n'.format(self)
		result += '              (VectorFont "{0.vector}")\n'.format(self)
		result += '              (FontWidth 0)\n'
		result += '              (FontScale 0)\n'
		result += '              (Orientation 0)\n'
		result += '              (Type {0.shape.value})\n'.format(self)
		result += '              (FontSize {0.font_size})\n'.format(self)
		result += '              (FontColor 0)\n'
		result += '              (FontType 0)\n'
		result += '              (FontName "{0.font}")\n'.format(self)
		result += '              (Name "{0.text}")\n'.format(self)
		result += '              (Width {0.line_width:0.5g})\n'.format(self)
		result += '              (TextAngle {0.text_angle})\n'.format(self)
		result += '              (TextHorz {0.text_horiz})\n'.format(self)
		result += '              (TextVert {0.text_vert})\n'.format(self)
		result += '              (TextAlign {0.text_align.value})\n'.format(self)
		result += '              (LineSpacing {0.text_spacing})\n'.format(self)
		result += '              (Group -1)\n'

		if len(self.points):
			result += '              (Points\n'
			for point in self.points: result += str(point)
			result += '              )\n'

		if len(self.points):
			result += '              (Points_New\n'
			for point in self.points: result += str(point)
			result += '              )\n'

		result += '            )\n'

		return result


if __name__ == "__main__":
	pass