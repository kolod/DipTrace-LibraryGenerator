#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from typing import  Literal, Optional, AnyStr
from reHelper import reBracketed, reJoin, reBool, reFloat, reInt
from DipTraceUnits import mm2units

class DipTraceHole:

	def __init__(self, match:re.Match[AnyStr]) -> None:
		self.setEnabled()
		self.setLocked()
		self.setPosition()
		self.setHole()
		self.setKeepout()
		self.setGroup()
		if match:
			self.enabled = match.group(1)
			self.locked  = match.group(2)
			self.x       = float(match.group(3))
			self.y       = float(match.group(4))
			self.keepout = float(match.group(5))
			self.hole    = float(match.group(6))
			self.group   = int(match.group(7))
		super().__init__()

	def setEnabled(self, state:bool=False):
		self.enabled = 'Y' if state else 'N'
		return self

	def setLocked(self, state:bool=False):
		self.locked = 'Y' if state else 'N'
		return self

	def setPosition(self, x:float=0.0, y:float=0.0):
		self.x = mm2units(x)
		self.y = mm2units(y)
		return self

	def setHole(self, hole:float=0.0):
		self.hole = mm2units(hole)
		return self

	def setKeepout(self, keepout:float=0.0):
		self.keepout = mm2units(keepout)
		return self

	def setGroup(self, group:int=-1):
		self.group = group
		return self

	def move(self, x:float=0.0, y:float=0.0):
		self.x += mm2units(x)
		self.y += mm2units(y)
		return self

	@staticmethod
	def pattern() -> Literal:
		return reBracketed(reJoin(r'Hole', reBool, reBool, reFloat, reFloat, reFloat, reFloat, reInt))

	def __str__(self) -> str:
		return f'(Hole "{self.enabled}" "{self.locked}" {self.x:.5g} {self.y:.5g} {self.keepout:.5g} {self.hole:.5g} {self.group})'


if __name__ == "__main__":
	pass