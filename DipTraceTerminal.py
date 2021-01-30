#!/usr/bin/python3
#-*- coding: utf-8 -*-


import re
from io import TextIOWrapper

from reHelper import reJoin, searchSingleInt, searchSingleFloat, searchDoubleFloat, reInt
from DipTraceUnits import mm2units, units2mm
from DipTraceEnums import DipTraceTerminalShapes
from DipTracePoint import DipTracePoint


class DipTraceTerminal:

	def __init__(self):
		self.points = []
		self.setposition()
		self.setShape()
		self.setAngle()
		self.setSize()
		self.setCorner()
		super().__init__()

	def setposition(self, x:float=0.0, y:float=0.0):
		self.x = mm2units(x)
		self.y = mm2units(y)
		return self

	def move(self, x:float=0.0, y:float=0.0):
		self.x += mm2units( x )
		self.y += mm2units( y )
		return self

	def setSize(self, width:float=0.0, height:float=0.0):
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

	def addPoint(self, x:float=0.0, y:float=0.0):
		self.points.append(DipTracePoint(x, y))
		return self

	def load(self, datafile:TextIOWrapper):
		while line := datafile.readline().strip():

			if line == ')': break

			elif tmp := re.search(reJoin(r'\(ShapePoints', reInt), line):
				while line := datafile.readline():
					if line.strip() == ')':
						break
					if tmp := searchDoubleFloat(r'pt', line):
						x = units2mm(tmp.group(1))
						y = units2mm(tmp.group(2))
						self.addPoint(x, y)

			elif tmp := searchSingleInt(r'Type', line):
				self.shape = DipTraceTerminalShapes(int(tmp.group(1)))

			elif tmp := searchSingleFloat(r'X', line):
				self.x = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'Y', line):
				self.y = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'Angle', line):
				self.angle = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'ShapeWidth', line):
				self.width = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'ShapeHeight', line):
				self.height = float(tmp.group(1))

		return self

	def __str__(self):

		points = '\n'.join([str(point) for point in self.points])

		return ''.join([
			f'(PadTerminal\n'
			f'(Type {self.shape.value})\n',
			f'(X {self.x:.4g})\n',
			f'(Y {self.y:.4g})\n',
			f'(Angle {self.angle:.4g})\n',
			f'(ShapeWidth {self.width:.4g})\n',
			f'(ShapeHeight {self.height:.4g})\n',
			f'(ShapeCorner {self.corner:.4g})\n',
			f'(ShapePoints {len(self.points)}\n{points}\n',
			f')\n',
			f')\n',
		])


if __name__ == "__main__":
	pass