#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from io import TextIOWrapper
from typing import Literal, AnyStr, List
from DipTraceUnits import mm2units, units2mm
from reHelper import reBracketed, searchSingleBool, searchSingleString, searchSingleInt, searchSingleFloat, searchDoubleFloat, searchSingleIntlList, searchSingleBoolList, searchSingleFloatList, reJoin, reString, reBool, reInt
from DipTracePad import DipTracePad
from DipTraceHole import DipTraceHole
from DipTracePoint import DipTracePoint
from DipTrace3dModel import DipTrace3dModel
from DipTracePatternShape import DipTracePatternShape
from DipTraceEnums import DipTracePatternType, DipTracePatternShapeType, DipTraceHoleTypes, DipTracePadShapes, DipTracePadShapesNew
from DipTraceLayer import DipTraceLayer
from DipTraceTerminal import DipTraceTerminal

class DipTracePattern:

	isComponent = False

	def __init__(self, match:re.Match[AnyStr]=None):
		self.pads         = []
		self.shapes       = []
		self.points       = []
		self.pointsNew    = []
		self.holes        = []
		self.layers       = []
		self.terminals    = []
		self.names        = []
		self.user_fields  = []
		self.setName()
		self.setRef()
		self.setManufacturer()
		self.setDatasheet()
		self.setValue()
		self.setLocked()
		self.setSize()
		self.setSurface()
		self.setPadSize()
		self.setShape()
		self.setShapeNew()
		self.setType()
		self.setOrientation()
		self.setVariableParameters()
		self.setNumbers()
		self.setSpacings()
		self.setOrigin()
		self.setDescription()
		self.setUniqueName()
		self.setRecovery()
		self.setPadMask()
		self.setHole()
		self.setVerifications()

		if match:
			self.name = match.group(1)
			self.ref = match.group(2)
		super().__init__()

	def setName(self, name:str=''):
		self.name = name
		return self

	def setRef(self, ref:str=''):
		self.ref = ref
		return self

	def setLocked(self, state:bool=False):
		self.locked = 'Y' if state else 'N'
		return self

	def setSurface(self, state=False):
		self.surface = 'Y' if state else 'N'
		return self

	def setManufacturer(self, manufacturer:str=''):
		self.manufacturer = manufacturer
		return self

	def setDatasheet(self, datasheet:str=''):
		self.datasheet = datasheet
		return self

	def setValue(self, value:str=''):
		self.value = value
		return self

	def setType(self, type:DipTracePatternType=DipTracePatternType.Free):
		self.type = type
		return self

	def setSize(self, width=0.0, height=0.0):
		self.width  = mm2units(width)
		self.height = mm2units(height)
		return self

	def setPadSize(self, width=0.0, height=0.0):
		self.padWidth  = mm2units(width)
		self.padHeight = mm2units(height)
		return self

	def addPad(self, pad):
		if type(pad) is list:
			self.pads.extend(pad)
		else:
			self.pads.append(pad)
		return self

	def setShape(self, shape=DipTracePadShapes.Oval):
		self.shape = shape
		return self

	def setShapeNew(self, shape=DipTracePadShapesNew.Ellipse):
		self.shape_new = shape
		return self

	def addShape(self, shape):
		if type(shape) is list:
			self.shapes.extend(shape)
		else:
			self.shapes.append(shape)
		return self

	def addHole(self, hole:DipTraceHole):
		self.holes.append(hole)
		return self

	def move(self, x:float=0.0, y:float=0.0):
		for pad in self.pads: pad.move(x, y)
		for shape in self.shapes: shape.move(x, y)
		return self

	def add3dModel(self, model:DipTrace3dModel):
		self.model = model
		return self

	def setVariableParameters(self, vars:List[str]=['N', 'N', 'N', 'N', 'N']):
		self.variableParameters = vars
		return self

	def setSpacings(self, spacings:List[float]=[0.0, 0.0, 0.0]):
		self.spacings = spacings
		return self

	def setNumbers(self, numbers:List[int]=[0,0]):
		self.numbers = numbers
		return self

	def setVerifications(self, verifications:List[str]=['N', 'N', 'N', 'N']):
		self.verifications = verifications
		return self

	def setOrigin(self, x:float=0.0, y:float=0.0, cross:bool=True, circle:bool=True, common:float=0.0, courtyard:float=0.0):
		self.orgin_x          = mm2units(x)
		self.orgin_y          = mm2units(y)
		self.orgin_cross      = 'Y' if cross  else 'N'
		self.orgin_circle     = 'Y' if circle else 'N'
		self.orgin_common     = common
		self.orgin_courtyard  = courtyard
		return self

	def setDescription(self, description:str=''):
		self.description = description
		return self

	def setOrientation(self, orientation:float=0.0):
		self.orientation = orientation
		return self

	def setUniqueName(self, name:str=''):
		self.unique_name = name
		return self

	def setRecovery(self, code:str='', generator:bool=False, model:bool=False):
		self.recovery_code      = code
		self.recovery_generator = 'Y' if generator else 'N'
		self.recovery_model     = 'Y' if model     else 'N'
		return self

	def setPadMask(self, percent:float=0.0, edge_gap:float=0.0, segment_gap:float=0.0, segment_side:int=0):
		self.mask_percent      = percent
		self.mask_edge_gap     = edge_gap
		self.mask_segment_gap  = segment_gap
		self.mask_segment_side = segment_side
		return self

	def setHole(self, hole_type=DipTraceHoleTypes.Round, width=0.0, height=0.0):
		self.hole_type   = hole_type
		self.hole_width  = mm2units( width )
		self.hole_height = mm2units( height )
		return self

	def addDefaultShapes(self):
		self.shapes.insert(0,
			DipTracePatternShape(DipTracePatternShapeType.Null)
			.setGroup(0))
		self.shapes.append(
			DipTracePatternShape(DipTracePatternShapeType.Null)
			.setGroup(0))

	def addPoint(self, x:float=0.0, y:float=0.0):
		self.points.append(DipTracePoint(x, y))
		return self

	def addLayer(self, layer:DipTraceLayer):
		self.layers.append(layer)
		return self

	def addTerminal(self, terminal:DipTraceTerminal):
		self.terminals.append(terminal)
		return self

	def addPossibleName(self, name:str=''):
		self.names.append(name)
		return self

	def addUserField(self, name:str='', value:str='', isLink:bool=False):
		self.user_fields.append([name, value, 1 if isLink else 0])
		return self

	@staticmethod
	def pattern() -> Literal:
		return reJoin(r'\(Pattern', reString, reString)

	def load(self, datafile:TextIOWrapper):
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
						name   = tmp.group(1)
						value  = tmp.group(2)
						isLink = int(tmp.group(3))
						self.addUserField(name, value, isLink)

			elif line == '(Dimensions':
				while line := datafile.readline().strip():
					if line == ')':
						break

			elif line == '(PadPoints_New':
				while line := datafile.readline().strip():
					if line == ')':
						break

			elif line.startswith('(CategoryTypes '):
				while line := datafile.readline().strip():
					if line == ')':
						break

			elif line.startswith('(PossibleNames '): # unused
				while line := datafile.readline().strip():
					if line == ')':
						break

			elif line.startswith('(PadMask_TopSegments '):
				while line := datafile.readline().strip():
					if line == ')':
						break

			elif line.startswith('(PadMask_BotSegments '):
				while line := datafile.readline().strip():
					if line == ')':
						break

			elif line.startswith('(PadTerminalCount'):
				while line := datafile.readline().strip():
					if line == ')':
						break
					if line == '(PadTerminal':
						self.addTerminal(DipTraceTerminal().load(datafile))

			elif line == '(Model3D':
				self.add3dModel(DipTrace3dModel().load(datafile))

			elif line == '(Holes':
				while line := datafile.readline().strip():
					if line == ')':
						break
					if tmp := re.search(DipTraceHole.pattern(), line):
						self.addHole(DipTraceHole(match=tmp))

			elif line == '(Shapes':
				while line := datafile.readline().strip():
					if line == ')':
						break
					if tmp := re.search(DipTracePatternShape.pattern(), line):
						self.addShape( DipTracePatternShape(match=tmp).load(datafile))

			elif line == '(PadPoints':
				while line := datafile.readline().strip():
					if line == ')':
						break
					if tmp := searchDoubleFloat(r'pt', line):
						x = units2mm(float(tmp.group(1)))
						y = units2mm(float(tmp.group(2)))
						self.addPoint(x, y)

			elif line == '(Layers':
				while line := datafile.readline().strip():
					if line == ')':
						break
					if line == '(Layer':
						self.addLayer(DipTraceLayer().load(datafile))

			elif line == '(Pads':
				while line := datafile.readline().strip():
					if line == ')':
						break
					elif tmp := re.search(DipTracePad.pattern(), line):
						self.addPad(DipTracePad(match=tmp).load(datafile))

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

			elif tmp := searchSingleFloat(r'PadWidth', line):
				self.padWidth = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadHeight', line):
				self.padHeight = float(tmp.group(1))

			elif tmp := searchSingleInt(r'Type', line):
				self.type = DipTracePatternType(int(tmp.group(1)))

			elif tmp := searchSingleFloat(r'OriginX', line):
				self.orgin_x = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'OriginY', line):
				self.orgin_y = float(tmp.group(1))

			elif tmp := searchSingleBool(r'OriginCross', line):
				self.orgin_cross = tmp.group(1)

			elif tmp := searchSingleBool(r'OriginCircle', line):
				self.orgin_circle = tmp.group(1)

			elif tmp := searchSingleFloat(r'OriginCommon', line):
				self.orgin_common = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'OriginCourtyard', line):
				self.orgin_courtyard = float(tmp.group(1))

			elif tmp := searchSingleString(r'Name_Description', line):
				self.description = tmp.group(1)

			elif tmp := searchSingleString(r'Name_Unique', line):
				self.unique_name = tmp.group(1)

			elif tmp := searchSingleString(r'RecoveryCode', line):
				self.recovery_code = tmp.group(1)

			elif  tmp := searchSingleBool(r'RecoveryCode_Generator', line):
				self.recovery_generator = tmp.group(1)

			elif tmp := searchSingleBool(r'RecoveryCode_Model', line):
				self.recovery_model = tmp.group(1)

			elif tmp := searchSingleString(r'Manufacturer', line):
				self.manufacturer = tmp.group(1)

			elif tmp := searchSingleString(r'Datasheet', line):
				self.datasheet = tmp.group(1)

			elif tmp := searchSingleBool(r'LockProperties', line):
				self.locked = tmp.group(1)

			elif tmp := searchSingleFloat(r'PadMask_Percent', line):
				self.mask_percent = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadMask_EdgeGap', line):
				self.mask_edge_gap = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadMask_SegmentGap', line):
				self.mask_segment_gap = float(tmp.group(1))

			elif tmp := searchSingleInt(r'PadMask_SegmentSide', line):
				self.mask_segment_side = int(tmp.group(1))

			elif tmp := searchSingleBool(r'SurfacePad', line):
				self.surface = tmp.group(1)

			elif tmp := searchSingleFloat(r'PadHole', line):
				self.hole_width = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'PadHoleH', line):
				self.hole_height = float(tmp.group(1))

			elif tmp := searchSingleInt(r'PadHoleType', line):
				self.hole_type = DipTraceHoleTypes(int(tmp.group(1)))

			elif tmp := searchSingleFloat(r'PatternOrientation', line):
				self.orientation = float(tmp.group(1))

			elif tmp := searchSingleInt(r'PadShape', line):
				self.shape = DipTracePadShapes(int(tmp.group(1)))

			elif tmp := searchSingleInt(r'PadShape_New', line):
				self.shape_new = DipTracePadShapesNew(int(tmp.group(1)))

			elif tmp := re.search(r'\(Verification\s(("([NY])+"\s*)*)\)', line): #TODO: Implement function for find array
				if tmp := re.findall(reBool, tmp.group(1)):
					self.verifications = tmp

		return self


	def __str__(self) -> str:

		points     = '\n'.join([str(point)    for point    in self.points    ])
		points_new = '\n'.join([str(point)    for point    in self.pointsNew ])
		pads       = '\n'.join([str(pad)      for pad      in self.pads      ])
		shapes     = '\n'.join([str(shape)    for shape    in self.shapes    ])
		holes      = '\n'.join([str(hole)     for hole     in self.holes     ])
		layers     = '\n'.join([str(layer)    for layer    in self.layers    ])
		terminals  = '\n'.join([str(terminal) for terminal in self.terminals ])

		holes   = '(Holes\n'   + holes   + '\n)\n' if len(holes)   else ''
		pads    = '(Pads\n'    + pads    + '\n)\n' if len(pads)    else ''
		shapes  = '(Shapes\n'  + shapes  + '\n)\n' if len(shapes)  else ''

		model   = str(self.model) + '\n' if hasattr(self, 'model') else ''

		user_fields   = '\n'.join(f'(UserField "{field[0]}" "{field[1]}" {field[2]})' for field in self.user_fields)
		verifications = ' '.join(f'"{verification}"' for verification in self.verifications)

		return ''.join([
			f'(Pattern "{self.name}" "{self.ref}"\n',
			f'(Value "{self.value}")\n',
			f'(VariableParameter1 "{self.variableParameters[0]}")\n',
			f'(VariableParameter2 "{self.variableParameters[1]}")\n',
			f'(VariableParameter3 "{self.variableParameters[2]}")\n',
			f'(VariableParameter4 "{self.variableParameters[3]}")\n',
			f'(Width {self.width:.5g})\n',
			f'(Height {self.height:.5g})\n',
			f'(Spacing1 {self.spacings[0]:.5g})\n',
			f'(Spacing2 {self.spacings[1]:.5g})\n',
			f'(VariableParameter5 "{self.variableParameters[4]}")\n',
			f'(Spacing3 {self.spacings[2]:.5g})\n',
			f'(LockProperties "{self.locked}")\n',
			f'(PatternOrientation {self.orientation:.5g})\n',
			f'(Number1 {self.numbers[0]})\n',
			f'(Number2 {self.numbers[1]})\n',
			f'(Type {self.type.value})\n',
			f'(PadWidth {self.padWidth})\n',
			f'(PadHeight {self.padHeight})\n',
			f'(PadShape {self.shape.value})\n',
			f'(SurfacePad "{self.surface}")\n',
			f'(PadHole {self.hole_width:.5g})\n',
			f'(PadHoleH {self.hole_height:.5g})\n',
			f'(PadHoleType {self.hole_type.value})\n',
			f'(PadPoints\n{points}\n)\n',
			f'(PadPoints_New\n{points_new}\n)\n',
			f'(PadShape_New {self.shape_new.value})\n',
			f'(PadTerminalCount {len(self.terminals)}\n{terminals}\n)\n',

			f'(PadMask_Percent {self.mask_percent:.5g})\n',
			f'(PadMask_EdgeGap {self.mask_edge_gap:.5g})\n',
			f'(PadMask_SegmentGap {self.mask_segment_gap:.5g})\n',
			f'(PadMask_SegmentSide {self.mask_segment_side})\n',

			f'(PadMask_TopSegments 0\n)\n', #TODO: implement PadMask_TopSegments
			f'(PadMask_BotSegments 0\n)\n', #TODO: implement PadMask_BotSegments

			f'{pads}\n',
			f'{shapes}\n',
			f'{holes}\n',
			f'(OriginX {self.orgin_x:.5g})\n',
			f'(OriginY {self.orgin_y:.5g})\n',
			f'(OriginCross "{self.orgin_cross}")\n',
			f'(OriginCircle "{self.orgin_circle}")\n',
			f'(OriginCommon {self.orgin_common:.5g})\n',
			f'(OriginCourtyard {self.orgin_courtyard:.5g})\n',
			f'(Name_Description "{self.description}")\n',
			f'(Name_Unique "{self.unique_name}")\n',
			f'(RecoveryCode "{self.recovery_code}")\n',
			f'(RecoveryCode_Generator "{self.recovery_generator}")\n',
			f'(RecoveryCode_Model "{self.recovery_model}")\n',
			f'(Manufacturer "{self.manufacturer}")\n',
			f'(Pattern_Groups\n)\n',
			f'(Layers\n{layers}\n)\n',
			f'(UserFields\n{user_fields}\n)\n',
			f'(Dimensions\n)\n', #TODO: Add Dimensions
			f'{model}\n',
			f'(Datasheet "{self.datasheet}")\n',
			f'(PossibleNames {len(self.names)}\n)\n',
			f'(Verification {verifications})\n',
			f')',
		])


if __name__ == "__main__":
	import os
	os.system('DipTracePatternLibrary.py')