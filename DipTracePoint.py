#!/usr/bin/python3
#-*- coding: utf-8 -*-

from DipTraceUnits import mm2units

class DipTracePoint:

	def __init__(self, x:float=0.0, y:float=0.0):
		self.x = mm2units( x )
		self.y = mm2units( y )

	def move(self, x:float=0.0, y:float=0.0):
		self.x += mm2units( x )
		self.y += mm2units( y )
		return self

	def __str__(self) -> str:
		return '(pt {0.x:.5g} {0.y:.5g})'.format(self)


if __name__ == "__main__":
	pass