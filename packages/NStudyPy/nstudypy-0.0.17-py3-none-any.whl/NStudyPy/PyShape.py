#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-04-25 13:53
# @Author  : Jack
# @File    : PyShape

"""
PyShape
"""
from shapely import Polygon


def get_bounds(coords: list) -> tuple[float, float, float, float]:
    """
    计算多边形坐标点的最小边界框。

    Args:
        coords (list[tuple[float, float]]): 多边形坐标点列表，每个坐标点为(x, y)。

    Returns:
        tuple[float, float, float, float]: 最小边界框的左上角和右下角坐标点坐标，
            格式为(left, bottom, right, top)。

    """
    polygon = Polygon(coords)
    return polygon.bounds
