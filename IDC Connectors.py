#!/usr/bin/python3
#-*- coding: utf-8 -*-

import math
from copy import deepcopy
from typing import List
from DipTracePin import DipTracePin
from DipTracePad import DipTracePad
from DipTraceEnums import DipTraceHoleTypes, DipTraceLayerType, DipTraceTerminalShapes, DipTracePadShapes, DipTracePatternShapeType, DipTraceComponentShapeType
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
		self.componentLibrary = DipTraceComponentLibrary(name)
		super().__init__()

	def _terminal(self) -> DipTraceTerminal:
		return DipTraceTerminal().setShape(DipTraceTerminalShapes.Rectangle).setSize(0.64, 0.64)

	def _model(self, pins:int, isR:bool=False) -> DipTrace3dModel:
		return DipTrace3dModel('BH{1}-{0:02}.STEP'.format(pins, 'R' if isR else '')).setRotation(90.0)

	def _pattern_shape(self, pins:int) -> List[DipTracePatternShape]:
		C      = 2.54 * int(pins/2 - 1)
		A      = C + 10.14
		bottom = (8.4 - 2.54) / 2
		top    = bottom - 8.4
		left   = (C-A)/2
		right  = (C+A)/2
		middle = C/2
		triag  = 2 / math.sqrt(3)

		shape_01 = DipTracePatternShape(DipTracePatternShapeType.Rectangle) \
			.addPoint(right, top) \
			.addPoint(left, bottom)

		shape_02 = DipTracePatternShape(DipTracePatternShapeType.Poliline) \
			.addPoint(middle - 2.5, bottom      ) \
			.addPoint(middle - 2.5, bottom - 0.5) \
			.addPoint(left   + 0.5, bottom - 0.5) \
			.addPoint(left   + 0.5, top    + 0.5) \
			.addPoint(right  - 0.5, top    + 0.5) \
			.addPoint(right  - 0.5, bottom - 0.5) \
			.addPoint(middle + 2.5, bottom - 0.5) \
			.addPoint(middle + 2.5, bottom      )

		shape_04 = DipTracePatternShape(DipTracePatternShapeType.Poligon) \
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
		triag    = 2 / math.sqrt(3)

		shape_01 = DipTracePatternShape(DipTracePatternShapeType.Rectangle) \
			.addPoint(right, top) \
			.addPoint(left, bottom)

		shape_02 = DipTracePatternShape(DipTracePatternShapeType.Poliline) \
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
		row    = int(number % 2)
		column = int(number / 2)
		x      = column *  2.54
		y      = row    * -2.54
		pad    = DipTracePad(number+1, x, y)
		pad.setLocked(True)
		pad.setSize(1.7, 1.7)
		pad.setPadMask(50.0, 0.9, 0.6, 3)
		pad.setHole(DipTraceHoleTypes.Round, 1.13)
		pad.setStandart(number != 0)
		pad.setShape(DipTracePadShapes.Rectangle if number == 0 else DipTracePadShapes.Obround)
		pad.addTerminal(self._terminal())
		return pad

	def _pattern(self, pin_count:int, isR:bool=False) -> DipTracePattern:
		C = 2.54 * int(pin_count/2 - 1)
		A = C + 10.14

		pattern = DipTracePattern('BH{1}-{0:02}'.format(pin_count, 'R' if isR else ''), 'J')
		pattern.setSize(A, 8.4)

		for pin in range(pin_count):
			pattern.addPad(self._pad(pin))

		if isR:
			pattern.addShape(self._pattern_shape_r(pin_count))
		else:
			pattern.addShape(self._pattern_shape(pin_count))

		pattern.add3dModel(self._model(pin_count, isR))

		pattern.move(-(pin_count/2-1)*1.27, 1.27)

		return pattern

	def _pin(self, pin_number:int) -> DipTracePin:
		pin = DipTracePin(pin_number)
		pin.setPosition(0.0, int((pin_number-1)/2) * 2.54)
		pin.setOrientation(DipTraceIndentation.Right)
		pin.setLength(5.08)
		return pin

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

	def _component_part(self, pin_count:int, number:int) -> List[DipTraceComponentShape] :
		part = DipTraceComponentPart('Part {0}'.format(number))

		for pin in range(number, pin_count, 2):
			part.addPin(self._pin(pin+1))

		for pin in range(int(pin_count / 2)):
			part.addShape(self._component_pin_shape(pin))

		part.addShape([
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(2.54-0.3175, 0)
				.addPoint(2.54-0.3175, (pin_count/2-1)*2.54),
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(2.54+0.3175, 0)
				.addPoint(2.54+0.3175, (pin_count/2-1)*2.54),
		])

		return part

	def _component(self, pin_count:int, isR:bool=False) -> DipTraceComponent:
		component = DipTraceComponent('BH{1}-{0:02}'.format(pin_count, 'R' if isR else ''), 'J')
		for i in range(2): component.addPart(self._component_part(pin_count, i))
		return component

	def run(self) -> None:
		for pin_count in self.pins:
			p = self._pattern(pin_count)
			c = self._component(pin_count).setPattern(p)
			self.patternlibrary.addPattern(p)
			self.componentLibrary.addComponent(c)

		for pin_count in self.pins:
			p = self._pattern(pin_count, True)
			c = self._component(pin_count, True).setPattern(p)
			self.patternlibrary.addPattern(p)
			self.componentLibrary.addComponent(c)

		self.patternlibrary.save('{0}.pattern.asc'.format(self.name) )
		self.componentLibrary.save('{0}.component.asc'.format(self.name) )


if __name__ == "__main__":
	IDC_Connectors(
		'IDC Connectors',
		[6, 8, 10, 14, 16, 20, 24, 26, 34, 40, 50, 60, 64]
	).run()
