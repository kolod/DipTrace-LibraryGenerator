#!/usr/bin/python3
#-*- coding: utf-8 -*-


import re
from io import TextIOWrapper
from typing import  Literal, AnyStr

from DipTraceUnits import mm2units, units2mm
from DipTracePoint import DipTracePoint
from DipTraceTerminal import DipTraceTerminal
from DipTraceEnums import DipTraceHoleTypes, DipTracePadShapes

from reHelper import reJoin, reInt, reString, reFloat, searchDoubleFloat, searchSingleBool, searchSingleFloat, searchSingleInt

class DipTracePad:

	def __init__(self, match:re.Match[AnyStr]):
		self.terminals            = []
		self.points               = []
		self.points_new           = []
		self.mask_top_segments    = []
		self.mask_bottom_segments = []
		self.setName()
		self.setNote()
		self.setNumber()
		self.setposition()
		self.setGroup()
		self.setSurface()
		self.setSize()
		self.setLocked()
		self.setInverted()
		self.setSided()
		self.setStandart()
		self.setPadMask()
		self.setShape()
		self.setHole()
		if match:
			self.number = int(match.group(1))
			self.name   = match.group(2)
			self.note   = match.group(3)
			self.x      = float(match.group(4))
			self.y      = float(match.group(5))
		super().__init__()

	def setName(self, name:str=''):
		self.name = name
		return self

	def setNote(self, note:str=''):
		self.note = note
		return self

	def setNumber(self, number:int=0):
		self.number = number
		return self

	def setposition(self, x:float=0.0, y:float=0.0):
		self.x = mm2units(x)
		self.y = mm2units(y)
		return self

	def setStandart(self, state=False):
		self.standart = 'Y' if state else 'N'
		return self

	def setSurface(self, state=False):
		self.surface = 'Y' if state else 'N'
		return self

	def setGroup(self, group:int=-1):
		self.group = group
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

	def setInverted(self, state=False):
		self.inverted = 'Y' if state else 'N'
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

	@staticmethod
	def pattern():
		return reJoin(r'\(Pad', reInt, reString, reString, reFloat, reFloat)

	def load(self, datafile:TextIOWrapper):

		while line := datafile.readline().strip():

			if line == ')':
				break

			elif line == '(Points':
				while line := datafile.readline().strip():
					if line == ')':
						break
					if tmp := searchDoubleFloat(r'pt', line):
						x = units2mm(float(tmp.group(1)))
						y = units2mm(float(tmp.group(2)))
						self.points.append(DipTracePoint(x, y))

			elif line == '(PadPoints_New':
				while line := datafile.readline().strip():
					if line == ')':
						break
					if tmp := searchDoubleFloat(r'pt', line):
						x = units2mm(float(tmp.group(1)))
						y = units2mm(float(tmp.group(2)))
						self.points_new.append(DipTracePoint(x, y))

			elif line.startswith('(PadTerminalCount '):
				while line := datafile.readline().strip():
					if line == ')':
						break
					if line == '(PadTerminal':
						terminal = DipTraceTerminal()
						terminal.load(datafile)
						self.addTerminal(terminal)

			elif line.startswith('(PadMask_TopSegments '):
				while line := datafile.readline().strip():
					if line == ')':
						break
				# TODO: implement PadMask_TopSegments

			elif line.startswith('(PadMask_BotSegments '):
				while line := datafile.readline().strip():
					if line == ')':
						break
				# TODO: implement PadMask_BotSegments

			elif tmp := searchSingleBool(r'Locked', line):
				self.locked = tmp.group(1)

			elif tmp := searchSingleBool(r'Inverted', line):
				self.inverted = tmp.group(1)

			elif tmp := searchSingleBool(r'Sided', line):
				self.sided = tmp.group(1)

			elif tmp := searchSingleBool(r'SurfacePad', line):
				self.surface = tmp.group(1)

			elif tmp :=searchSingleBool(r'Standard', line):
				self.standart = tmp.group(1)

			elif tmp := searchSingleInt(r'Group', line):
				self.group = int(tmp.group(1))

			elif tmp := searchSingleInt(r'PadShape', line):
				self.shape = DipTracePadShapes(int(tmp.group(1)))

			elif tmp := searchSingleFloat(r'PadWidth', line):
				self.width = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadHeight', line):
				self.height = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadWidth_New', line):
				self.width = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadHeight_New', line):
				self.height = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadMask_Percent', line):
				self.mask_percent = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadMask_EdgeGap', line):
				self.mask_edge_gap = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadMask_SegmentGap', line):
				self.mask_segment_gap = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadMask_SegmentSide', line):
				self.mask_segment_side = float(tmp.group(1))

		return self


	def __str__(self):
		points         = '\n'.join([str(point) for point in self.points])
		points_new     = '\n'.join([str(point) for point in self.points_new])
		terminals      = '\n'.join([str(point) for point in self.terminals])
		top_segmens    = '\n'
		bottom_segmens = '\n'

		return \
			f'(Pad {self.number} "{self.name}" "{self.note}" {self.x:.5g} {self.y:.5g}\n'\
			f'(Number {self.number})\n'\
			f'(Number_New {self.number})\n'\
			f'(Inverted "{self.inverted}")\n'\
			f'(Locked "{self.locked}")\n'\
			f'(Sided "{self.sided}")\n'\
			f'(PadWidth {self.width:.5g})\n'\
			f'(PadHeight {self.height:.5g})\n'\
			f'(PadHole {self.hole_width:.5g})\n'\
			f'(PadHoleH {self.hole_height:.5g})\n'\
			f'(PadHoleType {self.hole_type.value})\n'\
			f'(SurfacePad "{self.surface}")\n'\
			f'(PadShape {self.shape.value})\n'\
			f'(PadShape_New {self.shape.value})\n'\
			f'(PadWidth_New {self.width:.5g})\n'\
			f'(PadHeight_New {self.height:.5g})\n'\
			f'(Group {self.group})\n'\
			f'(Standard "{self.standart}")\n'\
			f'(Points\n{points}\n)\n'\
			f'(PadPoints_New\n{points_new}\n)\n'\
			f'(PadTerminalCount {len(self.terminals)}\n{terminals}\n)\n'\
			f'(PadMask_Percent {self.mask_percent:0.2g})\n'\
			f'(PadMask_EdgeGap {self.mask_edge_gap:0.1g})\n'\
			f'(PadMask_SegmentGap {self.mask_segment_gap:0.1g})\n'\
			f'(PadMask_SegmentSide {self.mask_segment_side:0.1g})\n'\
			f'(PadMask_TopSegments {len(self.mask_top_segments)}{top_segmens}\n)\n'\
			f'(PadMask_BotSegments {len(self.mask_bottom_segments)}{bottom_segmens}\n)\n'\
			f')\n'


if __name__ == "__main__":
	pass