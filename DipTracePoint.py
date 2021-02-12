#!/usr/bin/python3
#-*- coding: utf-8 -*-

from pyfields import field
from DipTraceUnits import mm2units

class DipTracePoint:

	x       :float = field(native=True, default=0.0  , doc='X coortinate')
	y       :float = field(native=True, default=0.0  , doc='Y coortinate')
	convert :bool  = field(native=True, default=False, doc='If the conversion flag set to the "True" str() method do coordinates conversion.')

	def __init__(self, x:float = 0.0, y:float = 0.0, convert:bool=True) -> None:
		self.x = x
		self.y = y
		self.convert = convert
		super().__init__()

	def move(self, x:float=0.0, y:float=0.0):
		self.x += x
		self.y += y
		return self

	def __str__(self) -> str:
		x = mm2units(self.x) if self.convert else self.x
		y = mm2units(self.y) if self.convert else self.y
		return f'(pt {x:.5g} {-y+0:.5g})'

if __name__ == "__main__":
	pass