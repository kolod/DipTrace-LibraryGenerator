#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from enum import Enum


class DipTraceMarkingType(Enum):
    Text = 0
    Name = 1
    RefDes = 2
    Value = 3


class DipTraceTextRotation(Enum):
    Default = 0
    Rotate_90 = 1
    Rotate_180 = 2
    Rotate_270 = 3


class DipTraceDimentionType(Enum):
    Horizontal = 0
    Vertical = 1
    Free = 2
    Radius = 3
    Point = 4


class DipTraceDimentionUnits(Enum):
    Default = 0
    Inches = 1
    Mils = 2
    Millimeters = 3


class DipTraceDimensionPointerType(Enum):
    Coordinates = 0
    Comment = 1


class DipTraceIpcMounting(Enum):
    Surface = 0
    ThroughtHole = 1


class DipTracePatternType(Enum):
    Free = 0
    Circle = 4
    Lines = 5
    Square = 6
    Matrix = 7
    Rectangle = 8
    ZigZag = 9
    IPC7351 = 10


class DipTracePatternShapeType(Enum):
    Null = 0   # TODO:Rename
    Line = 1
    Rectangle = 2
    Obround = 3
    FilledRectangle = 4
    FilledObround = 5
    Arc = 6
    Text = 7
    Poliline = 8
    Poligon = 9


class DipTraceComponentShapeType(Enum):
    Null = 0   # TODO:Rename
    Line = 1   # +
    Rectangle = 2
    Arrow = 3   # +
    FilledRectangle = 2
    FilledObround = 5
    Arc = 6
    Text = 7
    Poliline = 8   # +
    Poligon = 9


class DipTraceLayerType(Enum):
    TopSilk = 0
    TopAssembly = 1
    TopMask = 2
    TopPaste = 3
    BottomPaste = 4
    BottomMask = 5
    BottomAssembly = 6
    BottomSilk = 7
    Top = 8
    TopKeepout = 9
    BottomKeepout = 10
    Bottom = 11
    BoardCutout = 12
    TopDimension = 13
    BottomDimension = 14
    TopCourtyard = 16
    BottomCourtyard = 17
    TopOutline = 18
    BottomOutline = 19


class DipTraceTextAlign(Enum):
    Left = -1
    Center = 0
    Right = 1


class DipTraceHoleTypes(Enum):
    Round = 0
    Obround = 1


class DipTracePadTypes(Enum):
    ThroughHole = 0
    Surface = 1


class DipTracePadShapes(Enum):
    ''' version 3.3.1.3 and below '''
    Ellipse = 0
    Oval = 1
    Rectangle = 2
    Polygon = 3


class DipTracePadShapesNew(Enum):
    ''' version 4.0 and above '''
    Ellipse = 0
    Obround = 1
    Rectangle = 2
    Polygon = 3
    DShape = 4


class DipTraceTerminalShapes(Enum):
    Null = 0
    Obround = 1
    Rectangle = 2
    Polygon = 3
    DShape = 4


class DipTraceComponentPartType(Enum):
    Normal = 0
    PowerAndGnd = 1
    NetPorts = 2


class DipTracePinType(Enum):
    Undefined = 0
    Dot = 1
    PolarityIn = 2
    PolarityOut = 3
    NonLogic = 4
    Open = 5
    OpenHigh = 6
    OpenLow = 7
    ThreeState = 8
    Hysteresis = 9
    Amplyfier = 10
    Postponed = 11
    Shift = 12
    Clock = 13
    Generator = 14


class DipTracePinElectric(Enum):
    Undefined = 0
    Passive = 1
    Input = 2
    Output = 3
    Bidirectional = 4
    OpenHigh = 6
    OpenLow = 7
    PassiveHigh = 6
    PassiveLow = 7
    ThreeState = 8
    Power = 9


class DipTracePinOrientation(Enum):
    Right = 0
    Top = 1
    Left = 2
    Bottom = 3


class DipTrace3dModelType(Enum):
    File = 0
    Generator = 1
    Outline = 2


class DipTrace3dModelUnits(Enum):
    Wings3D = -1
    Meters = 0
    Mils = 1
    Inches = 2


if __name__ == "__main__":
    pass
