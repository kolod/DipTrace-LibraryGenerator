#!/usr/bin/python3
#-*- coding: utf-8 -*-

from io import TextIOWrapper
from DipTraceUnits import mm2units
from reHelper import searchSingleBool, searchSingleString, searchSingleInt, searchSingleFloat, searchSingleIntlList, searchSingleFloatList
from DipTraceEnums import DipTraceDimentionType, DipTraceDimentionUnits, DipTraceLayerType, DipTraceDimensionPointerType


class DipTraceDimension:

	def __init__(self) -> None:
		self.points      = []
		self.connections = []
		self.setEnabled()
		self.setlocked()
		self.setType()
		self.setLayer()
		self.setArrowSize()
		self.setUnits()
		self.setShowUnits()
		self.setVectorFont()
		self.setFont()
		self.setText()
		self.setAngle()
		self.setGroup()
		self.setPointD()
		self.setExternalRadius()
		self.setPointerMode()
		super().__init__()

	def setEnabled(self, state:bool=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def setlocked(self, state:bool=False):
		self.locked = 'Y' if state else 'N'
		return self

	def setType(self, type:DipTraceDimentionType=DipTraceDimentionType.Free):
		self.type = type
		return self

	def setLayer(self, layer:DipTraceLayerType=DipTraceLayerType.TopDimension):
		self.layer = layer
		return self

	def setArrowSize(self, size:float=1.0):
		self.arrow_size = mm2units(size)
		return self

	def setUnits(self, units:DipTraceDimentionUnits=DipTraceDimentionUnits.Default):
		self.units = units
		return self

	def setShowUnits(self, state:bool=False):
		self.show_units = 'Y' if state else 'N'
		return self

	def setVectorFont(self, state:bool=True):
		self.vector = 'Y' if state else 'N'
		return self

	def setFont(self, name:str='Tahoma', size:int=8, scale:float=1.0, width:float=1.0):
		self.font_name = name
		self.font_size = size
		self.font_scale = scale
		self.font_width = width
		return self

	def setText(self, text:str=''):
		self.text = text
		return self

	def setAngle(self, angle:float=0.0):
		self.angle = angle
		return self

	def setGroup(self, group:int=-1):
		self.group = group
		return self

	def setExternalRadius(self, radius:float=0.0):
		self.radius = radius
		return self

	def setPointerMode(self, mode:DipTraceDimensionPointerType=DipTraceDimensionPointerType.Coordinates):
		self.pointer_mode = mode
		return self

	def setPointD(self, x:float=0.0, y:float=0.0):
		self.point_d = {
			'x' : mm2units(x),
			'y' : mm2units(y)
		}
		return self

	def addPoint(self, x:float=0.0, y:float=0.0):
		self.points.append({
			'x' : mm2units(x),
			'y' : mm2units(y)
		})
		return self

	def addConnection(self, connected:bool=False, object:int=0, sub_object:int=0, point:int=0):
		self.connections.append({
			'connected'  : connected,
			'object'     : object,
			'sub_object' : sub_object,
			'point'      : point
		})
		return self

	def move(self, x:float=0.0, y:float=0.0):
		self.point_d['x'] += mm2units(x)
		self.point_d['y'] += mm2units(y)
		for point in self.points:
			point['x'] += mm2units(x)
			point['y'] += mm2units(y)
		return self

	def load(self, datafile:TextIOWrapper):
		while line := datafile.readline().strip():

			if line == ')':
				break

			elif tmp := searchSingleBool(r'Enabled', line):
				self.enabled = tmp.group(1)

			elif tmp := searchSingleBool(r'Locked', line):
				self.locked = tmp.group(1)

			elif tmp := searchSingleInt(r'Type', line):
				self.type = DipTraceDimentionType(int(tmp.group(1)))

			elif tmp := searchSingleIntlList(r'Connected', line):
				id    = int(tmp.group(1)) - 1
				value = int(tmp.group(2))
				while len(self.connections) < (id + 1):
					self.addConnection()
				self.connections[id]['connected'] = value

			elif tmp := searchSingleIntlList(r'Object', line):
				id    = int(tmp.group(1)) - 1
				value = int(tmp.group(2))
				while len(self.connections) < (id + 1):
					self.addConnection()
				self.connections[id]['object'] = value

			elif tmp := searchSingleIntlList(r'SubObject', line):
				id    = int(tmp.group(1)) - 1
				value = int(tmp.group(2))
				while len(self.connections) < (id + 1):
					self.addConnection()
				self.connections[id]['sub_object'] = value

			elif tmp := searchSingleIntlList(r'Point', line):
				id    = int(tmp.group(1)) - 1
				value = int(tmp.group(2))
				while len(self.connections) < (id + 1):
					self.addConnection()
				self.connections[id]['point'] = value

			elif tmp := searchSingleInt(r'Layer', line):
				self.layer = DipTraceLayerType(int(tmp.group(1)))

			elif tmp := searchSingleFloatList(r'X', line):
				id = int(tmp.group(1)) - 1
				value = float(tmp.group(2))
				while len(self.points) < (id + 1):
					self.addPoint()
				self.points[id]['x'] = value

			elif tmp := searchSingleFloatList(r'Y', line):
				id = int(tmp.group(1)) - 1
				value = float(tmp.group(2))
				while len(self.points) < (id + 1):
					self.addPoint()
				self.points[id]['y'] = value

			elif tmp := searchSingleFloat(r'XD', line):
				self.point_d['x'] = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'YD', line):
				self.point_d['y'] = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'ArrowSize', line):
				self.arrow_size = float(tmp.group(1))

			elif tmp := searchSingleInt(r'Units', line):
				self.units = DipTraceDimentionUnits(int(tmp.group(1)))

			elif tmp := searchSingleBool(r'VectorFont', line):
				self.vector = tmp.group(1)

			elif tmp := searchSingleString(r'FontName', line):
				self.font_name = tmp.group(1)

			elif tmp := searchSingleInt(r'FontSize', line):
				self.font_size = int(tmp.group(1))

			elif tmp := searchSingleFloat(r'FontScale', line):
				self.font_scale = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'FontWidth', line):
				self.font_width = float(tmp.group(1))

			elif tmp := searchSingleBool(r'ShowUnits', line):
				self.show_units = tmp.group(1)

			elif tmp := searchSingleFloat(r'Angle', line):
				self.angle = float(tmp.group(1))

			elif tmp := searchSingleFloat(r'ExternalRadius', line):
				self.radius = float(tmp.group(1))

			elif tmp := searchSingleInt(r'PointerMode', line):
				self.pointer_mode = DipTraceDimensionPointerType(int(tmp.group(1)))

			elif tmp := searchSingleString(r'PointerText', line):
				self.text = tmp.group(1)

			elif tmp := searchSingleInt(r'Group', line):
				self.group = int(tmp.group(1))

		return self

	def __str__(self) -> str:
		return ''.join([
			f'(Dimension\n',
			f'(Enabled "{self.enabled}")\n',
			f'(Locked "{self.locked}")\n',
			f'(Type {self.type.value})\n',
			f'(Connected1 {self.connections[0]["connected"]})\n'  if len(self.connections) >= 1 else '',
			f'(Object1 {self.connections[0]["object"]})\n'        if len(self.connections) >= 1 else '',
			f'(SubObject1 {self.connections[0]["sub_object"]})\n' if len(self.connections) >= 1 else '',
			f'(Point1 {self.connections[0]["point"]})\n'          if len(self.connections) >= 1 else '',
			f'(Connected2 {self.connections[1]["connected"]})\n'  if len(self.connections) >= 2 else '',
			f'(Object2 {self.connections[1]["object"]})\n'        if len(self.connections) >= 2 else '',
			f'(SubObject2 {self.connections[1]["sub_object"]})\n' if len(self.connections) >= 2 else '',
			f'(Point2 {self.connections[1]["point"]})\n'          if len(self.connections) >= 2 else '',
			f'(Layer {self.layer.value})\n',
			f'(X1 {self.points[0]["x"]:.6g})\n(Y1 {self.points[0]["y"]:.6g})\n' if len(self.points) >= 1 else '',
			f'(X2 {self.points[1]["x"]:.6g})\n(Y2 {self.points[1]["y"]:.6g})\n' if len(self.points) >= 2 else '',
			f'(XD {self.point_d["x"]:.6g})\n(YD {self.point_d["y"]:.6g})\n',
			f'(ArrowSize {self.arrow_size:.5g})\n',
			f'(Units {self.units.value})\n',
			f'(VectorFont "{self.vector}")\n',
			f'(FontName "{self.font_name}")\n',
			f'(FontSize {self.font_size})\n',
			f'(FontScale {self.font_scale:.5g})\n',
			f'(FontWidth {self.font_width:.5g})\n',
			f'(ShowUnits "{self.show_units}")\n',
			f'(Angle {self.angle:.5g})\n',
			f'(ExternalRadius {self.radius:.6g})\n',
			f'(PointerMode {self.pointer_mode.value})\n',
			f'(PointerText "{self.text}")\n',
			f'(Group {self.group})\n',
			f')'
		])

if __name__ == "__main__":
	pass