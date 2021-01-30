#!/usr/bin/python3
#-*- coding: utf-8 -*-

import math
from typing import Pattern

from DipTraceEnums import *
from DipTracePatternShape import *
from DipTracePatternLibrary import *
from DipTraceComponentShape import *
from DipTraceComponentLibrary import *

def shape_5mm():

	r = 2.95
	x = 2.6
	y = math.sqrt(math.pow(r, 2) - math.pow(x, 2))

	return [
		DipTracePatternShape(DipTracePatternShapeType.Arc)
			.setLayer(DipTraceLayer.TopSilk)
			.addPoint(-x, y)
			.addPoint(0.0, r)
			.addPoint(-x, -y)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Line)
			.setLayer(DipTraceLayer.TopSilk)
			.addPoint(-x, y)
			.addPoint(-x, -y)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Arc)
			.setLayer(DipTraceLayer.TopCourtyard)
			.addPoint(-x, y)
			.addPoint(0.0, r)
			.addPoint(-x, -y)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Line)
			.setLayer(DipTraceLayer.TopCourtyard)
			.addPoint(-x, y)
			.addPoint(-x, -y)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Arc)
			.setLayer(DipTraceLayer.TopAssembly)
			.addPoint(-x, y)
			.addPoint(0.0, r)
			.addPoint(-x, -y)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Line)
			.setLayer(DipTraceLayer.TopAssembly)
			.addPoint(-x, y)
			.addPoint(-x, -y)
			.setLocked(True)
	]

def shape_3mm():

	r = 1.5
	x1 = r * math.cos(math.radians(45))
	y1 = r * math.sin(math.radians(45))
	x2 = r * math.cos(math.radians(45))
	y2 = r * math.sin(math.radians(45))

	r3 = 3.85 / 2
	x3 = 1.6
	y3 = math.sqrt(math.pow(r3, 2) - math.pow(x3, 2))

	return [
		DipTracePatternShape(DipTracePatternShapeType.Arc)
			.setLayer(DipTraceLayer.TopSilk)
			.addPoint(-x1,y1)
			.addPoint(0.0,r)
			.addPoint(x2,y2)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Arc)
			.setLayer(DipTraceLayer.TopSilk)
			.addPoint(-x1,-y1)
			.addPoint(0,-r)
			.addPoint(x2,-y2)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Arc)
			.setLayer(DipTraceLayer.TopCourtyard)
			.addPoint(-x3, y3)
			.addPoint(0.0, r3)
			.addPoint(-x3, -y3)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Line)
			.setLayer(DipTraceLayer.TopCourtyard)
			.addPoint(-x3, y3)
			.addPoint(-x3, -y3)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Arc)
			.setLayer(DipTraceLayer.TopAssembly)
			.addPoint(-x3, y3)
			.addPoint(0.0, r3)
			.addPoint(-x3, -y3)
			.setLocked(True),
		DipTracePatternShape(DipTracePatternShapeType.Line)
			.setLayer(DipTraceLayer.TopAssembly)
			.addPoint(-x3, y3)
			.addPoint(-x3, -y3)
			.setLocked(True)
	]

def pad():
	return [
		DipTracePad(1, -1.27, 0.0)
			.setLocked(True)
			.setStandart(False)
			.setPadMask(50.0, 0.9, 0.6, 3)
			.setHole(DipTraceHoleTypes.Round, 0.9)
			.setSize(1.5, 1.5)
			.setShape(DipTracePadShapes.Rectangle)
			.addTerminal(DipTraceTerminal()
				.setShape(DipTraceTerminalShapes.Rectangle)
				.setSize(0.45, 0.45)),
		DipTracePad(2,  1.27, 0.0)
			.setLocked(True)
			.setStandart(False)
			.setPadMask(50.0, 0.9, 0.6, 3)
			.setHole(DipTraceHoleTypes.Round, 0.9)
			.setSize(1.5, 1.5)
			.setShape(DipTracePadShapes.Obround)
			.addTerminal(DipTraceTerminal()
				.setShape(DipTraceTerminalShapes.Rectangle)
				.setSize(0.45, 0.45)),
	]


def pattern_3mm(color:str):
	name = 'LED-3mm-{0}'.format(color)
	model = name + '.step'

	return DipTracePattern(name, 'D') \
		.addShape(shape_3mm()) \
		.addPad(pad()) \
		.add3dModel(DipTrace3dModel(model).setRotation(90.0))


def pattern_5mm(color:str):
	name = 'LED-5mm-{0}'.format(color)
	model = name + '.step'

	return DipTracePattern(name, 'D') \
		.addShape(shape_5mm()) \
		.addPad(pad()) \
		.add3dModel(DipTrace3dModel(model).setRotation(90.0))


def pin():
	return [
		DipTracePin(1)
			.setOrientation(DipTracePinOrientation.Left)
			.setPosition(2.54, 0.0)
			.setLength(2.54),
		DipTracePin(2)
			.setOrientation(DipTracePinOrientation.Right)
			.setPosition(-2.54, 0.0)
			.setLength(2.54)
	]

def pin_shape() -> list:
		x = 1.27 * math.sin(math.radians(60.0))

		return [
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(-2.54, 0.0)
				.addPoint( 2.54, 0.0)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Poliline)
				.addPoint(-x,  1.27)
				.addPoint( x, 0.0)
				.addPoint(-x, -1.27)
				.addPoint(-x,  1.27)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Line)
				.addPoint(x,  1.27)
				.addPoint(x, -1.27)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Arrow)
				.addPoint(0.343, -1.613)
				.addPoint(1.587, -3.492)
				.setLocked(True),
			DipTraceComponentShape(DipTraceComponentShapeType.Arrow)
				.addPoint(-0.61, -2.248)
				.addPoint(0.635, -4.127)
				.setLocked(True)
		]


def component(color:str):
	name = 'LED-3mm-{0}'.format(color)
	return DipTraceComponent(name, 'D').addPart(DipTraceComponentPart('Part 1').addShape(pin_shape()).addPin(pin()))


def run(colors):
	patternLib = DipTracePatternLibrary('LEDs')
	componentLib = DipTraceComponentLibrary('LEDs')

	for color in colors:
		p = pattern_3mm(color)
		c = component(color).setPattern(p)
		patternLib.addPattern(p)
		componentLib.addComponent(c)

	for color in colors:
		p = pattern_5mm(color)
		c = component(color).setPattern(p)
		patternLib.addPattern(p)
		componentLib.addComponent(c)

	patternLib.save('LEDs.pattern.asc')
	componentLib.save('LEDs.component.asc')

if __name__ == "__main__":
	run([
		'green',
		'red',
		'orange',
		'clear'
	])