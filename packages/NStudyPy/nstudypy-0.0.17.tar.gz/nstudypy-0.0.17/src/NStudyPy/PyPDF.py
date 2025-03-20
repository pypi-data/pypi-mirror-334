#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-04-26 11:06
# @Author  : Jack
# @File    : PyPDF

"""
PyPDF
"""
from enum import Enum
from typing import List

import cv2
import numpy as np
from pdf2image import convert_from_path


class ImageFormat(Enum):
    """
    Image format 枚举
    """
    PIL = 'pil'
    OPENCV = 'opencv'


def convert_images(pdf_path: str, image_format: ImageFormat = ImageFormat.OPENCV) -> List[object]:
    """
    Convert pdf to images
    :param image_format: ImageFormat
    :param pdf_path:
    :return: List[Image.Image] or List[cv2.typing.MatLike]
    """
    images = convert_from_path(pdf_path)
    if image_format == ImageFormat.OPENCV:
        new_images = []
        for image in images:
            opencv_image = np.array(image)
            if opencv_image.shape[2] == 3:
                opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
            new_images.append(opencv_image)
        return new_images
    return images
