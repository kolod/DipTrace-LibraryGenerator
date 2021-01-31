#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from io import TextIOWrapper
from reHelper import searchSingleString, reJoin, reFloat, reBool
from DipTraceUnits import mm2units
from DipTraceEnums import DipTrace3dModelType, DipTrace3dModelUnits


class DipTrace3dModel:

	def __init__(self):
		self.setType()
		self.setUnits()
		self.setHeight()
		self.setColor()
		self.setFilename()
		self.setOrigin()
		self.setTranslation()
		self.setRotation()
		self.setScale()
		self.setAutomaticSearch()
		self.setFlipByZ()
		super().__init__()

	def setType(self, type:DipTrace3dModelType=DipTrace3dModelType.File):
		self.type = type
		return self

	def setUnits(self, units:DipTrace3dModelUnits=DipTrace3dModelUnits.Meters):
		self.units = units
		return self

	def setHeight(self, height:float=0.0):
		''' Set height for outline model generation '''
		self.height = mm2units(height)
		return self

	def setColor(self, r:int=0, g:int=0, b:int=0):
		self.color = r << 16 | g << 8 | b
		return self

	def setOrigin(self, x:float=0.0, y:float=0.0):
		''' Only for IPC-7351 generated type'''
		self.origin_x = mm2units(x) #TODO: Check units
		self.origin_y = mm2units(y) #TODO: Check units
		return self

	def setFilename(self, filename:str=''):
		self.filename = filename
		return self

	def setTranslation(self, x=0.0, y=0.0, z=0.0):
		self.x = x
		self.y = y
		self.z = z
		return self

	def setRotation(self, x=0.0, y=0.0, z=0.0):
		self.rotation_x = x
		self.rotation_y = y
		self.rotation_z = z
		return self

	def setScale(self, x=1.0, y=1.0, z=1.0):
		self.scale_x = x
		self.scale_y = y
		self.scale_z = z
		return self

	def setAutomaticSearch(self, state=False):
		''' Only for file type '''
		self.search = 'Y' if state else 'N'
		return self

	def setFlipByZ(self, state=False):
		self.flip = 'Y' if state else 'N'
		return self

	def load(self, datafile:TextIOWrapper):
		while line := datafile.readline().strip():

			if line == ')':
				break

			if tmp := searchSingleString(r'Model3DFile', line):
				self.filename = tmp.group(1)

			elif tmp := re.search(reJoin(r'pt', reFloat, reFloat, reFloat, reFloat, reFloat, reFloat,
			reFloat, reFloat, reFloat, reBool, reBool, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat), line):
				self.rotation_x = float(tmp.group(1))
				self.rotation_y = float(tmp.group(2))
				self.rotation_z = float(tmp.group(3))
				self.x          = float(tmp.group(4))
				self.y          = float(tmp.group(5))
				self.z          = float(tmp.group(6))
				self.scale_x    = float(tmp.group(7))
				self.scale_y    = float(tmp.group(8))
				self.scale_z    = float(tmp.group(9))
				self.flip       = tmp.group(10)
				self.search     = tmp.group(11)
				self.units      = DipTrace3dModelUnits(int(tmp.group(12)))
				self.origin_x   = float(tmp.group(13))
				self.origin_y   = float(tmp.group(14))
				self.height     = float(tmp.group(15))
				self.color      = int(tmp.group(16))
				self.type       = DipTrace3dModelType(int(tmp.group(17)))

		return self

	def __str__(self):
		return ''.join([
			f'(Model3D\n',
			f'(Model3DFile "{self.filename}")\n',
			f'(pt {self.rotation_x:.4g} {self.rotation_y:.4g} {self.rotation_z:.4g} ',
			f'{self.x:.4g} {self.y:.4g} {self.z:.4g} ',
			f'{self.scale_x:.4g} {self.scale_y:.4g} {self.scale_z:.4g} ',
			f'"{self.flip}" "{self.search}" ',
			f'{self.units.value} {self.origin_x:.5g} {self.origin_y:.5g} {self.height} {self.color} {self.type.value})\n',
			f')\n',
		])


if __name__ == "__main__":
	pass