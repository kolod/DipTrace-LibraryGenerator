#!/usr/bin/python3
#-*- coding: utf-8 -*-

from DipTraceUnits import mm2units

class DipTracePoint:

	def __init__(self, x:float=0.0, y:float=0.0):
		self.x = mm2units(x)
		self.y = mm2units(y)
		super().__init__()

	def move(self, x:float=0.0, y:float=0.0):
		self.x += mm2units(x)
		self.y += mm2units(y)
		return self

	def __str__(self) -> str:
		return f'(pt {self.x:.6g} {self.y:.6g})'

if __name__ == "__main__":
	pass