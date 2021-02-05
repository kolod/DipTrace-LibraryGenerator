#!/usr/bin/python3
#-*- coding: utf-8 -*-

from DipTraceCategoryType import DipTraceCategoryType
from DipTracePatternShape import DipTracePatternShape
import textwrap
from reHelper import searchSingleString
from DipTraceUnits import mm2units
from DipTraceEnums import DipTracePinType, DipTracePinElectric, DipTracePinOrientation, DipTraceComponentPartType
from DipTracePatternLibrary import DipTracePattern
from DipTraceIndentation import DipTraceIndentation
from DipTraceComponent import DipTraceComponent
from DipTracePad import DipTracePad

class DipTraceComponentLibrary:

	def __init__(self):
		self.components = []
		self.setName()
		self.setHint()
		super().__init__()

	def setName(self, name:str=''):
		self.name = name
		return self

	def setHint(self, hint:str=''):
		self.hint = hint
		return self

	def addComponent(self, component:DipTraceComponent):
		if type(component) is list:
			self.components.extend(component)
		else:
			self.components.append(component)
		return self

	def __str__(self) -> str:
		DipTracePad.isComponent          = True # Fix for DipTracePad
		DipTracePattern.isComponent      = True # Fix for DipTracePattern
		DipTracePatternShape.isComponent = True # Fix for DipTracePatternShape
		DipTraceCategoryType.isComponent = True # Fix for DipTraceCategoryType

		components = '\n'.join([str(component) for component in self.components])

		return DipTraceIndentation(''.join([
			f'(Source "DipTrace-ElementLibrary" 28)\n',
			f'(Library\n',
			f'(Name "{self.name}")\n',
			f'(Hint "{self.hint}")\n',
			f'(Subfolders\n)\n',
			f'(Categories 0\n)\n',
			f'(Components\n{components})\n',
			f')\n',
			f'()\n',
		]))

	def save(self, filename:str):
		with open(filename, 'w', encoding='cp1251') as datafile:
			datafile.write(str(self))

if __name__ == "__main__":
	pass