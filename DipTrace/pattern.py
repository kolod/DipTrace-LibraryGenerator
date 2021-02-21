#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import re
from io import TextIOWrapper
from typing import Literal, AnyStr, List, Union
from pyfields import field, init_fields
from DipTrace.math import getArcSize
from DipTrace.reHelper import reBracketed, searchSingleBool, searchSingleString, searchSingleInt, searchSingleFloat,\
    searchDoubleFloat, searchSingleIntlList, searchSingleBoolList, searchSingleFloatList, reJoin, reString, reBool, reInt
from DipTrace.pad import DipTracePad
from DipTrace.bool import DipTraceBool
from DipTrace.hole import DipTraceHole
from DipTrace.units import mm2units, units2mm
from DipTrace.point import DipTracePoint
from DipTrace.enums import DipTracePatternType, DipTraceHoleTypes, DipTracePadShapes, DipTracePadShapesNew, DipTracePatternShapeType
from DipTrace.model import DipTrace3dModel
from DipTrace.terminal import DipTraceTerminal
from DipTrace.dimension import DipTraceDimension
from DipTrace.patternShape import DipTracePatternShape
from DipTrace.patternLayer import DipTracePatternLayer
from DipTrace.categoryType import DipTraceCategoryType


class DipTracePattern:

    isComponent: bool = False

    pads: List[DipTracePad] = field(default=[], doc='')
    shapes: List[DipTracePatternShape] = field(default=[], doc='')
    points: List[DipTracePoint] = field(default=[], doc='')
    points_new: List[DipTracePoint] = field(default=[], doc='')
    holes: List[DipTraceHole] = field(default=[], doc='')
    layers: List[DipTracePatternLayer] = field(default=[], doc='')
    terminals: List[DipTraceTerminal] = field(default=[], doc='')
    names: List[str] = field(default=[], doc='')
    user_fields: List[Union[str, int]] = field(default=[], doc='')
    categories: List[DipTraceCategoryType] = field(default=[], doc='')
    dimensions: List[DipTraceDimension] = field(default=[], doc='')
    model: DipTrace3dModel = field(default=DipTrace3dModel(), doc='')
    variableParameters: List[str] = field(default=['N', 'N', 'N', 'N', 'N'])
    verifications: List[str] = field(default=['N', 'N', 'N', 'N'])
    type: DipTracePatternType = field(default=DipTracePatternType.Free, doc='')
    name: str = field(default='', doc='Pattern name')
    unique_name: str = field(default='', doc='Pattern unique name')
    ref: str = field(default='', doc='Pattern ref')
    description: str = field(default='', doc='Pattern description')
    value: str = field(default='', doc='Value')
    manufacturer: str = field(default='', doc='Chip manufacturer')
    datasheet: str = field(default='', doc='Chip datasheet')
    category_name: str = field(default='', doc='')
    category_index: int = field(default=0, doc='')
    locked: DipTraceBool = field(default=DipTraceBool(False), doc='Locking shape')
    surface: DipTraceBool = field(default=DipTraceBool(False), doc='Surface mount')
    mounting: int = field(default=0, doc='')
    width: float = field(default=0.0, doc='Pattern width')
    height: float = field(default=0.0, doc='Pattern height')
    # TODO: Check is float or not
    orientation: float = field(default=0.0, doc='')
    spacings: List[float] = field(default=[0.0, 0.0, 0.0], doc='')
    numbers: List[float] = field(default=[0.0, 0.0], doc='')
    origin_x: float = field(default=0.0, doc='')
    origin_y: float = field(default=0.0, doc='')
    origin_common: float = field(default=0.0, doc='')
    origin_courtyard: float = field(default=0.0, doc='')
    origin_cross: DipTraceBool = field(default=DipTraceBool(False), doc='')
    origin_circle: DipTraceBool = field(default=DipTraceBool(False), doc='')
    recovery_code_int: int = field(default=0, doc='')
    recovery_code: str = field(default='', doc='')
    recovery_generator: DipTraceBool = field(default=DipTraceBool(False), doc='')
    recovery_model: DipTraceBool = field(default=DipTraceBool(False), doc='')
    hole_type: DipTraceHoleTypes = field(default=DipTraceHoleTypes.Round, doc='')
    hole_width: float = field(default=0.0, doc='')
    hole_height: float = field(default=0.0, doc='')
    custom_swell: float = field(default=0.0, doc='')
    custom_shrink: float = field(default=0.0, doc='')
    top_mask_state: int = field(default=0, doc='')
    bottom_mask_state: int = field(default=0, doc='')
    top_paste_state: int = field(default=0, doc='')
    bottom_paste_state: int = field(default=0, doc='')
    pad_shape: DipTracePadShapes = field(default=DipTracePadShapes.Oval, doc='Default pad shape')
    pad_shape_new: DipTracePadShapesNew = field(default=DipTracePadShapesNew.Ellipse, doc='Default pad shape (for version 4.0 and above)')
    pad_width: float = field(default=0.0, doc='')
    pad_height: float = field(default=0.0, doc='')
    pad_width_new: float = field(default=0.0, doc='')
    pad_height_new: float = field(default=0.0, doc='')
    # TODO: Check is float or not
    pad_angle: float = field(default=0.0, doc='')
    pad_corner: float = field(default=0.0, doc='')
    pad_shape_x: float = field(default=0.0, doc='')
    pad_shape_y: float = field(default=0.0, doc='')
    mask_percent: float = field(default=0.0, doc='')
    mask_edge_gap: float = field(default=0.0, doc='')
    mask_segment_gap: float = field(default=0.0, doc='')
    mask_segment_side: float = field(default=0, doc='')

    @origin_cross.converter(accepts=bool)
    @origin_circle.converter(accepts=bool)
    @surface.converter(accepts=bool)
    @locked.converter(accepts=bool)
    @surface.converter(accepts=bool)
    @recovery_generator.converter(accepts=bool)
    @recovery_model.converter(accepts=bool)
    def toDipTraceBool(self, field, value):
        return DipTraceBool(value)

    @init_fields
    def __init__(self, match: re.Match[AnyStr] = None):
        if match:
            self.name = match.group(1)
            self.ref = match.group(2)
        super().__init__()

    def setNumbers(self, numbers: List[int] = [0, 0]):
        self.numbers = numbers
        return self

    def normalize(self):

        # Find limits
        min_x: float = 0.0
        min_y: float = 0.0
        max_x: float = 0.0
        max_y: float = 0.0

        for pad in self.pads:

            # Calculate pad shape points for older versions
            pad.calculateOld()

            if pad.x - pad.width / 2 < min_x:
                min_x = pad.x - pad.width / 2
            if pad.x + pad.width / 2 > max_x:
                max_x = pad.x + pad.width / 2
            if pad.y - pad.height / 2 < min_y:
                min_y = pad.y - pad.height / 2
            if pad.y + pad.height / 2 > max_y:
                max_y = pad.y + pad.height / 2

        for shape in self.shapes:

            if shape.shape == DipTracePatternShapeType.Arc:

                shape_max_x, shape_min_x, shape_max_y, shape_min_y = getArcSize(shape.points_new)

                if shape_max_x > max_x:
                    max_x = shape_max_x
                if shape_min_x < min_x:
                    min_x = shape_min_x
                if shape_max_y > max_y:
                    max_y = shape_max_y
                if shape_min_y < min_y:
                    min_y = shape_min_y

            else:
                for point in shape.points_new:
                    if point.x < min_x:
                        min_x = point.x
                    if point.x > max_x:
                        max_x = point.x
                    if point.y < min_y:
                        min_y = point.y
                    if point.y > max_y:
                        max_y = point.y

        # Find pattern size
        self.width = max_x - min_x
        self.height = max_y - min_y

        # find pattern origin position
        self.origin_x = -(max_x + min_x) / 2.0
        self.origin_y = -(max_y + min_y) / 2.0
        self.model.origin_x = self.origin_x
        self.model.origin_y = self.origin_y

        for pad in self.pads:
            pad.x, pad.y = pad.x + self.origin_x, pad.y + self.origin_y
            pass

        # Recalculate old points
        for shape in self.shapes:
            if len(shape.points_new) > 0:
                shape.recalculate(self.origin_x, self.origin_y, self.width, self.height)

        return self

    def move(self, x: float = 0.0, y: float = 0.0):
        for pad in self.pads:
            pad.move(x, y)
        for shape in self.shapes:
            shape.move(x, y)
        return self

    @staticmethod
    def pattern() -> Literal:
        return reJoin(r'\(Pattern', reString, reString)

    def load(self, datafile: TextIOWrapper):
        while line := datafile.readline().strip():

            if line == ')':
                break

            elif line == '(Pattern_Groups':
                while line := datafile.readline().strip():
                    if line == ')':
                        break

            elif line == '(UserFields':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if tmp := re.search(reBracketed(reJoin(r'UserField', reString, reString, reInt)), line):
                        name = tmp.group(1)
                        value = tmp.group(2)
                        isLink = int(tmp.group(3))
                        self.user_fields.append([name, value, isLink])

            elif line == '(PadPoints_New':
                while line := datafile.readline().strip():
                    if line == ')':
                        break

            elif line == '(Dimensions':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if line == '(Dimension':
                        self.addDimension(DipTraceDimension().load(datafile))

            elif line.startswith('(CategoryTypes'):
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if tmp := re.search(DipTraceCategoryType.pattern(), line):
                        self.categories.append(DipTraceCategoryType(match=tmp))

            elif line.startswith('(PossibleNames '):  # unused
                while line := datafile.readline().strip():
                    if line == ')':
                        break

            elif line.startswith('(PadTerminalCount'):
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if line == '(PadTerminal':
                        self.terminals.append(
                            DipTraceTerminal().load(datafile))

            elif line == '(Model3D':
                self.model = DipTrace3dModel().load(datafile)

            elif line == '(Holes':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if tmp := re.search(DipTraceHole.pattern(), line):
                        self.holes.append(DipTraceHole(match=tmp))

            elif line == '(Shapes':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if tmp := re.search(DipTracePatternShape.pattern(), line):
                        self.shapes.append(DipTracePatternShape(
                            match=tmp).load(datafile))

            elif line == '(PadPoints':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if tmp := searchDoubleFloat(r'pt', line):
                        x = units2mm(float(tmp.group(1)))
                        y = units2mm(float(tmp.group(2)))
                        self.points.append(DipTracePoint(x=x, y=y))

            elif line == '(Layers':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    if line == '(Layer':
                        self.layers.append(
                            DipTracePatternLayer().load(datafile))

            elif line == '(Pads':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    elif tmp := re.search(DipTracePad.pattern(), line):
                        self.pads.append(DipTracePad(match=tmp).load(datafile))

            elif tmp := searchSingleString(r'Value', line):
                self.value = tmp.group(1)

            elif tmp := searchSingleBoolList(r'VariableParameter', line):
                if tmp.group(2):
                    id = int(tmp.group(1)) - 1
                    self.variableParameters[id] = tmp.group(2)

            elif tmp := searchSingleFloatList(r'Spacing', line):
                if tmp.group(2):
                    id = int(tmp.group(1)) - 1
                    self.spacings[id] = float(tmp.group(2))

            elif tmp := searchSingleIntlList(r'Number', line):
                if tmp.group(2):
                    id = int(tmp.group(1)) - 1
                    self.numbers[id] = tmp.group(2)

            elif tmp := searchSingleFloat(r'Width', line):
                self.width = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'Height', line):
                self.height = float(tmp.group(1))

            elif tmp := searchSingleInt(r'Type', line):
                self.type = DipTracePatternType(int(tmp.group(1)))

            elif tmp := searchSingleFloat(r'OriginX', line):
                self.origin_x = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'OriginY', line):
                self.origin_y = float(tmp.group(1))

            elif tmp := searchSingleBool(r'OriginCross', line):
                self.origin_cross = tmp.group(1)

            elif tmp := searchSingleBool(r'OriginCircle', line):
                self.origin_circle = tmp.group(1)

            elif tmp := searchSingleFloat(r'OriginCommon', line):
                self.origin_common = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'OriginCourtyard', line):
                self.origin_courtyard = float(tmp.group(1))

            elif tmp := searchSingleString(r'Name_Description', line):
                self.description = tmp.group(1)

            elif tmp := searchSingleString(r'Name_Unique', line):
                self.unique_name = tmp.group(1)

            elif tmp := searchSingleInt(r'RecoveryCode', line):
                self.recovery_code_int = int(tmp.group(1))

            elif tmp := searchSingleString(r'RecoveryCode', line):
                self.recovery_code = tmp.group(1)

            elif tmp := searchSingleBool(r'RecoveryCode_Generator', line):
                self.recovery_generator = tmp.group(1)

            elif tmp := searchSingleBool(r'RecoveryCode_Model', line):
                self.recovery_model = tmp.group(1)

            elif tmp := searchSingleString(r'Manufacturer', line):
                self.manufacturer = tmp.group(1)

            elif tmp := searchSingleString(r'Datasheet', line):
                self.datasheet = tmp.group(1)

            elif tmp := searchSingleBool(r'LockProperties', line):
                self.locked = tmp.group(1)

            elif tmp := searchSingleBool(r'SurfacePad', line):
                self.surface = tmp.group(1)

            elif tmp := searchSingleInt(r'Mounting', line):
                self.mounting = int(tmp.group(1))

            elif tmp := searchSingleString(r'CategoryName', line):
                self.category_name = tmp.group(1)

            elif tmp := searchSingleInt(r'CategoryIndex', line):
                self.category_index = int(tmp.group(1))

            elif tmp := searchSingleFloat(r'PatternOrientation', line):
                self.orientation = float(tmp.group(1))

            # TODO: Implement function for find array
            elif tmp := re.search(r'\(Verification\s(("([NY])+"\s*)*)\)', line):
                if tmp := re.findall(reBool, tmp.group(1)):
                    self.verifications = tmp

            elif tmp := searchSingleFloat(r'PadWidth', line):
                self.pad_width = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadHeight', line):
                self.pad_height = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadWidth_New', line):
                self.pad_width_new = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadHeight_New', line):
                self.pad_height_new = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadMask_Percent', line):
                self.mask_percent = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadMask_EdgeGap', line):
                self.mask_edge_gap = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadMask_SegmentGap', line):
                self.mask_segment_gap = float(tmp.group(1))

            elif tmp := searchSingleInt(r'PadMask_SegmentSide', line):
                self.mask_segment_side = int(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadHole', line):
                self.hole_width = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadHoleH', line):
                self.hole_height = float(tmp.group(1))

            elif tmp := searchSingleInt(r'PadHoleType', line):
                self.hole_type = DipTraceHoleTypes(int(tmp.group(1)))

            elif tmp := searchSingleInt(r'PadShape', line):
                self.pad_shape = DipTracePadShapes(int(tmp.group(1)))

            elif tmp := searchSingleInt(r'PadShape_New', line):
                self.pad_shape_new = DipTracePadShapesNew(int(tmp.group(1)))

            elif tmp := searchSingleFloat(r'PadAngle', line):
                self.pad_angle = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadShape_X', line):
                self.pad_shape_x = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadShape_Y', line):
                self.pad_shape_y = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'PadCorner', line):
                self.pad_corner = float(tmp.group(1))

            elif line.startswith('(PadMask_TopSegments '):
                while line := datafile.readline().strip():
                    if line == ')':
                        break

            elif line.startswith('(PadMask_BotSegments '):
                while line := datafile.readline().strip():
                    if line == ')':
                        break

            elif tmp := searchSingleFloat(r'CustomSwell_New', line):
                self.custom_swell = float(tmp.group(1))

            elif tmp := searchSingleFloat(r'CustomShrink_New', line):
                self.custom_shrink = float(tmp.group(1))

            elif tmp := searchSingleInt(r'TopMask_State', line):
                self.top_mask_state = int(tmp.group(1))

            elif tmp := searchSingleInt(r'BotMask_State', line):
                self.bottom_mask_state = int(tmp.group(1))

            elif tmp := searchSingleInt(r'TopPaste_State', line):
                self.top_mask_state = int(tmp.group(1))

            elif tmp := searchSingleInt(r'BotPaste_State', line):
                self.bottom_paste_state = int(tmp.group(1))

        return self

    def __str__(self) -> str:

        points = '\n'.join([str(point) for point in self.points])
        points_new = '\n'.join([str(point) for point in self.points_new])
        shapes = '\n'.join([str(shape) for shape in self.shapes])
        holes = '\n'.join([str(hole) for hole in self.holes])
        layers = '\n'.join([str(layer) for layer in self.layers])
        terminals = '\n'.join([str(terminal) for terminal in self.terminals])
        categories = '\n'.join([str(category) for category in self.categories])
        dimensions = '\n'.join([str(dimension)
                                for dimension in self.dimensions])
        pads = '\n'.join([str(self.pads[i]).format(i+1)
                          for i in range(len(self.pads))])
        model = str(self.model) + '\n' if hasattr(self, 'model') else ''
        user_fields = '\n'.join(
            f'(UserField "{field[0]}" "{field[1]}" {field[2]})' for field in self.user_fields)
        verifications = ' '.join(
            f'"{verification}"' for verification in self.verifications)
        connections = ''

