#!/usr/'bi'n/python3
#-*- coding: utf-8 -*-

import math
from typing import List
from DipTracePin import DipTracePin
from DipTraceEnums import DipTracePinOrientation, DipTraceComponentShapeType
from DipTraceComponent import DipTraceComponent
from DipTraceComponentPart import DipTraceComponentPart
from DipTracePatternLibrary import DipTracePatternLibrary
from DipTraceComponentShape import DipTraceComponentShape
from DipTraceComponentLibrary import DipTraceComponentLibrary

class SMAJ:
	_data = [
		{'uni': 'SMAJ5.0A', 'bi': 'SMAJ5.0CA', 'voltage': 5.0},
		{'uni': 'SMAJ6.0A', 'bi': 'SMAJ6.0CA', 'voltage': 6.0},
		{'uni': 'SMAJ6.5A', 'bi': 'SMAJ6.5CA', 'voltage': 6.5},
		{'uni': 'SMAJ7.0A', 'bi': 'SMAJ7.0CA', 'voltage': 7.0},
		{'uni': 'SMAJ7.5A', 'bi': 'SMAJ7.5CA', 'voltage': 7.5},
		{'uni': 'SMAJ8.0A', 'bi': 'SMAJ8.0CA', 'voltage': 8.0},
		{'uni': 'SMAJ8.5A', 'bi': 'SMAJ8.5CA', 'voltage': 8.5},
		{'uni': 'SMAJ9.0A', 'bi': 'SMAJ9.0CA', 'voltage': 9.0},
		{'uni': 'SMAJ10A' , 'bi': 'SMAJ10CA' , 'voltage': 10.0},
		{'uni': 'SMAJ11A' , 'bi': 'SMAJ11CA' , 'voltage': 11.0},
		{'uni': 'SMAJ12A' , 'bi': 'SMAJ12CA' , 'voltage': 12.0},
		{'uni': 'SMAJ13A' , 'bi': 'SMAJ13CA' , 'voltage': 13.0},
		{'uni': 'SMAJ14A' , 'bi': 'SMAJ14CA' , 'voltage': 14.0},
		{'uni': 'SMAJ15A' , 'bi': 'SMAJ15CA' , 'voltage': 15.0},
		{'uni': 'SMAJ16A' , 'bi': 'SMAJ16CA' , 'voltage': 16.0},
		{'uni': 'SMAJ17A' , 'bi': 'SMAJ17CA' , 'voltage': 17.0},
		{'uni': 'SMAJ18A' , 'bi': 'SMAJ18CA' , 'voltage': 18.0},
		{'uni': 'SMAJ20A' , 'bi': 'SMAJ20CA' , 'voltage': 20.0},
		{'uni': 'SMAJ22A' , 'bi': 'SMAJ22CA' , 'voltage': 22.0},
		{'uni': 'SMAJ24A' , 'bi': 'SMAJ24CA' , 'voltage': 24.0},
		{'uni': 'SMAJ26A' , 'bi': 'SMAJ26CA' , 'voltage': 26.0},
		{'uni': 'SMAJ28A' , 'bi': 'SMAJ28CA' , 'voltage': 28.0},
		{'uni': 'SMAJ30A' , 'bi': 'SMAJ30CA' , 'voltage': 30.0},
		{'uni': 'SMAJ33A' , 'bi': 'SMAJ33CA' , 'voltage': 33.0},
		{'uni': 'SMAJ36A' , 'bi': 'SMAJ36CA' , 'voltage': 36.0},
		{'uni': 'SMAJ40A' , 'bi': 'SMAJ40CA' , 'voltage': 40.0},
		{'uni': 'SMAJ43A' , 'bi': 'SMAJ43CA' , 'voltage': 43.0},
		{'uni': 'SMAJ45A' , 'bi': 'SMAJ45CA' , 'voltage': 45.0},
		{'uni': 'SMAJ48A' , 'bi': 'SMAJ48CA' , 'voltage': 48.0},
		{'uni': 'SMAJ51A' , 'bi': 'SMAJ51CA' , 'voltage': 51.0},
		{'uni': 'SMAJ54A' , 'bi': 'SMAJ54CA' , 'voltage': 54.0},
		{'uni': 'SMAJ58A' , 'bi': 'SMAJ58CA' , 'voltage': 58.0},
		{'uni': 'SMAJ60A' , 'bi': 'SMAJ60CA' , 'voltage': 60.0},
		{'uni': 'SMAJ64A' , 'bi': 'SMAJ64CA' , 'voltage': 64.0},
		{'uni': 'SMAJ70A' , 'bi': 'SMAJ70CA' , 'voltage': 70.0},
		{'uni': 'SMAJ75A' , 'bi': 'SMAJ75CA' , 'voltage': 75.0},
		{'uni': 'SMAJ78A' , 'bi': 'SMAJ78CA' , 'voltage': 78.0},
		{'uni': 'SMAJ85A' , 'bi': 'SMAJ85CA' , 'voltage': 85.0},
		{'uni': 'SMAJ90A' , 'bi': 'SMAJ90CA' , 'voltage': 90.0},
		{'uni': 'SMAJ100A', 'bi': 'SMAJ100CA', 'voltage': 100.0},
		{'uni': 'SMAJ110A', 'bi': 'SMAJ110CA', 'voltage': 110.0},
		{'uni': 'SMAJ120A', 'bi': 'SMAJ120CA', 'voltage': 120.0},
		{'uni': 'SMAJ130A', 'bi': 'SMAJ130CA', 'voltage': 130.0},
		{'uni': 'SMAJ150A', 'bi': 'SMAJ150CA', 'voltage': 150.0},
		{'uni': 'SMAJ160A', 'bi': 'SMAJ160CA', 'voltage': 160.0},
		{'uni': 'SMAJ170A', 'bi': 'SMAJ170CA', 'voltage': 170.0},
		{'uni': 'SMAJ180A', 'bi': 'SMAJ180CA', 'voltage': 180.0},
		{'uni': 'SMAJ200A', 'bi': 'SMAJ200CA', 'voltage': 200.0},
		{'uni': 'SMAJ220A', 'bi': 'SMAJ220CA', 'voltage': 220.0},
		{'uni': 'SMAJ250A', 'bi': 'SMAJ250CA', 'voltage': 250.0},
		{'uni': 'SMAJ300A', 'bi': 'SMAJ300CA', 'voltage': 300.0},
		{'uni': 'SMAJ350A', 'bi': 'SMAJ350CA', 'voltage': 350.0},
		{'uni': 'SMAJ400A', 'bi': 'SMAJ400CA', 'voltage': 400.0},
		{'uni': 'SMAJ440A', 'bi': 'SMAJ440CA', 'voltage': 440.0}
	]

	def __init__(self) -> None:
		self.pattern_lib = DipTracePatternLibrary().load('patterns.asc')
		super().__init__()

	def _pin(self):
		return [
			DipTracePin()
				.setNumber(1)
				.setOrientation(DipTracePinOrientation.Left)
				.setPosition(2.54, 0.0)
				.setLength(2.54),
			DipTracePin()
				.setNumber(2)
				.setOrientation(DipTracePinOrientation.Right)
				.setPosition(-2.54, 0.0)
				.setLength(2.54)
		]

	def _pin_shape_uni(self) -> list:
		x = 1.27 * math.sin(math.radians(60.0))

		return [
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(-2.54, 0.0)
				.addPoint( 2.54, 0.0)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Poliline)
				.addPoint(-x,  1.27)
				.addPoint( x,  0.00)
				.addPoint(-x, -1.27)
				.addPoint(-x,  1.27)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Poliline)
				.addPoint(x + 1.27/2,  1.27)
				.addPoint(x         ,  1.27)
				.addPoint(x         , -1.27)
				.addPoint(x - 1.27/2, -1.27)
				.setLocked(True)
		]

	def _pin_shape_bi(self) -> list:
		x = 2.54 * math.sin(math.radians(60.0))

		return [
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(-2.54, 0.0)
				.addPoint( 2.54, 0.0)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Poliline)
				.addPoint(0.0, 0.0)
				.addPoint(-x,  1.27)
				.addPoint(-x, -1.27)
				.addPoint(0.0, 0.0)
				.addPoint( x,  1.27)
				.addPoint( x, -1.27)
				.addPoint(0.0, 0.0)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Poliline)
				.addPoint( 1.27/2,  1.27)
				.addPoint(    0.0,  1.27)
				.addPoint(    0.0, -1.27)
				.addPoint(-1.27/2, -1.27)
				.setLocked(True)
		]

	def _pattern_uni(self):
		return self.pattern_lib.pattern('DIOM520X255X230L115X155N')

	def _pattern_bi(self):
		return self.pattern_lib.pattern('DIONM520X255X230L115X155N')

	def _component_tvs_uni(self, name: str, voltage:float):
		return DipTraceComponent(name, 'D', voltage) \
			.setPattern(self._pattern_uni()) \
			.addPart(DipTraceComponentPart(name)
				.setValue(f'{voltage:.5g} V')
				.addShape(self._pin_shape_uni())
				.addPin(self._pin()))

	def _component_tvs_bi(self, name: str, voltage:float):
		return DipTraceComponent(name, 'D', voltage) \
			.setPattern(self._pattern_bi()) \
			.addPart(DipTraceComponentPart(name)
				.setValue(f'{voltage:.5g} V')
				.addShape(self._pin_shape_bi())
				.addPin(self._pin()))

	def _smaj(self) -> List[DipTraceComponent]:
		result = []
		result.extend([self._component_tvs_uni(component['uni'], component['voltage']) for component in self._data])
		result.extend([self._component_tvs_uni(component['uni'], component['voltage']) for component in self._data])
		return result

	def run(self) -> None:
		lib = DipTraceComponentLibrary().setName('Diodes TVS')
		lib.addComponent(self._smaj())
		lib.save('Diodes TVS.component.asc')


if __name__ == "__main__":
	SMAJ().run()
