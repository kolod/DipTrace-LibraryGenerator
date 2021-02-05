#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from io import TextIOWrapper
from typing import  Literal, AnyStr
from DipTraceUnits import mm2units, units2mm
from DipTracePoint import DipTracePoint
from DipTraceTerminal import DipTraceTerminal
from DipTraceEnums import DipTraceHoleTypes, DipTracePadShapes, DipTracePadShapesNew
from reHelper import reBracketed, reJoin, reInt, reString, reFloat, searchDoubleFloat, searchSingleBool, searchSingleFloat, searchSingleInt

# DisableTopMask     |  DisableTopPaste     |
# DisableBottomMask  |  DisableBottomPaste  |
#--------------------+----------------------+----------------
#	Common           |    Common            |   "N", 0, 0
#	Open             |    Solder            |   "N", 1, 1
#	Tented           |    NoSolder          |   "Y", 2
#	ByPasteMask      |    Segments          |   "N", 0, 3


class DipTracePad:

	isComponent:bool = False

	def __init__(self, match:re.Match[AnyStr]=None):
		self.terminals            = []
		self.points               = []
		self.points_new           = []
		self.mask_top_segments    = []
		self.mask_bottom_segments = []
		self.setName()
		self.setNote()
		self.setNumber()
		self.setPosition()
		self.setGroup()
		self.setSurface()
		self.setSize()
		self.setLocked()
		self.setInverted()
		self.setSided()
		self.setStandart()
		self.setPadMask()
		self.setShape()
		self.setShapeNew()
		self.setHole()
		self.setCustomShrink()
		self.setCustomShrinkNew()
		self.setCustomSwell()
		self.setCustomSwellNew()
		self.setPadAngle()
		self.setPadShapePosition()
		self.setPadCorner()
		self.setTopMask()
		self.setBottomMask()
		self.setTopPaste()
		self.setBottomPaste()

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

	def setPosition(self, x:float=0.0, y:float=0.0):
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

	def setShape(self, shape=DipTracePadShapes.Oval):
		self.shape = shape
		return self

	def setShapeNew(self, shape=DipTracePadShapesNew.Ellipse):
		self.shape_new = shape
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

	def setCustomSwell(self, swell:float=0.0):
		self.custom_swell = swell
		return self

	def setCustomSwellNew(self, swell:float=0.0):
		self.custom_swell_new = swell
		return self

	def setCustomShrink(self, shrink:float=0.0):
		self.custom_shrink = shrink
		return self

	def setCustomShrinkNew(self, shrink:float=0.0):
		self.custom_shrink_new = shrink
		return self

	def setPadAngle(self, angle:float=0.0):
		self.pad_angle = angle
		return self

	def setPadShapePosition(self, x:float=0.0, y:float=0.0):
		self.pad_shape_x = mm2units(x) #TODO: Check units
		self.pad_shape_y = mm2units(y) #TODO: Check units
		return self

	def setPadCorner(self, corner:float=0.0):
		self.pad_corner = corner
		return self

	@staticmethod
	def _mask(param1:bool=False, param2:int=0, param3:int=0, match:re.Match=None):
		result= []
		if match == None:
			result.append('Y' if param1 else 'N')
			result.append(param2)
			if param3 != None:
				result.append(param3)
		else:
			if match.lastindex >= 1: result.append(match.group(1))
			if match.lastindex >= 2: result.append(int(match.group(2)))
			if match.lastindex >= 3: result.append(int(match.group(3)))
		return result

	def setTopMask(self, param1:bool=False, param2:int=0, param3:int=0):
		self.top_mask = self._mask(param1, param2, param3)
		return self

	def setBottomMask(self, param1:bool=False, param2:int=0, param3:int=0):
		self.bottom_mask = self._mask(param1, param2, param3)
		return self

	def setTopPaste(self, param1:bool=False, param2:int=0, param3:int=0):
		self.top_paste = self._mask(param1, param2, param3)
		return self

	def setBottomPaste(self, param1:bool=False, param2:int=0, param3:int=0):
		self.bottom_paste = self._mask(param1, param2, param3)
		return self

	def addTerminal(self, terminal:DipTraceTerminal):
		self.terminals.append(terminal)
		return self

	def move(self, x:float=0.0, y:float=0.0):
		self.x += mm2units( x )
		self.y += mm2units( y )
		return self

	@staticmethod
	def pattern() -> Literal:
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

			elif tmp := searchSingleInt(r'PadShape_New', line):
				self.shape_new = DipTracePadShapesNew(int(tmp.group(1)))

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

			elif tmp := searchSingleFloat(r'CustomSwell', line):
				self.custom_swell = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'CustomSwell_New', line):
				self.custom_swell_new = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'CustomShrink', line):
				self.custom_shrink = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'CustomShrink_New', line):
				self.custom_shrink_new = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadHole', line):
				self.hole_width = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadHoleH', line):
				self.hole_height = float(tmp.group(1))

			elif tmp := searchSingleInt(r'PadHoleType', line):
				self.hole_type = DipTraceHoleTypes(int(tmp.group(1)))

			elif tmp := searchSingleFloat(r'PadAngle', line):
				self.pad_angle = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadShape_X', line):
				self.pad_shape_x = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadShape_Y', line):
				self.pad_shape_y = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadCorner', line):
				self.pad_corner = float(tmp.group(1))

			elif tmp := re.search(reBracketed(reJoin(r'DisableTopMask', r'"([YN]?)" ([-]?\d*)\s*([-]?\d*)')), line):
				self.top_mask = self._mask(match=tmp)

			elif tmp := re.search(reBracketed(reJoin(r'DisableBottomMask', r'"([YN]?)" ([-]?\d*)\s*([-]?\d*)')), line):
				self.bottom_mask = self._mask(match=tmp)

			elif tmp := re.search(reBracketed(reJoin(r'DisableTopPaste', r'"([YN]?)" ([-]?\d*)\s*([-]?\d*)')), line):
				self.top_paste = self._mask(match=tmp)

			elif tmp := re.search(reBracketed(reJoin(r'DisableBottomPaste', r'"([YN]?)" ([-]?\d*)\s*([-]?\d*)')), line):
				self.bottom_paste = self._mask(match=tmp)

		return self


	def __str__(self):
		points         = '\n'.join([str(point) for point in self.points     ])
		points_new     = '\n'.join([str(point) for point in self.points_new ])
		terminals      = '\n'.join([str(point) for point in self.terminals  ])
		top_segmens    = '\n'
		bottom_segmens = '\n'

		def ff(value) -> str:
			if type(value) == str: return f'"{value}"'
			if type(value) == int: return str(value)
			return ''

		top_mask      = ' '.join([ff(v) for v in self.top_mask    ])
		bottom_mask   = ' '.join([ff(v) for v in self.bottom_mask ])
		top_paste     = ' '.join([ff(v) for v in self.top_paste   ])
		bottom_paste  = ' '.join([ff(v) for v in self.bottom_paste])

		if self.isComponent:
 			return ''.join([
				f'(Pad {"{0}"} "{self.name}" "{self.note}" {self.x:.5g} {self.y:.5g}\n',
				f'(Number {self.number})\n',
				f'(Number_New {self.number})\n',
				f'(Inverted "{self.inverted}")\n',
				f'(Locked "{self.locked}")\n',
				f'(Sided "{self.sided}")\n',
				f'(DisableTopMask {top_mask})\n',
				f'(DisableBottomMask {bottom_mask})\n',
				f'(DisableTopPaste {top_paste})\n',
				f'(DisableBottomPaste {bottom_paste})\n',
				f'(CustomSwell {self.custom_swell:.5g})\n',
				f'(CustomShrink {self.custom_swell_new:.5g})\n',
				f'(CustomSwell_New {self.custom_shrink:.5g})\n',
				f'(CustomShrink_New {self.custom_shrink_new:.5g})\n',
				f'(PadWidth {self.width:.5g})\n',
				f'(PadHeight {self.height:.5g})\n',
				f'(PadHole {self.hole_width:.5g})\n',
				f'(PadHoleH {self.hole_height:.5g})\n',
				f'(PadHoleType {self.hole_type.value})\n',
				f'(SurfacePad "{self.surface}")\n',
				f'(PadShape {self.shape.value})\n',
				f'(PadShape_New {self.shape_new.value})\n',
				f'(PadAngle {self.pad_angle:0.5g})\n',
				f'(PadShape_X {self.pad_shape_x:0.5g})\n',
				f'(PadShape_Y {self.pad_shape_y:0.5g})\n',
				f'(PadCorner {self.pad_corner:.6g})\n',
				f'(PadWidth_New {self.width:.5g})\n',
				f'(PadHeight_New {self.height:.5g})\n',
				f'(Group {self.group})\n',
				f'(Standard "{self.standart}")\n',
				f'(Point\n{points}\n)\n',
				f'(PadPoints_New\n{points_new}\n)\n' if len(self.points) else '',
				f'(PadTerminalCount {len(self.terminals)}\n{terminals}\n)\n',
				f'(PadMask_Percent {self.mask_percent:0.2g})\n',
				f'(PadMask_EdgeGap {self.mask_edge_gap:0.1g})\n',
				f'(PadMask_SegmentGap {self.mask_segment_gap:0.1g})\n',
				f'(PadMask_SegmentSide {self.mask_segment_side:0.1g})\n',
				f'(PadMask_TopSegments {len(self.mask_top_segments)}{top_segmens}\n)\n',
				f'(PadMask_BotSegments {len(self.mask_bottom_segments)}{bottom_segmens}\n)\n',
				f')\n',
			])
		else:
			return ''.join([
				f'(Pad {"{0}"} "{self.name}" "{self.note}" {self.x:.5g} {self.y:.5g}\n',
				f'(Number {self.number})\n',
				f'(Number_New {self.number})\n',
				f'(Inverted "{self.inverted}")\n',
				f'(Locked "{self.locked}")\n',
				f'(Sided "{self.sided}")\n',
				f'(DisableTopMask {top_mask})\n',
				f'(DisableBottomMask {bottom_mask})\n',
				f'(DisableTopPaste {top_paste})\n',
				f'(DisableBottomPaste {bottom_paste})\n',
				f'(CustomSwell {self.custom_swell:.5g})\n',
				f'(CustomShrink {self.custom_swell_new:.5g})\n',
				f'(CustomSwell_New {self.custom_shrink:.5g})\n',
				f'(CustomShrink_New {self.custom_shrink_new:.5g})\n',
				f'(PadWidth {self.width:.5g})\n',
				f'(PadHeight {self.height:.5g})\n',
				f'(PadHole {self.hole_width:.5g})\n',
				f'(PadHoleH {self.hole_height:.5g})\n',
				f'(PadHoleType {self.hole_type.value})\n',
				f'(SurfacePad "{self.surface}")\n',
				f'(PadShape {self.shape.value})\n',
				f'(PadShape_New {self.shape_new.value})\n',
				f'(PadAngle {self.pad_angle:0.5g})\n',
				f'(PadShape_X {self.pad_shape_x:0.5g})\n',
				f'(PadShape_Y {self.pad_shape_y:0.5g})\n',
				f'(PadCorner {self.pad_corner:.6g})\n',
				f'(PadWidth_New {self.width:.5g})\n',
				f'(PadHeight_New {self.height:.5g})\n',
				f'(Group {self.group})\n',
				f'(Standard "{self.standart}")\n',
				f'(Points\n{points}\n)\n',
				f'(PadPoints_New\n{points_new}\n)\n',
				f'(PadTerminalCount {len(self.terminals)}\n{terminals}\n)\n',
				f'(PadMask_Percent {self.mask_percent:0.2g})\n',
				f'(PadMask_EdgeGap {self.mask_edge_gap:0.1g})\n',
				f'(PadMask_SegmentGap {self.mask_segment_gap:0.1g})\n',
				f'(PadMask_SegmentSide {self.mask_segment_side:0.1g})\n',
				f'(PadMask_TopSegments {len(self.mask_top_segments)}{top_segmens}\n)\n',
				f'(PadMask_BotSegments {len(self.mask_bottom_segments)}{bottom_segmens}\n)\n',
				f')\n',
			])


if __name__ == "__main__":
	pass