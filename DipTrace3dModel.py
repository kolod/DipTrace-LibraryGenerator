#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from io import TextIOWrapper
from typing import List
from reHelper import *
from DipTraceUnits import mm2units, units2mm
from DipTraceEnums import *


class DipTrace3dModel:

	def __init__(self):
		self.setFilename()
		self.setTranslation()
		self.setRotation()
		self.setScale()
		self.setAutomaticSearch()
		self.setFlipByZ()
		super().__init__()

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

			elif tmp := re.search(reJoin(r'pt', reFloat, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat, reBool, reBool, reFloat, reFloat, reFloat, reFloat, reFloat, reFloat), line):
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

		return self

	def __str__(self):
		return \
			f'(Model3D\n' \
			f'(Model3DFile "{self.filename}")\n'\
			f'(pt {self.rotation_x:.4g} {self.rotation_y:.4g} {self.rotation_z:.4g} {self.x:.4g} {self.y:.4g} {self.z:.4g} {self.scale_x:.4g} {self.scale_y:.4g} {self.scale_z:.4g} "{self.flip}" "{self.search}")\n'\
			f')\n'


if __name__ == "__main__":
	pass