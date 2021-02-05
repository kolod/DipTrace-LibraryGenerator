#!/usr/bin/python3
#-*- coding: utf-8 -*-

from DipTraceUnits import mm2units
from DipTraceEnums import DipTraceComponentShapeType, DipTraceTextAlign
from DipTracePoint import DipTracePoint

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

	def setText(self, text:str=''):
		self.text:str = text
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

		points     = '\n'.join([str(point) for point in self.points])
		points_new = '\n'.join([str(point) for point in self.points])
		text_lines = '\n'.join(f'(pt "{line}")' for line in (self.text if len(self.text) else "\n").splitlines())

		return ''.join([
			f'(Shape {"{0}"}\n',
			f'(Enabled "{self.enabled}")\n',
			f'(Locked "{self.locked}")\n',
			f'(VectorFont "{self.vector}")\n',
			f'(FontWidth 0)\n',
			f'(FontScale 0)\n',
			f'(Orientation 0)\n',
			f'(Type {self.shape.value})\n',
			f'(FontSize {self.font_size})\n',
			f'(FontColor 0)\n',
			f'(FontType 0)\n',
			f'(FontName "{self.font}")\n',
			f'(Name "{self.text}")\n',
			f'(Width {self.line_width:0.6g})\n',
			f'(Points\n{points}\n)\n',
			f'(TextAngle {self.text_angle:0.6g})\n',
			f'(TextHorz {self.text_horiz:0.6g})\n',
			f'(TextVert {self.text_vert:0.6g})\n',
			f'(TextAlign {self.text_align.value})\n',
			f'(LineSpacing {self.text_spacing})\n',
			f'(Group -1)\n',
			f'(TextLines\n{text_lines}\n)\n',
			f'(Points_New\n{points_new}\n)\n',
			f')\n'
		])

if __name__ == "__main__":
	pass