#        holes = f'(Hole "N" "N" 0 0 0 0 -1)\n{holes}\n(Hole "N" "N" 0 0 0 0 -1)'

        if self.isComponent:
            return ''.join([
                f'(Pattern "{self.name}"\n',
                f'(Type {self.type.value})\n',
                f'(VariableParameter1 "{self.variableParameters[0]}")\n',
                f'(VariableParameter2 "{self.variableParameters[1]}")\n',
                f'(VariableParameter3 "{self.variableParameters[2]}")\n',
                f'(VariableParameter4 "{self.variableParameters[3]}")\n',
                f'(InternalConnections\n{connections})\n',
                f'(Number1 {self.numbers[0]:.6g})\n',
                f'(Number2 {self.numbers[1]:.6g})\n',
                f'(Spacing1 {self.spacings[0]:.6g})\n',
                f'(Spacing2 {self.spacings[1]:.6g})\n',
                f'(VariableParameter5 "{self.variableParameters[4]}")\n',
                f'(Spacing3 {self.spacings[2]:.6g})\n',
                f'(LockProperties "{self.locked}")\n',
                f'(PatternOrientation {self.orientation:.6g})\n',
                f'(Width {mm2units(self.width):.6g})\n',
                f'(Height {mm2units(self.height):.6g})\n',
                f'(PadWidth {mm2units(self.pad_width):.6g})\n',
                f'(PadHeight {mm2units(self.pad_height):.6g})\n',
                f'(PadShape {self.pad_shape.value})\n',
                f'(SurfacePad "{self.surface}")\n',
                f'(PadHole {mm2units(self.hole_width):.6g})\n',
                f'(PadHoleH {mm2units(self.hole_height):.6g})\n',
                f'(PadHoleType {self.hole_type.value})\n',
                f'(PadPoints\n{points}\n)\n',
                f'(PadPoints_New\n{points_new}\n)\n',
                f'(PadShape_New {self.pad_shape_new.value})\n',
                f'(PadAngle {self.pad_angle:.6g})\n',
                f'(PadShape_X {mm2units(self.pad_shape_x):.6g})\n',
                f'(PadShape_Y {mm2units(self.pad_shape_y):.6g})\n',
                f'(PadCorner {self.pad_corner:.6g})\n',
                f'(PadWidth_New {mm2units(self.pad_width_new):.6g})\n',
                f'(PadHeight_New {mm2units(self.pad_height_new):.6g})\n',
                f'(PadTerminalCount {len(self.terminals)}\n{terminals}\n)\n',
                f'(TopMask_State {self.top_mask_state})\n',
                f'(BotMask_State {self.bottom_mask_state})\n',
                f'(TopPaste_State {self.top_mask_state})\n',
                f'(BotPaste_State {self.bottom_paste_state})\n',
                f'(CustomSwell_New {self.custom_swell:.6g})\n',
                f'(CustomShrink_New {self.custom_shrink:.6g})\n',
                f'(PadMask_Percent {self.mask_percent:.6g})\n',
                f'(PadMask_EdgeGap {self.mask_edge_gap:.6g})\n',
                f'(PadMask_SegmentGap {self.mask_segment_gap:.6g})\n',
                f'(PadMask_SegmentSide {self.mask_segment_side:.6g})\n',
                # TODO: implement PadMask_TopSegments
                '(PadMask_TopSegments 0\n)\n',
                # TODO: implement PadMask_BotSegments
                '(PadMask_BotSegments 0\n)\n',
                f'(OriginX {mm2units(self.origin_x):.6g})\n',
                f'(OriginY {mm2units(self.origin_y):.6g})\n',
                f'(Origin_Cross "{self.origin_cross}")\n',
                f'(Origin_Circle "{self.origin_circle}")\n',
                f'(Origin_Common {self.origin_common:.6g})\n',
                f'(Origin_Courtyard {self.origin_courtyard:.6g})\n',
                f'(Name_Description "{self.description}")\n',
                f'(Name_Unique "{self.unique_name}")\n',
                f'(RecoveryCode "{self.recovery_code}")\n',
                f'(RecoveryCode_Generator "{self.recovery_generator}")\n',
                f'(RecoveryCode_Model "{self.recovery_model}")\n',
                f'(Manufacturer "{self.manufacturer}")\n',
                '(Pattern_Groups\n)\n',
                f'(Pads\n{pads}\n)\n' if len(self.pads) else '',

                f'(Shapes\n{shapes}\n)\n' if len(self.shapes) else '',
                f'(Holes\n{holes}\n)\n' if len(self.holes) else '',
                f'(Layers\n{layers}\n)\n',
                f'(UserFields\n{user_fields}\n)\n',
                f'(Dimensions\n{dimensions}\n)\n',
                f'{model}\n',
                f'(Mounting {self.mounting})\n',

                f'(CategoryName "{self.category_name}")\n',
                f'(CategoryIndex {self.category_index})\n',
                f'(CategoryTypes {len(self.categories)}\n{categories}\n)\n',
                f'(PossibleNames {len(self.names)}\n)\n',
                ')',
            ])
        else:
            return ''.join([
                f'(Pattern "{self.name}" "{self.ref}"\n',
                f'(Value "{self.value}")\n',
                f'(VariableParameter1 "{self.variableParameters[0]}")\n',
                f'(VariableParameter2 "{self.variableParameters[1]}")\n',
                f'(VariableParameter3 "{self.variableParameters[2]}")\n',
                f'(VariableParameter4 "{self.variableParameters[3]}")\n',
                f'(Width {mm2units(self.width):.6g})\n',
                f'(Height {mm2units(self.height):.6g})\n',
                f'(Spacing1 {self.spacings[0]:.6g})\n',
                f'(Spacing2 {self.spacings[1]:.6g})\n',
                f'(VariableParameter5 "{self.variableParameters[4]}")\n',
                f'(Spacing3 {self.spacings[2]:.6g})\n',
                f'(LockProperties "{self.locked}")\n',
                f'(PatternOrientation {self.orientation:.6g})\n',
                f'(Number1 {self.numbers[0]:.6g})\n',
                f'(Number2 {self.numbers[1]:.6g})\n',
                f'(Type {self.type.value})\n',
                f'(PadWidth {mm2units(self.pad_width):.6g})\n',
                f'(PadHeight {mm2units(self.pad_height):.6g})\n',
                f'(PadShape {self.pad_shape.value})\n',
                f'(SurfacePad "{self.surface}")\n',
                f'(PadHole {mm2units(self.hole_width):.6g})\n',
                f'(PadHoleH {mm2units(self.hole_height):.6g})\n',
                f'(PadHoleType {self.hole_type.value})\n',
                f'(PadPoints\n{points}\n)\n',
                f'(PadPoints_New\n{points_new}\n)\n' if len(
                    self.points_new) else '',
                f'(PadShape_New {self.pad_shape_new.value})\n',
                f'(PadAngle {self.pad_angle:.6g})\n',
                f'(PadShape_X {mm2units(self.pad_shape_x):.6g})\n',
                f'(PadShape_Y {mm2units(self.pad_shape_y):.6g})\n',
                f'(PadCorner {self.pad_corner:.6g})\n',
                f'(PadWidth_New {mm2units(self.pad_width_new):.6g})\n',
                f'(PadHeight_New {mm2units(self.pad_height_new):.6g})\n',
                f'(PadTerminalCount {len(self.terminals)}\n{terminals}\n)\n',
                f'(PadMask_Percent {self.mask_percent:.6g})\n',
                f'(PadMask_EdgeGap {self.mask_edge_gap:.6g})\n',
                f'(PadMask_SegmentGap {self.mask_segment_gap:.6g})\n',
                f'(PadMask_SegmentSide {self.mask_segment_side:.6g})\n',
                f'(TopMask_State {self.top_mask_state})\n',
                f'(BotMask_State {self.bottom_mask_state})\n',
                f'(TopPaste_State {self.top_mask_state})\n',
                f'(BotPaste_State {self.bottom_paste_state})\n',
                f'(CustomSwell_New {self.custom_swell:.6g})\n',
                f'(RecoveryCode {self.recovery_code_int})\n',
                # TODO: implement PadMask_TopSegments
                '(PadMask_TopSegments 0\n)\n',
                # TODO: implement PadMask_BotSegments
                '(PadMask_BotSegments 0\n)\n',
                f'(Pads\n{pads}\n)\n' if len(self.pads) else '',
                f'(Shapes\n{shapes}\n)\n' if len(self.shapes) else '',
                f'(Holes\n{holes}\n)\n',
                f'(OriginX {mm2units(self.origin_x):.6g})\n',
                f'(OriginY {mm2units(self.origin_y):.6g})\n',
                f'(OriginCross "{self.origin_cross}")\n',
                f'(OriginCircle "{self.origin_circle}")\n',
                f'(OriginCommon {self.origin_common:.6g})\n',
                f'(OriginCourtyard {self.origin_courtyard:.6g})\n',
                f'(Name_Description "{self.description}")\n',
                f'(Name_Unique "{self.unique_name}")\n',
                f'(RecoveryCode "{self.recovery_code}")\n',
                f'(RecoveryCode_Generator "{self.recovery_generator}")\n',
                f'(RecoveryCode_Model "{self.recovery_model}")\n',
                f'(Manufacturer "{self.manufacturer}")\n',
                '(Pattern_Groups\n)\n',
                f'(Layers\n{layers}\n)\n',
                f'(UserFields\n{user_fields}\n)\n',
                f'(Dimensions\n{dimensions}\n)\n',  # TODO: Add Dimensions
                f'{model}\n',
                f'(Mounting {self.mounting})\n',
                f'(Datasheet "{self.datasheet}")\n',
                f'(CategoryName "{self.category_name}")\n',
                f'(CategoryIndex {self.category_index})\n',
                f'(CategoryTypes {len(self.categories)}\n{categories}\n)\n',
                f'(PossibleNames {len(self.names)}\n)\n',
                f'(Verification {verifications})\n',
                ')',
            ])


if __name__ == "__main__":
    pass
