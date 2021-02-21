#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import re
from typing import AnyStr, Literal, Optional

reTag = r'\((\w*)'
reBool = r'"([YN]?)"'
reString = r'"([^"]*)"'
reFloat = r'([-]*\d+(?:\.\d+)?)'
reInt = r'([-]*\d*)'


def reBracketed(r: re.Match) -> Literal:
    return r'\(' + r + r'\)'


def reJoin(*args: re.Match) -> Literal:
    return r' '.join(args)


def reSingleBool(name: re.Match) -> Literal:
    return reBracketed(reJoin(name, reBool))


def reSingleString(name: re.Match) -> Literal:
    return reBracketed(reJoin(name, reString))


def reSingleInt(name: re.Match) -> Literal:
    return reBracketed(reJoin(name, reInt))


def reSingleFloat(name: re.Match) -> Literal:
    return reBracketed(reJoin(name, reFloat))


def searchSingleBool(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(reJoin(name, reBool)), text)


def searchSingleString(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(reJoin(name, reString)), text)


def searchSingleInt(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(reJoin(name, reInt)), text)


def searchSingleFloat(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(reJoin(name, reFloat)), text)


def searchDoubleFloat(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(reJoin(name, reFloat, reFloat)), text)


def searchSingleBoolList(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(name + reJoin(reInt, reBool)), text)


def searchSingleStringList(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(name + reJoin(reInt, reString)), text)


def searchSingleIntlList(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(name + reJoin(reInt, reInt)), text)


def searchSingleFloatList(name: re.Match, text: str) -> Optional[re.Match[AnyStr]]:
    return re.search(reBracketed(name + reJoin(reInt, reFloat)), text)


def getTag(text) -> Optional[str]:
    if tmp := re.search(reTag, text):
        return tmp.group(1)
    return None


if __name__ == "__main__":
    pass
