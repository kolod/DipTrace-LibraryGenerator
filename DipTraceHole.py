#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from typing import  Literal, Optional, AnyStr
from pyfields import field
from reHelper import reBracketed, reJoin, reBool, reFloat, reInt
from DipTraceUnits import mm2units
from DipTraceBool import DipTraceBool

class DipTraceHole:

	enabled  :DipTraceBool  = field(default=DipTraceBool(True), doc='Enabling shape')
	locked   :DipTraceBool  = field(default=DipTraceBool(False), doc='Locking shape')
	x        :float         = field(native=True, default=0.0, doc='X coortinate')
	y        :float         = field(native=True, default=0.0, doc='Y coortinate')
	hole     :float         = field(native=True, default=0.0, doc='Hole diameter')
	keepout  :float         = field(native=True, default=0.0, doc='Keepout diameter')
	group    :int           = field(default=0, doc='Group number')

	@enabled.converter(accepts=bool)
	@locked.converter(accepts=bool)
	def toDipTraceBool(self, field, value):
		return DipTraceBool(value)

	def __init__(self, match:Optional[re.Match[AnyStr]] = None) -> None:
		if match:
			self.enabled = match.group(1)
			self.locked  = match.group(2)
			self.x       = float(match.group(3))
			self.y       = float(match.group(4))
			self.keepout = float(match.group(5))
			self.hole    = float(match.group(6))
			self.group   = int(match.group(7))
		super().__init__()

	def recalculate(self, origin_x:float, origin_y:float):
		self.x += origin_x
		self.y -= origin_y

	def move(self, x:float=0.0, y:float=0.0):
		self.x += x
		self.y += y
		return self

	@staticmethod
	def pattern() -> Literal:
		return reBracketed(reJoin(r'Hole', reBool, reBool, reFloat, reFloat, reFloat, reFloat, reInt))

	def __str__(self) -> str:
		return f'(Hole "{self.enabled}" "{self.locked}" {mm2units(self.x):.5g} {mm2units(-self.y):.5g} {mm2units(self.keepout):.5g} {mm2units(self.hole):.5g} {self.group})'


if __name__ == "__main__":
	pass