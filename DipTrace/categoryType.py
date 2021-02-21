#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import re
from typing import AnyStr, Literal
from pyfields import field, make_init
from DipTrace.reHelper import reBracketed, reJoin, reInt, reString


class DipTraceCategoryType:

    isComponent: bool = False

    unknownString1: str = field(default='', doc='Unknown string')
    unknownString2: str = field(default='', doc='Unknown string')
    unknownInt1: int = field(default=0, doc='Unknown int')
    unknownInt2: int = field(default=0, doc='Unknown int')

    __init__ = make_init()

    def __init__(self, match: re.Match[AnyStr] = None) -> None:
        if match:
            self.unknownString1 = match.group(1)
            self.unknownString2 = match.group(2)
            self.unknownInt1 = match.group(3)
            self.unknownInt2 = match.group(4)
        super().__init__()

    @staticmethod
    def pattern() -> Literal:
        return reBracketed(reJoin(r'CategoryTypeType', reString, reString, reInt, reInt))

    def __str__(self) -> str:
        if self.isComponent:
            return f'(CategoryType "{self.unknownString1}" "{self.unknownString2}" {self.unknownInt1} {self.unknownInt2})'
        else:
            return f'(CategoryTypeType "{self.unknownString1}" "{self.unknownString2}" {self.unknownInt1} {self.unknownInt2})'


if __name__ == "__main__":
    pass
