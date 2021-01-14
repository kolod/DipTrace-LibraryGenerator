#!/usr/bin/python3
#-*- coding: utf-8 -*-

import math
from copy import deepcopy
from DipTracePatternLibrary import *
from DipTraceComponentLibrary import *


class IDC_Connectors:

	def __init__(self, name, pins):
		self.pins = pins
		self.name = name

	def save(self, filename):
		self.library.save(filename)


class IDC_Connectors_Pattern(IDC_Connectors):

	def __init__(self, name, pins):
		self.library = DipTracePatternLibrary(name)
		super().__init__(name, pins)

	def terminal(self):
		return DipTraceTerminal() \
		.setShape(DipTraceTerminalShapes.Rectangle) \
		.setSize(0.64, 0.64)

	def model(self, pins):
		return DipTrace3dModel('BH-{0:02}.STEP'.format(pins)) \
			.setRotation(90.0)

	def shape(self, pins):
		C      = 2.54 * int(pins/2 - 1)
		A      = C + 10.14
		bottom = (8.4 - 2.54) / 2
		top    = bottom - 8.4
		left   = (C-A)/2
		right  = (C+A)/2
		middle = C/2
		triag  = 2 / math.sqrt(3)

		shape_01 = DipTraceShape(DipTraceShapeType.Rectangle) \
			.addPoint(right, top) \
			.addPoint(left, bottom)

		shape_02 = DipTraceShape(DipTraceShapeType.Poliline) \
			.addPoint(middle - 2.5, bottom      ) \
			.addPoint(middle - 2.5, bottom - 0.5) \
			.addPoint(left   + 0.5, bottom - 0.5) \
			.addPoint(left   + 0.5, top    + 0.5) \
			.addPoint(right  - 0.5, top    + 0.5) \
			.addPoint(right  - 0.5, bottom - 0.5) \
			.addPoint(middle + 2.5, bottom - 0.5) \
			.addPoint(middle + 2.5, bottom      )

		shape_03 = DipTraceShape(DipTraceShapeType.Line) \
			.addPoint(left , bottom - 2.0) \
			.addPoint(left + 2.0 , bottom)

		shape_04 = DipTraceShape(DipTraceShapeType.Poligon) \
			.addPoint(0.0         , bottom + 1.0) \
			.addPoint(triag       , bottom + 3.0) \
			.addPoint(-triag      , bottom + 3.0)

		return [
			deepcopy(shape_01).setLineWidth(0.25).setLayer(DipTraceLayer.TopSilk),
			deepcopy(shape_02).setLineWidth(0.25).setLayer(DipTraceLayer.TopSilk),
			deepcopy(shape_04).setLineWidth(0.25).setLayer(DipTraceLayer.TopSilk),
			deepcopy(shape_01).setLineWidth(0.12).setLayer(DipTraceLayer.TopAssembly),
			deepcopy(shape_03).setLineWidth(0.12).setLayer(DipTraceLayer.TopAssembly),
			deepcopy(shape_01).setLineWidth(0.05).setLayer(DipTraceLayer.TopCourtyard)
		]

	def pad(self, number):
		row    = int(number % 2)
		column = int(number / 2)
		x      = column *  2.54
		y      = row    * -2.54
		pad    = DipTracePad(number+1, x, y)
		pad.setSize(1.7, 1.7)
		pad.setHole(DipTraceHoleTypes.Round, 1.13)
		pad.setStandart(number != 0)
		pad.setShape(DipTracePadShapes.Rectangle if number == 0 else DipTracePadShapes.Obround)
		pad.addTerminal(self.terminal())
		return pad

	def pattern(self, pin_count):
		C = 2.54 * int(pin_count/2 - 1)
		A = C + 10.14

		pattern = DipTracePattern('BH-{}'.format(pin_count), 'J')
		pattern.setSize(A, 8.4)

		for pin in range(pin_count):
			pattern.addPad(self.pad(pin))

		pattern.addShape(self.shape(pin_count))
		pattern.add3dModel(self.model(pin_count))

		return pattern

	def save(self, filename):
		self.library.save(filename)

	def run(self, filename):
		for pin_count in self.pins:
			self.library.addPattern(self.pattern(pin_count))

		self.save(filename)


class IDC_Connectors_Component(IDC_Connectors):

	def __init__(self, name, pins):
		self.library = DipTraceComponentLibrary(name)
		super().__init__(name, pins)

	def pin(self, pin_number):
		pin = DipTracePin(pin_number)
		return pin

	def part(self, pin_count, number):
		part = DipTraceComponentPart('Part {0}'.format(number), 'J')

		for pin in range(number, pin_count, 2):
			part.addPin(self.pin(pin))

		return part

	def component(self, pin_count):
		component = DipTraceComponent('BH-{0}'.format(pin_count))
		for i in range(2): component.addPart(self.part(pin_count, i))
		return component

	def run(self, filename):
		for pin_count in self.pins:
			self.library.addComponent(self.component(pin_count))

		self.save(filename)


if __name__ == "__main__":
	IDC_Connectors_Pattern('IDC Connectors', [6, 8, 10, 14, 16, 20, 24, 26, 34, 40, 50, 60, 64]).run('IDC Connectors Pattern.asc')
	IDC_Connectors_Component('IDC Connectors', [6, 8, 10, 14, 16, 20, 24, 26, 34, 40, 50, 60, 64]).run('IDC Connectors Component.asc')
