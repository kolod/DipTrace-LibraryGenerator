#!/usr/bin/python3
#-*- coding: utf-8 -*-


import os
import re

from io import TextIOWrapper
from typing import  Literal, AnyStr

from DipTraceUnits import mm2units, units2mm
from reHelper import searchSingleBool, searchSingleString, searchSingleInt, searchSingleFloat, searchDoubleFloat, searchSingleBoolList, searchSingleFloatList, reJoin, reString, reFloat, reInt

from DipTracePad import DipTracePad
from DipTraceHole import DipTraceHole
from DipTracePoint import DipTracePoint
from DipTrace3dModel import DipTrace3dModel
from DipTracePatternShape import DipTracePatternShape
from DipTraceEnums import DipTracePatternType, DipTracePatternShapeType
from DipTraceLayer import DipTraceLayer
from DipTraceTerminal import DipTraceTerminal


class DipTracePattern:

	isComponent = False

	def __init__(self, match:re.Match[AnyStr]=None):
		self.pads       = []
		self.shapes     = []
		self.points     = []
		self.pointsNew  = []
		self.holes      = []
		self.layers     = []
		self.terminals  = []
		self.setName()
		self.setRef()
		self.setManufacturer()
		self.setvalue()
		self.setSize()
		self.setPadSize()
		self.setType()
		self.setVariableParameter()
		self.setSpacing()
		self.setOrigin()
		self.setDescription()
		self.setUniqueName()
		self.setRecovery()
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

	def setManufacturer(self, manufacturer:str=''):
		self.manufacturer = manufacturer
		return self

	def setvalue(self, value:str=''):
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

	def addShape(self, shape):
		if type(shape) is list:
			self.shapes.extend(shape)
		else:
			self.shapes.append(shape)
		return self

	def addHole(self, hole:DipTraceHole):
		self.holes.append(hole)
		return self

	def move(self, x=0.0, y=0.0):
		for pad in self.pads: pad.move(x, y)
		for shape in self.shapes: shape.move(x, y)
		return self

	def add3dModel(self, model:DipTrace3dModel):
		self.model = model
		return self

	def setVariableParameter(self, vars=None):
		self.variableParameter = vars or ['N', 'N', 'N', 'N', 'N']
		return self

	def setSpacing(self, spacing=None):
		self.spacing = spacing or [0, 0, 0]
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

	def setUniqueName(self, name:str=''):
		self.unique_name = name
		return self

	def setRecovery(self, code:str='', generator:bool=False, model:bool=False):
		self.recovery_code      = code
		self.recovery_generator = 'Y' if generator else 'N'
		self.recovery_model     = 'Y' if model     else 'N'
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

			elif line.startswith('(PossibleNames '):
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

			if line.startswith('(PadTerminalCount'):
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
					self.variableParameter[id] = tmp.group(2)

			elif tmp := searchSingleFloatList(r'Spacing', line):
				if tmp.group(2):
					id = int(tmp.group(1)) - 1
					self.spacing[id] = float(tmp.group(2))

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

			elif  tmp := searchSingleFloat(r'OriginX', line):
				self.orgin_x = float(tmp.group(1))

			elif  tmp := searchSingleFloat(r'OriginY', line):
				self.orgin_y = float(tmp.group(1))

			elif  tmp := searchSingleBool(r'OriginCross', line):
				self.orgin_cross = tmp.group(1)

			elif  tmp := searchSingleBool(r'OriginCircle', line):
				self.orgin_circle = tmp.group(1)

			elif  tmp := searchSingleFloat(r'OriginCommon', line):
				self.orgin_common = float(tmp.group(1))

			elif  tmp := searchSingleFloat(r'OriginCourtyard', line):
				self.orgin_courtyard = float(tmp.group(1))

			elif  tmp := searchSingleString(r'Name_Description', line):
				self.description = tmp.group(1)

			elif  tmp := searchSingleString(r'Name_Unique', line):
				self.unique_name = tmp.group(1)

			elif  tmp := searchSingleString(r'RecoveryCode', line):
				self.recovery_code = tmp.group(1)

			elif  tmp := searchSingleBool(r'RecoveryCode_Generator', line):
				self.recovery_generator = tmp.group(1)

			elif  tmp := searchSingleBool(r'RecoveryCode_Model', line):
				self.recovery_model = tmp.group(1)

			elif tmp := searchSingleString(r'Manufacturer', line):
				self.manufacturer = tmp.group(1)

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

		return ''.join([
			f'(Pattern "{self.name}" "{self.ref}"\n',
			f'(Value "{self.value}")\n',
			f'(VariableParameter1 "{self.variableParameter[0]}")\n',
			f'(VariableParameter2 "{self.variableParameter[1]}")\n',
			f'(VariableParameter3 "{self.variableParameter[2]}")\n',
			f'(VariableParameter4 "{self.variableParameter[3]}")\n',
			f'(Width {self.width:.5g})\n',
			f'(Height {self.height:.5g})\n',
			f'(Spacing1 {self.spacing[0]:.5g})\n',
			f'(Spacing2 {self.spacing[1]:.5g})\n',
			f'(VariableParameter5 "{self.variableParameter[4]}")\n',
			f'(Spacing3 {self.spacing[2]:.5g})\n',
			f'(Type {self.type.value})\n',
			f'(PadWidth {self.padWidth})\n',
			f'(PadHeight {self.padHeight})\n',
			f'(PadPoints\n{points}\n)\n',
			f'(PadPoints_New\n{points_new}\n)\n',
			f'(PadTerminalCount {len(self.terminals)}\n{terminals}\n)\n',
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
			f'{model}\n',
			f')',
		])


if __name__ == "__main__":
	os.system('DipTracePatternLibrary.py')