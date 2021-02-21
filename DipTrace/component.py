#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

from typing import List
from pyfields import field, make_init
from DipTrace.pattern import DipTracePattern
from DipTrace.componentPart import DipTraceComponentPart


class DipTraceComponent:

    name: str = field(default='', doc='')
    value: str = field(default='', doc='')
    ref: str = field(default='', doc='')
    parts: List[DipTraceComponentPart] = field(default=[], doc='')
    pattern: DipTracePattern = field(default=DipTracePattern(), doc='')

    __init__ = make_init()

    def __str__(self) -> str:
        parts = '\n'.join([str(part) for part in self.parts])
        pattern = str(self.pattern) if hasattr(self, 'pattern') else ''

        return '\n'.join([
            '(Component\n',
            f'{parts}\n',
            f'{pattern}\n',
            ')\n'
        ])


if __name__ == "__main__":
    pass
