#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from io import TextIOWrapper
from typing import  Literal, AnyStr, List, Any
from pyfields import field
from DipTraceBool import DipTraceBool
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

	points                :List[DipTracePoint]        = field(default=[], doc='Points for DipTrace format lower then version 4.0.')
	points_new            :List[DipTracePoint]        = field(default=[], doc='Points for DipTrace format version 4.0 or above.')
	terminals             :List[DipTraceTerminal]     = field(default=[], doc='Terminals.')
	mask_top_segments     :list                       = field(default=[])
	mask_bottom_segments  :list                       = field(default=[])
	name                  :str                        = field(default='', doc='Pad name.')
	note                  :str                        = field(default='', doc='Pad note.')
	number                :int                        = field(default=0, doc='Pad number')
	group                 :int                        = field(default=0, doc='Group number')
	x                     :float                      = field(default=0.0, doc='X coortinate')
	y                     :float                      = field(default=0.0, doc='Y coortinate')
	width                 :float                      = field(default=0.0, doc='Width')
	height                :float                      = field(default=0.0, doc='Height')
	shape                 :DipTracePadShapes          = field(default=DipTracePadShapes.Oval, doc='Pad shape for DipTrace format lower then version 4.0.')
	shape_new             :DipTracePadShapesNew       = field(default=DipTracePadShapes.Oval, doc='Pad shape for DipTrace format version 4.0 or above.')
	hole_type             :DipTraceHoleTypes          = field(default=DipTraceHoleTypes.Round, doc='Hole type')
	hole_width            :float                      = field(default=0.0, doc='Hole width')
	hole_height           :float                      = field(default=0.0, doc='Hole height')
	standart              :DipTraceBool               = field(default=DipTraceBool(True), doc="Use pattern's standart pad properties.")
	surface               :DipTraceBool               = field(default=DipTraceBool(True), doc="Surface mount pattern.")
	locked                :DipTraceBool               = field(default=DipTraceBool(False), doc='Locking shape')
	inverted              :DipTraceBool               = field(default=DipTraceBool(False), doc='Inverted')
	sided                 :DipTraceBool               = field(default=DipTraceBool(False), doc='Sided')
	mask_percent          :float                      = field(default=0.0, doc='')
	mask_edge_gap         :float                      = field(default=0.0, doc='')
	mask_segment_gap      :float                      = field(default=0.0, doc='')
	mask_segment_side     :int                        = field(default=0, doc='')
	mask_top_segments     :List[List[float]]          = field(default=[], doc='')
	mask_bottom_segments  :List[List[float]]          = field(default=[], doc='')
	custom_swell          :float                      = field(default=0.0, doc='')
	custom_swell_new      :float                      = field(default=0.0, doc='')
	custom_shrink         :float                      = field(default=0.0, doc='')
	custom_shrink_new     :float                      = field(default=0.0, doc='')
	pad_angle             :float                      = field(default=0.0, doc='Pad angle')
	pad_shape_x           :float                      = field(default=0.0, doc='Pad shape X')
	pad_shape_y           :float                      = field(default=0.0, doc='Pad shape Y')
	pad_corner            :float                      = field(default=0.0, doc='Pad corner')

	def __init__(self, match:re.Match[AnyStr]=None):
		if match:
			self.number = int(match.group(1))
			self.name   = match.group(2)
			self.note   = match.group(3)
			self._x     = float(match.group(4))
			self._y     = float(match.group(5))
		super().__init__()

	@staticmethod
	def _mask(match:re.Match[Any]):
		result= []
		if match.lastindex >= 1: result.append(match.group(1))
		if match.lastindex >= 2: result.append(int(match.group(2)))
		if match.lastindex >= 3: result.append(int(match.group(3)))
		return result

	def move(self, x:float=0.0, y:float=0.0):
		self._x += mm2units( x )
		self._y += mm2units( y )
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
					if tmp := re.search(reBracketed(reJoin(r'pt', reFloat, reFloat, reFloat, reFloat)), line):
						if tmp.lastindex >= 4:
							self.mask_top_segments.append([tmp.group(i+1) for i in range(4)])

			elif line.startswith('(PadMask_BotSegments '):
				while line := datafile.readline().strip():
					if line == ')':
						break
					if tmp := re.search(reBracketed(reJoin(r'pt', reFloat, reFloat, reFloat, reFloat)), line):
						if tmp.lastindex >= 4:
							self.mask_bottom_segments.append([tmp.group(i+1) for i in range(4)])

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
				self.top_mask = self._mask(tmp)

			elif tmp := re.search(reBracketed(reJoin(r'DisableBottomMask', r'"([YN]?)" ([-]?\d*)\s*([-]?\d*)')), line):
				self.bottom_mask = self._mask(tmp)

			elif tmp := re.search(reBracketed(reJoin(r'DisableTopPaste', r'"([YN]?)" ([-]?\d*)\s*([-]?\d*)')), line):
				self.top_paste = self._mask(tmp)

			elif tmp := re.search(reBracketed(reJoin(r'DisableBottomPaste', r'"([YN]?)" ([-]?\d*)\s*([-]?\d*)')), line):
				self.bottom_paste = self._mask(tmp)

		return self

	def __str__(self):
		points         = '\n'.join([str(point) for point in self.points     ])
		points_new     = '\n'.join([str(point) for point in self.points_new ])
		terminals      = '\n'.join([str(point) for point in self.terminals  ])
		top_segmens    = '\n'.join([f'(pt {s[0]:.5g} {s[1]:.5g} {s[2]:.5g} {s[3]:.5g}' for s in self.mask_top_segments   ])
		bottom_segmens = '\n'.join([f'(pt {s[0]:.5g} {s[1]:.5g} {s[2]:.5g} {s[3]:.5g}' for s in self.mask_bottom_segments])

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
				f'(Pad {"{0}"} "{self.name}" "{self.note}" {self._x:.5g} {self._y:.5g}\n',
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
				f'(PadMask_TopSegments {len(self.mask_top_segments)}\n{top_segmens}\n)\n',
				f'(PadMask_BotSegments {len(self.mask_bottom_segments)}\n{bottom_segmens}\n)\n',
				f')\n',
			])
		else:
			return ''.join([
				f'(Pad {"{0}"} "{self.name}" "{self.note}" {self._x:.5g} {self._y:.5g}\n',
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
				f'(PadPoints_New\n{points_new}\n)\n' if len(self.points_new) else '',
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