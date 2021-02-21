#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from io import TextIOWrapper
from typing import List
from pyfields import field, make_init
from DipTrace.reHelper import searchSingleBool, searchSingleInt
from DipTrace.bool import DipTraceBool


class DipTracePatternLayer(object):

    number: int = field(default=0, doc='Layer number')
    enabled: DipTraceBool = field(default=DipTraceBool(True), doc='Enabling shape')
    shapes: List[int] = field(default=[], doc='Shapes')
    holes: List[int] = field(default=[], doc='Holes')
    pads: List[int] = field(default=[], doc='Pads')

    __init__ = make_init()

    @enabled.converter(accepts=bool)
    def toDipTraceBool(self, field, value) -> DipTraceBool:
        return DipTraceBool(value)

    def load(self, datafile: TextIOWrapper):
        while line := datafile.readline().strip():

            if line == ')':
                break

            elif tmp := searchSingleBool(r'Enabled', line):
                self.enabled = tmp.group(1)

            elif tmp := searchSingleInt(r'Number', line):
                self.number = int(tmp.group(1))

            elif line == '(Pads':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    elif tmp := searchSingleInt(r'pt', line):
                        self.pads.append(int(tmp.group(1)))

            elif line == '(Shapes':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    elif tmp := searchSingleInt(r'pt', line):
                        self.shapes.append(int(tmp.group(1)))

            elif line == '(Holes':
                while line := datafile.readline().strip():
                    if line == ')':
                        break
                    elif tmp := searchSingleInt(r'pt', line):
                        self.holes.append(int(tmp.group(1)))

        return self

    def __str__(self) -> str:

        pads = '\n'.join(f'(pt {pad})' for pad in self.pads)
        shapes = '\n'.join(f'(pt {shape})' for shape in self.shapes)
        holes = '\n'.join(f'(pt {hole})' for hole in self.holes)

        return ''.join([
            '(Layer\n',
            f'(Enabled "{self.enabled}")\n',
            f'(Number {self.number})\n',
            # TODO: Check this hack
            f'(Pads\n{pads}\n)\n' if self.number != 2 else '',
            # TODO: Check this hack
            f'(Shapes\n{shapes}\n)\n' if self.number != 2 else '',
            f'(Holes\n{holes}\n)\n',
            ')\n',
        ])


if __name__ == "__main__":
    pass
