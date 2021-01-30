#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from enum import Enum
from io import TextIOWrapper
from typing import  Literal, AnyStr
from reHelper import *
from DipTraceEnums import *
from DipTraceUnits import *
from DipTracePoint import DipTracePoint

class DipTracePatternShape:

	def __init__(self, match:re.Match[AnyStr]=None):
		self.points = []
		self.points_new = []
		self.setType()
		self.setWidth()
		self.setLineWidth()
		self.setLocked()
		self.setLayer()
		self.setText()
		self.setGroup()
		self.setFont()
		self.setVector()
		self.setFontSize()
		self.setTextAngle()
		self.setTextAlign()
		self.setSpacing()
		self.setTextHorizontal()
		self.setTextVertical()
		self.setTextWidth()
		if match:
			self.shape       = DipTracePatternShapeType(int(match.group(1)))
			self.locked      = match.group(2)
			self.text        = match.group(10)
			self.font        = match.group(11)
			self.vector      = match.group(12)
			self.font_size   = int(match.group(13))
			self.text_width  = float(match.group(14))
			self.line_width  = float(match.group(15))
		super().__init__()

	def setType(self, shape:DipTracePatternShapeType=DipTracePatternShapeType.Null):
		self.shape = type
		return self

	def setLocked(self, state=False):
		self.locked = 'Y' if state else 'N'
		return self

	def setEnabled(self, state=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def setWidth(self, width:float=-1.0):
		self.width = mm2units(width)
		return self

	def setGroup(self, group=-1):
		self.group = group
		return self

	def setLineWidth(self, width=0.25):
		self.line_width = mm2units( width )
		return self

	def setLayer(self, layer=DipTraceLayerType.TopSilk):
		self.layer = layer
		return self

	def addPoint(self, x, y):
		self.points.append(DipTracePoint(x, y))
		return self

	def addPointNew(self, x, y):
		self.points_new.append(DipTracePoint(x, y))
		return self

	def move(self, x=0.0, y=0.0):
		for point in self.points:
			point.move(x, y)
		return self

	def setText(self, text:str=''):
		self.text         = text
		return self

	def setFont(self, font:str='Tahoma'):
		self.font         = font
		return self

	def setVector(self, vector:bool=True):
		self.vector       = 'Y' if vector else 'N'
		return self

	def setFontSize(self, size:int=8):
		self.font_size    = size
		return self

	def setTextAngle(self, align=DipTraceTextAlign.Left):
		self.text_align   = align
		return self

	def setTextAlign(self, angle:float=0.0):
		self.text_angle   = angle
		return self

	def setSpacing(self, spacing:float=1.2):
		self.text_spacing = spacing
		return self

	def setTextHorizontal(self, horizontal:float=0):
		self.text_horiz   = horizontal
		return self

	def setTextVertical(self, vertical=0):
		self.text_vert    = vertical
		return self

	def setTextWidth(self, width:float=1.0):
		self.text_width = width
		return self

	@staticmethod
	def pattern() -> Literal:
		return reJoin(r'Shape', reInt, reBool,
			reFloat, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat,
			reString, reString, reBool, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat)

	def load(self, datafile:TextIOWrapper):
		pos = datafile.tell()

		while line := datafile.readline().strip():

			if   tmp := searchSingleFloat(r'Width', line):
				self.width = float(tmp.group(1))

			elif tmp := searchSingleInt(r'Layer', line):
				self.layer = DipTraceLayerType(int(tmp.group(1)))

			elif tmp := searchSingleFloat(r'TextHorz', line):
				self.text_horiz = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'TextVert', line):
				self.text_vert = float(tmp.group(1))

			elif tmp := searchSingleInt(r'TextAlign', line):
				self.text_align = DipTraceTextAlign(int(tmp.group(1)))

			elif tmp := searchSingleFloat(r'LineSpacing', line):
				self.text_spacing = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'TextAngle', line):
				self.text_angle = float(tmp.group(1))

			elif line == '(Points':
				while line := datafile.readline().strip():
					if line == ')':
						break
					if tmp := searchDoubleFloat(r'pt', line):
						x = units2mm(float(tmp.group(1)))
						y = units2mm(float(tmp.group(2)))
						self.addPoint(x, y)

			elif line == '(Points_New':
				while line := datafile.readline().strip():
					if line == ')':
						break
					if tmp := searchDoubleFloat(r'pt', line):
						x = units2mm(float(tmp.group(1)))
						y = units2mm(float(tmp.group(2)))
						self.addPointNew(x, y)

			elif line.startswith('(Shape ') or line == ')':
				datafile.seek(pos)  # Save position
				break

			pos = datafile.tell()   # Restore last position

		return self


	def __str__(self):

		s = [
			self.points[0].x if len(self.points) >= 1  else 0,
			self.points[0].y if len(self.points) >= 1  else 0,
			self.points[1].x if len(self.points) >= 2  else 0,
			self.points[1].y if len(self.points) >= 2  else 0,
			self.points[2].x if len(self.points) >= 3  else 0,
			self.points[2].y if len(self.points) >= 3  else 0,
		]

		layer = self.layer.value
		if layer > 10: layer = 1

		points     = '(Points\n'     + '\n'.join([str(point) for point in self.points])     + '\n)\n'  if len(self.points)    else ''
		points_new = '(Points_New\n' + '\n'.join([str(point) for point in self.points_new]) + '\n)\n'  if len(self.points_new) else ''
		width      = 0.75 if self.width < 0 else self.width

		return ''.join([
			f'(Shape {self.shape.value} "{self.locked}" {layer} {s[0]:.5g} {s[1]:.5g} {s[2]:.5g} {s[3]:.5g} {s[4]:.5g} {s[5]:.5g} ',
			f'"{self.text}" "{self.font}" "{self.vector}" {self.font_size} {self.text_width:.5g} {self.line_width:.5g} 0 {width} 0)\n',
			f'{points}',
			f'(Width {self.width:.5g})\n',
			f'(Layer {self.layer.value})\n',
			f'(TextHorz {self.text_horiz:.5g})\n',
			f'(TextVert {self.text_vert:.5g})\n',
			f'(TextAlign {self.text_align.value})\n',
			f'(LineSpacing {self.text_spacing})\n',
			f'(TextAngle {self.text_angle:.5g})\n',
			f'{points_new}',
			f'(AllLayers "N")\n',
			f'(Group {self.group})\n'
		])


if __name__ == "__main__":
	pass