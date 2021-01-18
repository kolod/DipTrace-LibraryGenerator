#!/usr/bin/python3
#-*- coding: utf-8 -*-

import math
from copy import deepcopy
from DipTraceEnums import *
from DipTracePatternShape import *
from DipTracePatternLibrary import *
from DipTraceComponentShape import *
from DipTraceComponentLibrary import *


class IDC_Connectors:

	def __init__(self, name, pins):
		self.pins             = pins
		self.name             = name
		self.patternlibrary   = DipTracePatternLibrary(name)
		self.componentLibrary = DipTraceComponentLibrary(name)

	def terminal(self):
		return DipTraceTerminal() \
		.setShape(DipTraceTerminalShapes.Rectangle) \
		.setSize(0.64, 0.64)

	def model(self, pins, isR=False):
		return DipTrace3dModel('BH{1}-{0:02}.STEP'.format(pins, 'R' if isR else '')) \
			.setRotation(90.0)

	def pattern_shape(self, pins):
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
			deepcopy(shape_01).setLineWidth(0.25).setLayer(DipTraceLayer.TopSilk),
			deepcopy(shape_02).setLineWidth(0.25).setLayer(DipTraceLayer.TopSilk),
			deepcopy(shape_04).setLineWidth(0.25).setLayer(DipTraceLayer.TopSilk),
			deepcopy(shape_01).setLineWidth(0.12).setLayer(DipTraceLayer.TopAssembly),
			deepcopy(shape_02).setLineWidth(0.12).setLayer(DipTraceLayer.TopAssembly),
			deepcopy(shape_01).setLineWidth(0.05).setLayer(DipTraceLayer.TopCourtyard)
		]

	def pattern_shape_r(self, pins):
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
			deepcopy(shape_01).setLineWidth(0.25).setLayer(DipTraceLayer.TopSilk),
			deepcopy(shape_02).setLineWidth(0.25).setLayer(DipTraceLayer.TopSilk),
			deepcopy(shape_01).setLineWidth(0.12).setLayer(DipTraceLayer.TopAssembly),
			deepcopy(shape_02).setLineWidth(0.12).setLayer(DipTraceLayer.TopAssembly),
			deepcopy(shape_01).setLineWidth(0.05).setLayer(DipTraceLayer.TopCourtyard)
		]

	def pad(self, number):
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
		pad.addTerminal(self.terminal())
		return pad

	def pattern(self, pin_count, isR=False):
		C = 2.54 * int(pin_count/2 - 1)
		A = C + 10.14

		pattern = DipTracePattern('BH{1}-{0:02}'.format(pin_count, 'R' if isR else ''), 'J')
		pattern.setSize(A, 8.4)

		for pin in range(pin_count):
			pattern.addPad(self.pad(pin))

		if isR:
			pattern.addShape(self.pattern_shape_r(pin_count))
		else:
			pattern.addShape(self.pattern_shape(pin_count))

		pattern.add3dModel(self.model(pin_count, isR))

		pattern.move(-(pin_count/2-1)*1.27, 1.27)

		return pattern

	def pin(self, pin_number):
		pin = DipTracePin(pin_number)
		pin.setPosition(0.0, int((pin_number-1)/2) * 2.54)
		pin.setOrientation(DipTracePinOrientation.Right)
		pin.setLength(5.08)
		return pin

	def component_pin_shape(self, pin_number):
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

	def component_part(self, pin_count, number):
		part = DipTraceComponentPart('Part {0}'.format(number))

		for pin in range(number, pin_count, 2):
			part.addPin(self.pin(pin+1))

		for pin in range(int(pin_count / 2)):
			part.addShape(self.component_pin_shape(pin))

		part.addShape([
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(2.54-0.3175, 0)
				.addPoint(2.54-0.3175, (pin_count/2-1)*2.54),
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(2.54+0.3175, 0)
				.addPoint(2.54+0.3175, (pin_count/2-1)*2.54),
		])

		return part

	def component(self, pin_count, isR=False):
		component = DipTraceComponent('BH{1}-{0:02}'.format(pin_count, 'R' if isR else ''), 'J')
		for i in range(2): component.addPart(self.component_part(pin_count, i))
		return component

	def run(self):
		for pin_count in self.pins:
			p = self.pattern(pin_count)
			c = self.component(pin_count).setPattern(p)
			self.patternlibrary.addPattern(p)
			self.componentLibrary.addComponent(c)

		for pin_count in self.pins:
			p = self.pattern(pin_count, True)
			c = self.component(pin_count, True).setPattern(p)
			self.patternlibrary.addPattern(p)
			self.componentLibrary.addComponent(c)

		self.patternlibrary.save('{0}.pattern.asc'.format(self.name) )
		self.componentLibrary.save('{0}.component.asc'.format(self.name) )


if __name__ == "__main__":
	IDC_Connectors(
		'IDC Connectors',
		[6, 8, 10, 14, 16, 20, 24, 26, 34, 40, 50, 60, 64]
	).run()
