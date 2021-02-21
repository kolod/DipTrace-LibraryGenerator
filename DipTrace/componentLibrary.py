#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from typing import List
from pyfields import field, make_init
from DipTrace.pad import DipTracePad
from DipTrace.component import DipTraceComponent
from DipTrace.indentation import DipTraceIndentation
from DipTrace.categoryType import DipTraceCategoryType
from DipTrace.patternShape import DipTracePatternShape
from DipTrace.pattern import DipTracePattern


class DipTraceComponentLibrary:

    components: List[DipTraceComponent] = field(default=[], doc='Components')
    name: str = field(default='', doc='Library name')
    hint: str = field(default='', doc='Library hint')

    __init__ = make_init()

    def __str__(self) -> str:
        DipTracePad.isComponent = True           # Fix for DipTracePad
        DipTracePattern.isComponent = True       # Fix for DipTracePattern
        DipTracePatternShape.isComponent = True  # Fix for DipTracePatternShape
        DipTraceCategoryType.isComponent = True  # Fix for DipTraceCategoryType

        components = '\n'.join([str(component)
                                for component in self.components])

        return DipTraceIndentation(''.join([
            '(Source "DipTrace-ElementLibrary" 29)\n',
            '(Library\n',
            f'(Name "{self.name}")\n',
            f'(Hint "{self.hint}")\n',
            '(Subfolders\n)\n',
            '(Categories 0\n)\n',
            f'(Components\n{components})\n',
            ')\n',
            '()\n',
        ]))

    def save(self, filename: str):
        with open(filename, 'w', encoding='cp1251') as datafile:
            datafile.write(str(self))


if __name__ == "__main__":
    pass
