#!/usr/bin/python3
#-*- coding: utf-8 -*-


from enum import Enum
from DipTraceUnits import *
from DipTracePatternLibrary import *

class DipTracePin:

	def __init__(self, number, name=None):
		self.number = number
		self.name   = name or 'P{0}'.format(number)
		self.setLocked()
		self.setEnabled()
		self.setType()
		self.setElectric()
		self.setOrientation()
		self.setLength()
		self.setShowName()

	def setLocked(self, state=True):
		self.locked = 'Y' if state else 'N'
		return self

	def setEnabled(self, state=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def setShowName(self, state=False):
		self.show = 'Y' if state else 'N'
		return self

	def setType(self, type=DipTracePinType.Undefined):
		self.type = type
		return self

	def setElectric(self, electric=DipTracePinElectric.Undefined):
		self.electric = electric
		return self

	def setOrientation(self, orientation=DipTracePinOrientation.Right):
		self.orientation = orientation
		return self

	def setPosition(self, x=0.0, y=0.0):
		self.x = mm2units(x)
		self.y = mm2units(y)
		return self

	def setLength(self, length=3.81):
		self.length = mm2units(length)
		return self



	def __str__(self):
		result  = '            (Pin {1} {0.x} {0.y}\n'.format(self, '{1}')
		result += '              (Enabled "{0.locked}")\n'.format(self)
		result += '              (Locked "{0.enabled}")\n'.format(self)
		result += '              (Type {0.type.value})\n'.format(self)
		result += '              (ElectricType {0.electric.value})\n'.format(self)
		result += '              (Orientation {0.orientation.value})\n'.format(self)
		result += '              (Number -1)\n'
		result += '              (StringNumber "{0.number}")\n'.format(self)
		result += '              (Length {0.length})\n'.format(self)
		result += '              (Name "{0.name}")\n'.format(self)
		result += '              (ShowName "{0.show}")\n'.format(self)

		result += '              (PinNumXShift 0)\n'
		result += '              (PinNumYShift 0)\n'
		result += '              (PinNamexShift 0)\n'
		result += '              (PinNameYShift 0)\n'
		result += '              (NameFontSize 5)\n'
		result += '              (NameFontWidth -2)\n'
		result += '              (NameFontScale 1)\n'
		result += '              (SignalDelay 0)\n'
		result += '              (Group -1)\n'
		result += '              (PinNumRotate 0)\n'
		result += '              (PinNameRotate 0)\n'
		result += '            )\n'
		return result

class DipTraceComponentPart:

	def __init__(self, name, type=DipTraceComponentPartType.Normal):
		self.name           = name
		self.type           = type
		self.pins           = []
		self.shapes         = []
		self.setType()
		self.setEnabled()
		self.setOrigin()
		self.setSize()
		self.setShowNumbers()

	def setType(self, type=DipTraceComponentPartType.Normal):
		self.type = type
		return self

	def setEnabled(self, state=True):
		self.enabled = 'Y' if state else 'N'
		return self

	def addPin(self, pin):
		self.pins.append(pin)
		return self

	def addShape(self, shape):
		if type(shape) is list:
			self.shapes.extend(shape)
		else:
			self.shapes.append(shape)
		return self

	def setShowNumbers(self, state=True):
		self.show_numbers = 1 if state else 0
		return self

	def setOrigin(self, x=0.0, y=0.0):
		self.origin_x = mm2units( x )
		self.origin_y = mm2units( y )
		return self

	def setSize(self, width=0.0, height=0.0):
		self.width  = mm2units(  width )
		self.height = mm2units( height )
		return self

	def __str__(self):

		result  = '        (Part "{0.name}" "{0.ref}"\n'
		result += '          (Enabled "{0.enabled}")\n'.format(self)
		result += '          (PartType {0.type.value})\n'.format(self)
		result += '          (PartName "{0.name}")\n'.format(self)
		result += '          (ShowNumbers {0.show_numbers})\n'.format(self)
		result += '          (Type {0.type.value})\n'.format(self)
		result += '          (Width {0.width})\n'.format(self)
		result += '          (Height {0.height})\n'.format(self)
		result += '          (OriginX {0.origin_x})\n'.format(self)
		result += '          (OriginY {0.origin_y})\n'.format(self)
		result += '          (Value "{0.value}")\n'

		result += '          (Number1 0)\n'
		result += '          (Number2 0)\n'
		result += '          (LockProperties "N")\n'
		result += '          (Datasheet "")\n'
		result += '          (ModelType 0)\n'
		result += '          (ModelString "")\n'
		result += '          (ModelBody\n'
		result += '          )\n'
		result += '          (Manufacturer "")\n'
		result += '          (CategoryName "Connectors")\n'
		result += '          (CategoryIndex -1)\n'
		result += '          (CategoryTypes 0\n'
		result += '          )\n'
		result += '          (SubfolderIndex 1)\n'
		result += '          (Verification "N" "N" "N" "N" "N" "N" "N")\n'

		if len(self.pins):
			i = 0
			result += '          (Pins\n'
			for pin in self.pins:
				result += str(pin).format(self, i)
				i += 1
			result += '          )\n'

		if len(self.shapes):
			result += '          (Shapes\n'
			i = 0
			for shape in self.shapes:
				result += str(shape).format(i)
				i += 1
			result += '          )\n'

		result += '        )\n'

		return result

class DipTraceComponent:

	def __init__(self, name, ref='', value=None):
		self.name   = name
		self.value  = value or name
		self.ref    = ref
		self.parts  = []

	def addPart(self, part):
		self.parts.append(part)
		return self

	def setPattern(self, pattern):
		self.pattern = pattern
		return self

	def __str__(self):
		result  = '      (Component\n'
		for part in self.parts: result += str(part).format(self)
		if self.pattern: result += str(self.pattern)
		result += '      )\n'
		return result


class DipTraceComponentLibrary:

	def __init__(self, name, hint=None):

		self.name = name
		self.hint = hint or name
		self.components = []

	def addComponent(self, component):
		self.components.append(component)
		return self

	def __str__(self):
		DipTracePattern.isComponent = True # Fix for DipTracePattern

		result  = '(Source "DipTrace-ElementLibrary" 28)\n'
		result += '  (Library\n'
		result += '    (Name "{0.name}")\n'.format(self)
		result += '    (Hint "{0.hint}")\n'.format(self)
		result += '    (Subfolders\n'
		result += '    )\n'
		result += '    (Categories 0\n'
		result += '    )\n'

		if len(self.components):
			result += '    (Components\n'
			for component in self.components: result += str(component)
			result += '    )\n'

		result += '  )\n'
		result += '()\n'

		return result

	def save(self, filename):
		with open(filename, 'w', encoding='utf-8') as f:
			f.write(str(self))


if __name__ == "__main__":
	pass