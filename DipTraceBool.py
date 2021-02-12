#!/usr/bin/python3
#-*- coding: utf-8 -*-

from pyfields import field

class DipTraceBool:

	state:bool = field(native=True, default=False, doc='State')

	def __init__(self, state:bool=False) -> None:
		self.state = state
		super().__init__()

	def __str__(self) -> str:
		return 'Y' if self.state else 'N'

if __name__ == "__main__":
	pass