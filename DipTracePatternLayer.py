#!/usr/bin/python3
#-*- coding: utf-8 -*-

from io import TextIOWrapper
from typing import List, Union
from reHelper import searchSingleBool, searchSingleInt

class DipTracePatternLayer:

	def __init__(self) -> None:
		self.pads   = []
		self.shapes = []
		self.holes  = []
		self.setEnabled()
		self.setNumber()
		super().__init__()

	def setEnabled(self, state:bool=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def setNumber(self, number:int=0):
		self.number = number
		return self

	def addPad(self, pad:Union[int, List[int]]):
		if type(pad) == list:
			self.pads.extend(pad)
		else:
			self.pads.append(pad)
		return self

	def addShape(self, shape:Union[int, List[int]]):
		if type(shape) == list:
			self.shapes.extend(shape)
		else:
			self.shapes.append(shape)
		return self

	def addHole(self, hole:Union[int, List[int]]):
		if type(hole) == list:
			self.holes.extend(hole)
		else:
			self.holes.append(hole)
		return self

	def load(self, datafile:TextIOWrapper):
		while line := datafile.readline().strip():

			if line == ')':
				break

			elif tmp := searchSingleBool(r'Enabled', line):
				self.enabled = tmp.group(1)

			elif tmp := searchSingleInt(r'Number', line):
				self.number = int(tmp.group(1))

			elif line == '(Pads':
				while line := datafile.readline().strip():
					if line == ')':
						break
					elif tmp := searchSingleInt(r'pt', line):
						self.addPad(int(tmp.group(1)))

			elif line == '(Shapes':
				while line := datafile.readline().strip():
					if line == ')':
						break
					elif tmp := searchSingleInt(r'pt', line):
						self.addShape(int(tmp.group(1)))

			elif line == '(Holes':
				while line := datafile.readline().strip():
					if line == ')':
						break
					elif tmp := searchSingleInt(r'pt', line):
						self.addHole(int(tmp.group(1)))

		return self


	def __str__(self) -> str:

		pads   = '\n'.join(f'(pt {pad})'   for pad   in self.pads)
		shapes = '\n'.join(f'(pt {shape})' for shape in self.shapes)
		holes  = '\n'.join(f'(pt {hole})'  for hole  in self.holes)

		return ''.join([
			f'(Layer\n',
			f'(Enabled "{self.enabled}")\n',
			f'(Number {self.number})\n',
			f'(Pads\n{pads}\n)\n' if self.number != 2 else '',       #TODO: Check this hack
			f'(Shapes\n{shapes}\n)\n' if self.number != 2 else '',   #TODO: Check this hack
			f'(Holes\n{holes}\n)\n',
			f')\n',
		])


if __name__ == "__main__":
	pass