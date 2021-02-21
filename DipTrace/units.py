#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import math


def mm2units(value):
    return round(value * 3, 5) + 0.0


def units2mm(value):
    return round(value / 3, 5) + 0.0


def inch2mm(value):
    return round(value * 25.4, 5) + 0.0


def mm2inch(value):
    return round(value / 25.4, 5) + 0.0


def mm2units_p(value):
    return round(value, 5) + 0.0 if value < 0 else mm2units(value)


def units2mm_p(value):
    return round(value, 5) + 0.0 if value < 0 else units2mm(value)


def deg2rad(value):
    return round(math.radians(value), 5) + 0.0


def rad2deg(value):
    return round(math.degrees(value), 5) + 0.0


if __name__ == "__main__":
    pass
