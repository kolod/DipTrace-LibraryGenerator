#!/usr/bin/python3
#-*- coding: utf-8 -*-

import math
from copy import deepcopy
from typing import List
from DipTracePin import DipTracePin
from DipTracePad import DipTracePad
from DipTraceEnums import DipTraceHoleTypes, DipTraceLayerType, DipTracePadShapesNew, DipTracePinOrientation, DipTraceTerminalShapes, DipTracePadShapes, DipTracePatternShapeType, DipTraceComponentShapeType
from DipTracePattern import DipTracePattern
from DipTrace3dModel import DipTrace3dModel
from DipTraceTerminal import DipTraceTerminal
from DipTraceComponent import DipTraceComponent
from DipTraceIndentation import DipTraceIndentation
from DipTracePatternShape import DipTracePatternShape
from DipTraceComponentPart import DipTraceComponentPart
from DipTracePatternLibrary import DipTracePatternLibrary
from DipTraceComponentShape import DipTraceComponentShape
from DipTraceComponentLibrary import DipTraceComponentLibrary

class IDC_Connectors:

	def __init__(self, name:str, pins:List[int]):
		self.pins             = pins
		self.name             = name
		self.patternlibrary   = DipTracePatternLibrary(name)
		self.componentLibrary = DipTraceComponentLibrary().setName(name)
		super().__init__()

	def _terminal(self) -> DipTraceTerminal:
		return DipTraceTerminal().setShape(DipTraceTerminalShapes.Rectangle).setSize(0.64, 0.64)

	def _model(self, pins:int, isR:bool=False) -> DipTrace3dModel:
		return DipTrace3dModel().setFilename('BH{1}-{0:02}.STEP'.format(pins, 'R' if isR else '')).setRotation(90.0).setOrigin(0,-1.5).setColor(75,75,75)

	def _pattern_shape(self, pins:int) -> List[DipTracePatternShape]:
		C      = 2.54 * int(pins/2 - 1)
		A      = C + 10.14
		bottom = (8.4 - 2.54) / 2
		top    = bottom - 8.4
		left   = (C-A)/2
		right  = (C+A)/2
		middle = C/2
		triag  = 2 / math.sqrt(3)

		shape_01 = DipTracePatternShape() \
			.type(DipTracePatternShapeType.Rectangle) \
			.addPoint(right, top) \
			.addPoint(left, bottom)

		shape_02 = DipTracePatternShape() \
			.type(DipTracePatternShapeType.Poliline) \
			.addPoint(middle - 2.5, bottom      ) \
			.addPoint(middle - 2.5, bottom - 0.5) \
			.addPoint(left   + 0.5, bottom - 0.5) \
			.addPoint(left   + 0.5, top    + 0.5) \
			.addPoint(right  - 0.5, top    + 0.5) \
			.addPoint(right  - 0.5, bottom - 0.5) \
			.addPoint(middle + 2.5, bottom - 0.5) \
			.addPoint(middle + 2.5, bottom      )

		shape_04 = DipTracePatternShape() \
			.type(DipTracePatternShapeType.Poligon) \
			.addPoint(0.0         , bottom + 1.0) \
			.addPoint(triag       , bottom + 3.0) \
			.addPoint(-triag      , bottom + 3.0)

		return [
			deepcopy(shape_01).setLineWidth(0.25).setLayer(DipTraceLayerType.TopSilk),
			deepcopy(shape_02).setLineWidth(0.25).setLayer(DipTraceLayerType.TopSilk),
			deepcopy(shape_04).setLineWidth(0.25).setLayer(DipTraceLayerType.TopSilk),
			deepcopy(shape_01).setLineWidth(0.12).setLayer(DipTraceLayerType.TopAssembly),
			deepcopy(shape_02).setLineWidth(0.12).setLayer(DipTraceLayerType.TopAssembly),
			deepcopy(shape_01).setLineWidth(0.05).setLayer(DipTraceLayerType.TopCourtyard)
		]

	def _pattern_shape_r(self, pins:int) -> List[DipTracePatternShape]:
		C        = 2.54 * int(pins/2 - 1)
		A        = C + 10.14
		top      = 0.32 - 13.8
		bottom   = top + 9.0
		left     = (C-A)/2
		right    = (C+A)/2
		middle   = C/2

		shape_01 = DipTracePatternShape() \
			.type(DipTracePatternShapeType.Rectangle) \
			.setLineWidth(0.25)\
			.addPoint(right, top) \
			.addPoint(left, bottom)

		shape_02 = DipTracePatternShape() \
			.type(DipTracePatternShapeType.Poliline) \
			.setLineWidth(0.25)\
			.addPoint(middle - 2.5, top         ) \
			.addPoint(middle - 2.5, top    + 0.5) \
			.addPoint(left   + 0.5, top    + 0.5) \
			.addPoint(left   + 0.5, bottom - 0.5) \
			.addPoint(right  - 0.5, bottom - 0.5) \
			.addPoint(right  - 0.5, top    + 0.5) \
			.addPoint(middle + 2.5, top    + 0.5) \
			.addPoint(middle + 2.5, top         )

		return [
			deepcopy(shape_01).setLineWidth(0.25).setLayer(DipTraceLayerType.TopSilk),
			deepcopy(shape_02).setLineWidth(0.25).setLayer(DipTraceLayerType.TopSilk),
			deepcopy(shape_01).setLineWidth(0.12).setLayer(DipTraceLayerType.TopAssembly),
			deepcopy(shape_02).setLineWidth(0.12).setLayer(DipTraceLayerType.TopAssembly),
			deepcopy(shape_01).setLineWidth(0.05).setLayer(DipTraceLayerType.TopCourtyard)
		]

	def _pad(self, number:int) -> DipTracePad:
		x:float = int(number / 2) *  2.54
		y:float = int(number % 2) * -2.54
		return DipTracePad()\
			.setNumber(number+1)\
			.setName(str(number+1))\
			.setPosition(x, y)\
			.setLocked(True)\
			.setSize(1.7, 1.7)\
			.setPadMask(50.0, 0.9, 0.6, 3)\
			.setHole(DipTraceHoleTypes.Round, 1.13)\
			.setStandart(number != 0)\
			.setShape(DipTracePadShapes.Rectangle if number == 0 else DipTracePadShapes.Oval)\
			.setShapeNew(DipTracePadShapesNew.Rectangle if number == 0 else DipTracePadShapesNew.Obround)\
			.setCustomShrink(-1000)\
			.setCustomShrinkNew(-1000)\
			.setCustomSwell(-1000)\
			.setCustomSwellNew(-1000)\
			.addTerminal(self._terminal())

	def _pattern(self, name:str, pin_count:int, isR:bool=False) -> DipTracePattern:
		C:float = 2.54 * int(pin_count/2 - 1)
		A:float = C + 10.14

		pattern = DipTracePattern().setName('BH{1}-{0:02}'.format(pin_count, 'R' if isR else '')).setRef('J')
		pattern.setSize(A, 11.4)
		pattern.addPad([self._pad(pin) for pin in range(pin_count)])

		if isR:
			pattern.addShape(self._pattern_shape_r(pin_count))
		else:
			pattern.addShape(self._pattern_shape(pin_count))

		pattern.add3dModel(self._model(pin_count, isR))
		pattern.setRecovery(code_int=-1000, generator=True, model=True)
		pattern.setValue(name)
		pattern.setPadSize(1.7, 1.7)
		pattern.setShape(DipTracePadShapes.Oval)
		pattern.setShapeNew(DipTracePadShapesNew.Obround)
		pattern.setHole(width=1.13)
		pattern.addDefaultShapes()
		pattern.setCustomSwell(-1000)
		pattern.setPadMask(50, 0.9, 0.6, 3)
		pattern.setMounting(-1)
		pattern.setCategoryIndex(-1)

		pattern.addTerminal(DipTraceTerminal()
			.setShape(DipTraceTerminalShapes.Rectangle)
			.setSize(0.64, 0.64)
		)

		pattern.move(-(pin_count/2-1)*1.27, 1.27 - 1.5)
		pattern.setOrigin(0, -1.5, common=1)

		return pattern

	def _pin(self, pin_number:int) -> DipTracePin:
		return DipTracePin() \
			.setNumber(pin_number) \
			.setPosition(0.0, int((pin_number-1)/2) * 2.54) \
			.setOrientation(DipTracePinOrientation.Right) \
			.setLength(5.08)

	def _component_pin_shape(self, pin_number:int) -> List[DipTraceComponentShape]:
		y = pin_number * 2.54

		return [
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(0.0, y)
				.addPoint(5.08, y)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(5.08 - 0.9525, y - 0.9525)
				.addPoint(5.08, y)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(5.08 - 0.9525, y + 0.9525)
				.addPoint(5.08, y)
				.setLocked(True)
		]

	def _component_part(self, name:str, pin_count:int, part:int) -> List[DipTraceComponentShape] :
		shapes = []
		for pin in range(int(pin_count / 2)):
			shapes.extend(self._component_pin_shape(pin))

		shapes.extend([
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(2.54-0.3175, 0)
				.addPoint(2.54-0.3175, (pin_count/2-1)*2.54),
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(2.54+0.3175, 0)
				.addPoint(2.54+0.3175, (pin_count/2-1)*2.54),
		])

		return DipTraceComponentPart(name) \
			.setPartName('Part {0}'.format(part+1)) \
			.addPin([self._pin(pin+1) for pin in range(part, pin_count, 2)]) \
			.addShape(shapes)

	def _component(self, name:str, pin_count:int, isR:bool=False) -> DipTraceComponent:
		component = DipTraceComponent(name, 'J')
		for i in range(2): component.addPart(self._component_part(name, pin_count, i))
		return component

	def run(self) -> None:
		for pin_count in self.pins:
			name = f'BH-{pin_count:02}'
			p = self._pattern(name, pin_count)
			c = self._component(name, pin_count).setPattern(p)
			self.patternlibrary.addPattern(p)
			self.componentLibrary.addComponent(c)

		for pin_count in self.pins:
			name = f'BHR-{pin_count:02}'
			p = self._pattern(name, pin_count, True)
			c = self._component(name, pin_count, True).setPattern(p)
			self.patternlibrary.addPattern(p)
			self.componentLibrary.addComponent(c)

		self.patternlibrary.save('{0}.pattern.asc'.format(self.name) )
		self.componentLibrary.save('{0}.component.asc'.format(self.name) )


if __name__ == "__main__":
	IDC_Connectors(
		'IDC Connectors',
		[6, 8, 10, 14, 16, 20, 24, 26, 34, 40, 50, 60, 64]
	).run()
