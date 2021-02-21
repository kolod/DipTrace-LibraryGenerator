#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.

import math

from typing import List, Optional, Tuple
from DipTrace.point import DipTracePoint


def isAngleCrossArc(angle: float, alpha: float, omega: float) -> bool:
    if omega < alpha:
        result: bool = (angle >= omega) and (angle <= alpha)
    else:
        result: bool = (angle >= omega) or (angle <= alpha)
    return result


def getArcFromPoints(points: List[DipTracePoint]) -> Optional[Tuple[float]]:
    if len(points) == 3:
        A = points[0].x - points[1].x
        B = points[0].y - points[1].y
        C = points[2].x - points[1].x
        D = points[2].y - points[1].y
        E = A * (points[1].x + points[0].x) + B * (points[1].y + points[0].y)
        F = C * (points[1].x + points[2].x) + D * (points[1].y + points[2].y)
        G = 2 * (A * (points[2].y - points[0].y) -
                 B * (points[2].x - points[0].x))
        # Points not on one line
        if G != 0:
            # Center point
            X = (D * E - B * F) / G + 0
            Y = (A * F - C * E) / G + 0
            # radius
            R = math.sqrt(
                math.pow(points[1].x - X, 2) + math.pow(points[1].y - Y, 2))
            # Start angle
            Alpha = math.degrees(math.atan2(points[0].y - Y, points[0].x - X))
            # End angle
            Omega = math.degrees(math.atan2(points[2].y - Y, points[2].x - X))
            # If second point from opposite side
            if not isAngleCrossArc(math.degrees(math.atan2(points[1].y - Y, points[1].x - X)), Alpha, Omega):
                Alpha, Omega = Omega, Alpha

            return X, Y, R, Alpha, Omega

    return None


def getArcSize(points: List[DipTracePoint]) -> Optional[List[float]]:
    X, Y, R, Alpha, Omega = getArcFromPoints(points)

    if X is not None:
        max_x = points[0].x
        min_x = points[0].x
        max_y = points[0].y
        min_y = points[0].y

        for point in points:
            if point.x >= max_x:
                max_x = point.x
            if point.x <= min_x:
                min_x = point.x
            if point.y >= max_y:
                max_y = point.y
            if point.y <= min_y:
                min_y = point.y

        if isAngleCrossArc(-180, Alpha, Omega):
            min_x = X - R
        if isAngleCrossArc(-90, Alpha, Omega):
            max_y = Y + R
        if isAngleCrossArc(0, Alpha, Omega):
            max_x = X + R
        if isAngleCrossArc(90, Alpha, Omega):
            min_y = Y - R
        if isAngleCrossArc(180, Alpha, Omega):
            min_x = X - R

        return max_x, min_x, max_y, min_y

    return None


if __name__ == "__main__":
    points = [
        DipTracePoint(x=-1.6, y=-1.07),
        DipTracePoint(x=0, y=-1.925),
        DipTracePoint(x=-1.6, y=1.07)
    ]
    print(getArcFromPoints(points))
    pass
