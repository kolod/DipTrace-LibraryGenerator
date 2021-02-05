#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from typing import Optional
from reHelper import searchSingleString, reJoin, reInt
from DipTracePad import DipTracePad
from DipTracePattern import DipTracePattern
from DipTraceIndentation import DipTraceIndentation

class DipTracePatternLibrary:

	def __init__(self, name:str='', hint:str=None) -> None:

		self.name = name
		self.hint = hint or name
		self.patterns = []
		super().__init__()

	def addPattern(self, pattern:DipTracePattern):
		self.patterns.append(pattern)
		return self

	def pattern(self, name:str) -> Optional[DipTracePattern]:
		for pattern in self.patterns:
			if name == pattern.name:
				return pattern
		return None

	def save(self, filename:str) -> None:
		with open(filename, 'w', encoding='cp1251') as datafile:
			datafile.write(str(self))

	def load(self, filename:str):
		with open(filename, 'r', encoding='cp1251') as datafile:
			while line := datafile.readline().strip():

				if tmp := searchSingleString(r'Name', line):
					self.name = tmp.group(1); continue

				elif tmp := searchSingleString(r'Hint', line):
					self.hint = tmp.group(1); continue

				elif tmp := re.search(reJoin('\(Categories', reInt), line):
					while line := datafile.readline().strip():
						if line == ')':
							break

				elif line == '(Patterns':
					while line := datafile.readline().strip():
						if line == ')':
							break
						if tmp := re.search(DipTracePattern.pattern(), line):
							self.addPattern(DipTracePattern(match=tmp).load(datafile))

		return self

	def __str__(self) -> str:
		DipTracePattern.isComponent = False # Fix for DipTracePattern
		DipTracePad.isComponent     = False # Fix for DipTracePattern

		patterns = '\n'.join([str(pattern) for pattern in self.patterns])

		return DipTraceIndentation(''.join([
			f'(Source "DipTrace-ComLibrary" 21)\n',
			f'(Library\n',
			f'(Size {len(self.patterns)})\n',
			f'(Name "{self.name}")\n',
			f'(Hint "{self.hint}")\n',
			f'(Categories 0\n)\n',
			f'(Patterns\n{patterns}\n)\n',
			f')\n',
			f'()\n'
		]))


if __name__ == "__main__":
	pass