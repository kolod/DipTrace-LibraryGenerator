#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import re
from typing import Optional, List
from pyfields import field, make_init
from DipTrace.reHelper import searchSingleString, reJoin, reInt
from DipTrace.pad import DipTracePad
from DipTrace.pattern import DipTracePattern
from DipTrace.indentation import DipTraceIndentation


class DipTracePatternLibrary(object):

    patterns: List[DipTracePattern] = field(default=[], doc='Patterns')
    name: str = field(default='', doc='Library name')
    hint: str = field(default='', doc='Library hint')

    __init__ = make_init()

    def normalize(self):
        for pattern in self.patterns:
            pattern.normalize()

    def pattern(self, name: str) -> Optional[DipTracePattern]:
        for pattern in self.patterns:
            if name == pattern.name:
                return pattern
        return None

    def save(self, filename: str) -> None:
        with open(filename, 'w', encoding='cp1251') as datafile:
            datafile.write(str(self))

    def load(self, filename: str):
        with open(filename, 'r', encoding='cp1251') as datafile:
            while line := datafile.readline().strip():

                if tmp := searchSingleString(r'Name', line):
                    self.name = tmp.group(1)
                    continue

                elif tmp := searchSingleString(r'Hint', line):
                    self.hint = tmp.group(1)
                    continue

                elif tmp := re.search(reJoin(r'\(Categories', reInt), line):
                    while line := datafile.readline().strip():
                        if line == ')':
                            break

                elif line == '(Patterns':
                    while line := datafile.readline().strip():
                        if line == ')':
                            break
                        if tmp := re.search(DipTracePattern.pattern(), line):
                            self.patterns.append(
                                DipTracePattern(match=tmp).load(datafile))

        return self

    def __str__(self) -> str:
        DipTracePattern.isComponent = False  # Fix for DipTracePattern
        DipTracePad.isComponent = False  # Fix for DipTracePattern

        patterns = '\n'.join([str(pattern) for pattern in self.patterns])

        return DipTraceIndentation(''.join([
            '(Source "DipTrace-ComLibrary" 22)\n',
            '(Library\n',
            f'(Size {len(self.patterns)})\n',
            f'(Name "{self.name}")\n',
            f'(Hint "{self.hint}")\n',
            '(Categories 0\n)\n',
            f'(Patterns\n{patterns}\n)\n',
            ')\n',
            '()\n'
        ]))


if __name__ == "__main__":
    pass
