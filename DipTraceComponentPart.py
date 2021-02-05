#!/usr/bin/python3
#-*- coding: utf-8 -*-

from DipTracePatternShape import DipTracePatternShape
from DipTraceComponentShape import DipTraceComponentShape
from typing import List, Union
from DipTraceUnits import mm2units
from DipTraceEnums import DipTraceComponentPartType
from DipTracePin import DipTracePin
from DipTraceComponentLayer import DipTraceComponentLayer


class DipTraceComponentPart:

	def __init__(self, name:str, type:DipTraceComponentPartType=DipTraceComponentPartType.Normal):
		self.shapes:List[DipTraceComponentShape] = []
		self.layers:List[DipTraceComponentLayer] = []
		self.pins:List[DipTracePin] = []
		self.name = name
		self.type = type
		self.setType()
		self.setPartName()
		self.setRef()
		self.setValue()
		self.setEnabled()
		self.setOrigin()
		self.setSize()
		self.setShowNumbers()
		super().__init__()

	def setPartName(self, name:str='Part 1'):
		self.part_name = name
		return self

	def setType(self, type:DipTraceComponentPartType=DipTraceComponentPartType.Normal):
		self.type = type
		return self

	def setRef(self, ref:str=''):
		self.ref = ref
		return self

	def setValue(self, value:str=''):
		self.value = value
		return self

	def setEnabled(self, state:bool=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def addPin(self, pin:Union[DipTracePin, List[DipTracePin]]):
		if type(pin) is list:
			self.pins.extend(pin)
		else:
			self.pins.append(pin)
		return self

	def addLayer(self, layer:Union[DipTraceComponentLayer, List[DipTraceComponentLayer]]):
		if type(layer) is list:
			self.layers.extend(layer)
		else:
			self.layers.append(layer)
		return self

	def addShape(self, shape:Union[DipTracePatternShape, List[DipTracePatternShape]]):
		if type(shape) is list:
			self.shapes.extend(shape)
		else:
			self.shapes.append(shape)
		return self

	def setShowNumbers(self, state:bool=True):
		self.show_numbers = 1 if state else 0
		return self

	def setOrigin(self, x:float=0.0, y:float=0.0):
		self.origin_x = mm2units( x )
		self.origin_y = mm2units( y )
		return self

	def setSize(self, width:float=0.0, height:float=0.0):
		self.width  = mm2units(  width )
		self.height = mm2units( height )
		return self

	def __str__(self) -> str:

		pins        = '\n'.join([str(self.pins[i]).format(i)   for i in range(len(self.pins))  ])
		shapes      = '\n'.join([str(self.shapes[i]).format(i) for i in range(len(self.shapes))])
		groups      = '\n'
		layers      = '\n'.join([str(layer) for layer in self.layers])
		user_fields = '\n'

		return ''.join([
			f'(Part "{self.name}" "{self.ref}"\n',
			f'(Enabled "{self.enabled}")\n',
			f'(PartType {self.type.value})\n',
			f'(PartName "{self.part_name}")\n',
			f'(ShowNumbers {self.show_numbers})\n',
			f'(Type {self.type.value})\n',
			f'(Number1 0)\n',
			f'(Number2 0)\n',
			f'(Width {self.width})\n',
			f'(Height {self.height})\n',
			f'(Value "{self.value}")\n',
			f'(LockProperties "N")\n',
			f'(OriginX {self.origin_x:.6g})\n',
			f'(OriginY {self.origin_y:.6g})\n',
			f'(Datasheet "")\n',
			f'(ModelType 0)\n',
			f'(ModelString "")\n',
			f'(ModelBody\n)\n',
			f'(Manufacturer "")\n',
			f'(CategoryName "Connectors")\n',
			f'(CategoryIndex -1)\n',
			f'(CategoryTypes 0\n)\n',
			f'(SubfolderIndex 1)\n',
			f'(Verification "N" "N" "N" "N" "N" "N" "N")\n',
			f'(Pins\n{pins}\n)\n'     if len(self.pins)   else '',
			f'(Shapes\n{shapes}\n)\n' if len(self.shapes) else '',
			f'(Groups\n{groups}\n)\n',
			f'(Layers\n{layers}\n)\n',
			f'(UserFields\n{user_fields}\n)\n',
			f')\n'
		])

if __name__ == "__main__":
	pass