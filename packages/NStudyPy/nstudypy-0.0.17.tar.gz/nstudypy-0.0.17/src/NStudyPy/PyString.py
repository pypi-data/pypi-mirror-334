#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-04-25 13:39
# @Author  : Jack
# @File    : PyString

"""
PyString
"""
import random
import string

from wcwidth import wcswidth

from NStudyPy import PyDate


def get_random_id(length: int = 10) -> str:
    """
    生成指定长度的随机字符串

    Args:
        length (int, optional): 字符串长度，默认为10.

    Returns:
        str: 生成的随机字符串.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_trace_id(length: int = 5) -> str:
    """
    生成指定长度的随机字符串，并加上时间戳
    Args:
        length (int, optional): 字符串长度，默认为5.
    Returns:
        str: 生成的随机字符串.
    """
    return f'{PyDate.get_date()}_{get_random_id(length)}'


def pad_string(s, width) -> str:
    """
    填充字符串到指定宽度
    :param s: 字符串
    :param width: 指定宽度
    :return: 填充后的字符串
    """
    return s + ' ' * (width - wcswidth(s))
