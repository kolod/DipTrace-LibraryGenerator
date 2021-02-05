#!/usr/bin/python3
#-*- coding: utf-8 -*-

from DipTraceUnits import mm2units
from DipTraceEnums import DipTracePinType, DipTracePinElectric, DipTracePinOrientation

class DipTracePin:

	def __init__(self):
		self.setName()
		self.setNumber()
		self.setType()
		self.setLocked()
		self.setEnabled()
		self.setElectric()
		self.setOrientation()
		self.setLength()
		self.setShowName()
		super().__init__()

	def setType(self, type:DipTracePinType=DipTracePinType.Undefined):
		self.type = type
		return self

	def setName(self, name:str=''):
		self.name = name
		return self

	def setNumber(self, number:int=0):
		self.number = number
		return self

	def setLocked(self, state:bool=False):
		self.locked = 'Y' if state else 'N'
		return self

	def setEnabled(self, state:bool=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def setShowName(self, state:bool=False):
		self.show = 'Y' if state else 'N'
		return self

	def setElectric(self, electric:DipTracePinElectric=DipTracePinElectric.Undefined):
		self.electric = electric
		return self

	def setOrientation(self, orientation:DipTracePinOrientation=DipTracePinOrientation.Right):
		self.orientation = orientation
		return self

	def setPosition(self, x:float=0.0, y:float=0.0):
		self.x = mm2units(x)
		self.y = mm2units(y)
		return self

	def setLength(self, length:float=3.81):
		self.length = mm2units(length)
		return self

	def __str__(self):
		return ''.join([
			f'(Pin {"{0}"} {self.x:.6g} {self.y:.6g}\n',
			f'(Enabled "{self.enabled}")\n',
			f'(Locked "{self.locked}")\n',
			f'(ModelSig "")\n',
			f'(Type {self.type.value})\n',
			f'(Orientation {self.orientation.value})\n',
			f'(Number {self.number})\n',
			f'(Length {self.length})\n',
			f'(Name "{self.name if len(self.name) else str(self.number)}")\n',
			f'(StringNumber "{self.number}")\n',
			f'(ShowName "{self.show}")\n',
			f'(PinNumXShift 0)\n',
			f'(PinNumYShift 0)\n',
			f'(PinNamexShift 0)\n',
			f'(PinNameYShift 0)\n',
			f'(ElectricType {self.electric.value})\n',
			f'(NameFontSize 5)\n',
			f'(NameFontWidth -2)\n',
			f'(NameFontScale 1)\n',
			f'(SignalDelay 0)\n',
			f'(Group -1)\n',
			f'(PinNumRotate 0)\n',
			f'(PinNameRotate 0)\n',
			f')\n',
		])

if __name__ == "__main__":
	pass