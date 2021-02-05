#!/usr/bin/python3
#-*- coding: utf-8 -*-

from DipTracePatternLibrary import DipTracePattern
from DipTraceComponentPart import DipTraceComponentPart


class DipTraceComponent:

	def __init__(self, name:str, ref:str='', value:str=None):
		self.name   = name
		self.value  = value or name
		self.ref    = ref
		self.parts  = []
		super().__init__()

	def addPart(self, part:DipTraceComponentPart):
		self.parts.append(part)
		return self

	def setPattern(self, pattern:DipTracePattern):
		self.pattern = pattern
		return self

	def __str__(self) -> str:
		parts       = '\n'.join([str(part) for part in self.parts])
		pattern     = str(self.pattern) if hasattr(self, 'pattern') else ''
		groups      = ''
		layers      = ''
		user_fields = ''

		return '\n'.join([
			f'(Component\n',
			f'{parts}\n',
			f'{pattern}\n',
			f')\n'
		])

if __name__ == "__main__":
	pass