#!/usr/bin/python3
#-*- coding: utf-8 -*-

from enum import Enum

class DipTraceShapeType(Enum):
	Null             = 0   # TODO:
	Line             = 1
	Rectangle        = 2
	Obround          = 3
	FilledRectangle  = 2
	FilledObround    = 5
	Arc              = 6
	Text             = 7
	Poliline         = 8
	Poligon          = 9

class DipTraceLayer(Enum):
	TopSilk          = 0
	TopAssembly      = 1
	TopMask          = 2
	TopPaste         = 3
	BottomPaste      = 4
	BottomMask       = 5
	BottomAssembly   = 6
	BottomSilk       = 7
	Top              = 8
	TopKeepout       = 9
	BottomKeepout    = 10
	Bottom           = 11
	BoardCutout      = 12
	TopCourtyard     = 16
	BottomCourtyard  = 17
	TopOutline       = 18
	BottomOutline    = 19

class DipTraceTextAlign(Enum):
	Left             = -1
	Center           = 0
	Right            = 1

class DipTraceHoleTypes(Enum):
	Round     = 0
	Obround   = 1

class DipTracePadTypes(Enum):
	ThroughHole = 0
	Surface     = 1

class DipTracePadShapes(Enum):
	Ellipse   = 0
	Obround   = 1
	Rectangle = 2
	Polygon   = 3
	DShape    = 4

class DipTraceTerminalShapes(Enum):
	Null      = 0
	Obround   = 1
	Rectangle = 2
	Polygon   = 3
	DShape    = 4

class DipTraceComponentPartType(Enum):
	Normal      = 0
	PowerAndGnd = 1
	NetPorts    = 2

class DipTracePinType(Enum):
	Undefined    =  0
	Dot          =  1
	PolarityIn   =  2
	PolarityOut  =  3
	NonLogic     =  4
	Open         =  5
	OpenHigh     =  6
	OpenLow      =  7
	ThreeState   =  8
	Hysteresis   =  9
	Amplyfier    = 10
	Postponed    = 11
	Shift        = 12
	Clock        = 13
	Generator    = 14

class DipTracePinElectric(Enum):
	Undefined     = 0
	Passive       = 1
	Input         = 2
	Output        = 3
	Bidirectional = 4
	OpenHigh      = 6
	OpenLow       = 7
	PassiveHigh   = 6
	PassiveLow    = 7
	ThreeState    = 8
	Power         = 9

class DipTracePinOrientation(Enum):
	Right   = 0
	Top     = 1
	Left    = 2
	Bottom  = 3

if __name__ == "__main__":
	pass