#!/usr/bin/python3
#-*- coding: utf-8 -*-


from enum import Enum
from DipTraceEnums import *
from DipTraceUnits import *

class DipTracePoint:

	def __init__(self, x, y):
		self.x = mm2units( x )
		self.y = mm2units( y )

	def move(self, x=0.0, y=0.0):
		self.x += mm2units( x )
		self.y += mm2units( y )
		return self

	def __str__(self):
		return '              (pt {0.x:.5g} {0.y:.5g})\n'.format(self)


class DipTracePatternShape:

	def __init__(self, shape:DipTracePatternShapeType=DipTracePatternShapeType.Null):
		self.shape  = shape
		self.points = []
		self.setLineWidth()
		self.setLocked()
		self.setLayer()
		self.setText()
		self.setGroup()

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

	def setLayer(self, layer=DipTraceLayer.TopSilk):
		self.layer = layer
		return self

	def addPoint(self, x, y):
		self.points.append(DipTracePoint(x, y))
		return self

	def move(self, x=0.0, y=0.0):
		for point in self.points:
			point.move(x, y)
		return self

	def setText(self, text='', font='Tahoma', vector=True, size=8, align=DipTraceTextAlign.Left, angle=0.0, spacing=1.2, horizontal=0, vertical=0):
		self.text         = text
		self.font         = font
		self.vector       = 'Y' if vector else 'N'
		self.font_size    = size
		self.text_angle   = angle
		self.text_align   = align
		self.text_spacing = spacing
		self.text_horiz   = horizontal
		self.text_vert    = vertical
		return self

	def pattern(self):
		result  = '          (Shape {0.shape.value} "{0.locked}" 0 -0.5 -0.5 0.5 0.5 0 0 "{0.text}" "{0.font}" "{0.vector}" {0.font_size} 0 0 0 {0.line_width} 0)\n'.format(self)

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


	def __str__(self):
		result  = '          (Shape {0.shape.value} "{0.locked}" 0 -0.5 -0.5 0.5 0.5 0 0 "{0.text}" "{0.font}" "{0.vector}" {0.font_size} 0 0 0 {0.line_width} 0)\n'.format(self)
		result += '            (Width -1)\n'
		result += '            (Layer {0.layer.value})\n'.format(self)
		result += '            (TextHorz {0.text_horiz})\n'.format(self)
		result += '            (TextVert {0.text_vert})\n'.format(self)
		result += '            (TextAlign {0.text_align.value})\n'.format(self)
		result += '            (LineSpacing {0.text_spacing})\n'.format(self)
		result += '            (TextAngle {0.text_angle})\n'.format(self)
		result += '            (AllLayers "N")\n'
		result += '            (Group {0.group})\n'.format(self)

		if len(self.points):
			result += '            (Points_New\n'
			for point in self.points: result += str(point)
			result += '            )\n'

		return result


if __name__ == "__main__":
	pass