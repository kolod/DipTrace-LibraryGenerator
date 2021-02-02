#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
from typing import AnyStr, Literal
from reHelper import reBracketed, reJoin, reInt, reString

class DipTraceCategoryType:

	def __init__(self, match:re.Match[AnyStr]) -> None:
		self.unknownString1 = ''
		self.unknownString2 = ''
		self.unknownInt1    = 0
		self.unknownInt2    = 0
		if match:
			self.unknownString1 = match.group(1)
			self.unknownString2 = match.group(2)
			self.unknownInt1    = match.group(3)
			self.unknownInt2    = match.group(4)
		super().__init__()

	@staticmethod
	def pattern() -> Literal:
		return reBracketed(reJoin(r'CategoryTypeType', reString, reString, reInt, reInt))

	def __str__(self) -> str:
		return f'(CategoryTypeType "{self.unknownString1}" "{self.unknownString2}" {self.unknownInt1} {self.unknownInt2})'

if __name__ == "__main__":
	import os
	os.system('DipTracePatternLibrary.py')