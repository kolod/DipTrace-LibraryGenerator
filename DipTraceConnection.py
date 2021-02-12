#!/usr/bin/python3
#-*- coding: utf-8 -*-

from pyfields import field
from DipTraceBool import DipTraceBool

class DipTraceConnection:

	connected    :DipTraceBool = field(default=DipTraceBool(True), doc='')
	object       :int          = field(default=0, doc='')
	sub_object   :int          = field(default=0, doc='')
	point        :int          = field(default=0, doc='')

	def __init__(self) -> None:
		super().__init__()

	def __str__(self) -> str:
		return ''.join([
			f'(Connected{"{0}"} {self.connected})\n',
			f'(Object{"{0}"} {self.object})\n',
			f'(SubObject{"{0}"} {self.sub_object})\n',
			f'(Point{"{0}"} {self.point})\n',
		])

if __name__ == "__main__":
	pass