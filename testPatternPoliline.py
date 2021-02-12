#!/usr/bin/python3
#-*- coding: utf-8 -*-

from DipTraceUnits import units2mm
from DipTracePoint import DipTracePoint
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


def shape8new2old(points_new:List[DipTracePoint]) -> List[DipTracePoint]:
	# find limits
	min_x, max_x, min_y, max_y = 0, 0, 0, 0
	for point in points_new:
		if point.x > max_x: max_x = point.x
		if point.x < min_x: min_x = point.x
		if point.y > max_y: max_y = point.y
		if point.y < min_y: min_y = point.y

	# find size
	width  = max_x - min_x
	height = max_y - min_y
	print(f'Size:   [{width:5.2f}, {height:5.2f}]')

	# find origin
	origin_x = (max_x + min_x) / 2.0
	origin_y = (max_y + min_y) / 2.0
	print(f'Origin: [{origin_x:5.2f}, {origin_y:5.2f}]')

	# find old points
	old_points = []
	for point in points_new:
		old_points.append(DipTracePoint(
			(point.x - origin_x) / width,
			(point.y - origin_y) / height,
			False
		))

	return old_points


def testPatternPolylaine():

	points_new = [
		DipTracePoint(-0.5, -2),
		DipTracePoint(-2.5,  0),
		DipTracePoint(-0.5,  2),
		DipTracePoint( 2.5,  0),
		DipTracePoint(   0, -2),
	]

	points_old = shape8new2old(points_new)

	return str(DipTracePatternShape()
		.type(DipTracePatternShapeType.Poliline)
		.setLineWidth(0.25)
		.setLayer(DipTraceLayerType.TopSilk)
		.setLocked(False)
		.setTextHorizontal(-1)
		.setTextVertical(-1)
		.setTextWidth(1)
		.setFontSize(10)
		.setLineWidth(-2)
		.setVector(False)
		.setTextAngle(math.pi / 2)
		.addPoint(points_old)
		.addPointNew(points_new)
	)

if __name__ == "__main__":
	with  open('shape.2.txt', 'w', encoding='cp1251') as shape_file:
		shape_file.write(testPatternPolylaine())
