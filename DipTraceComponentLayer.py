#!/usr/bin/python3
#-*- coding: utf-8 -*-

from io import TextIOWrapper
from typing import List, Union
from reHelper import searchSingleBool, searchSingleInt

class DipTraceComponentLayer:

	def __init__(self) -> None:
		self.pins   = []
		self.shapes = []
		self.setEnabled()
		self.setNumber()
		super().__init__()

	def setEnabled(self, state:bool=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def setNumber(self, number:int=0):
		self.number = number
		return self

	def addPin(self, pin:Union[int,List[int]]):
		if type(pin) == list:
			self.pins.extend(pin)
		else:
			self.pins.append(pin)
		return self

	def addShape(self, shape:Union[int,List[int]]):
		if type(shape) == list:
			self.shapes.extend(shape)
		else:
			self.shapes.append(shape)
		return self

	def load(self, datafile:TextIOWrapper):
		while line := datafile.readline().strip():

			if line == ')':
				break

			elif tmp := searchSingleBool(r'Enabled', line):
				self.enabled = tmp.group(1)

			elif tmp := searchSingleInt(r'Number', line):
				self.number = int(tmp.group(1))

			elif line == '(Pins':
				while line := datafile.readline().strip():
					if line == ')':
						break
					elif tmp := searchSingleInt(r'pt', line):
						self.addPin(int(tmp.group(1)))

			elif line == '(Shapes':
				while line := datafile.readline().strip():
					if line == ')':
						break
					elif tmp := searchSingleInt(r'pt', line):
						self.addShape(int(tmp.group(1)))

		return self


	def __str__(self) -> str:

		pins   = '\n'.join(f'(pt {pin})'   for pin   in self.pins)
		shapes = '\n'.join(f'(pt {shape})' for shape in self.shapes)

		return ''.join([
			f'(Layer\n',
			f'(Enabled "{self.enabled}")\n',
			f'(Number {self.number})\n',
			f'(Pins\n{pins}\n)\n' if self.number != 2 else '',       #TODO: Check this hack
			f'(Shapes\n{shapes}\n)\n' if self.number != 2 else '',   #TODO: Check this hack
			f')\n',
		])


if __name__ == "__main__":
	pass