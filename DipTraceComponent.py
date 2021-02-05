#!/usr/bin/python3
#-*- coding: utf-8 -*-

from typing import List, Union
from DipTracePatternLibrary import DipTracePattern
from DipTraceComponentPart import DipTraceComponentPart

class DipTraceComponent:

	def __init__(self, name:str, ref:str='', value:str=None):
		self.name   = name
		self.value  = value or name
		self.ref    = ref
		self.parts  = []
		super().__init__()

	def setPattern(self, pattern:DipTracePattern):
		self.pattern = pattern
		return self

	def addPart(self, part:Union[DipTraceComponentPart, List[DipTraceComponentPart]]):
		if type(part) == list:
			self.parts.extend(part)
		else:
			self.parts.append(part)
		return self

	def __str__(self) -> str:
		parts       = '\n'.join([str(part) for part in self.parts])
		pattern     = str(self.pattern) if hasattr(self, 'pattern') else ''

		return '\n'.join([
			f'(Component\n',
			f'{parts}\n',
			f'{pattern}\n',
			f')\n'
		])

if __name__ == "__main__":
	pass