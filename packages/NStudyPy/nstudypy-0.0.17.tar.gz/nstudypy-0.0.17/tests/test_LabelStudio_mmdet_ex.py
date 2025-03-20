#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-07-02 12:00
# @Author  : Jack
# @File    : test_LabelStudio_mmdet_ex

"""
test_LabelStudio_mmdet_ex
"""

import os
import shutil
import time

from NStudyPy import PyFile


def merge_coco_data_all():
    result = {
        "images": [],
        "categories": [],
        "annotations": [],
        "info": {
            "year": 2024,
            "version": "1.0",
            "description": "code render",
            "contributor": "code render",
            "url": "",
            "date_created": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
    }

    json_files = [
        r'E:\Projects\mmdet\data\data_1\result.json',
        r'E:\Projects\mmdet\data\data_2\result.json',
        r'E:\Projects\mmdet\data\data_3\result.json'
    ]

    category_id = 0
    ann_id = 0
    img_id = 0
    for file_path in json_files:
        data = PyFile.read_json(file_path)

        category_id_convert = {}
        categories = []
        for category in data['categories']:
            category_find = next(filter(lambda x: x['name'] == category['name'], result['categories']), None)
            if category_find is None:
                category_id_convert[category['id']] = category_id
                category['id'] = category_id
                categories.append(category)
                category_id = category_id + 1
            else:
                category_id_convert[category['id']] = category_find['id']

        result['categories'].extend(categories)

        images = data['images']
        img_id_convert = {}
        for img in data['images']:
            img_id_convert[img['id']] = img_id
            img['id'] = img_id

            img_id = img_id + 1
        result['images'].extend(images)

        annotations = data['annotations']
        for ann in annotations:
            ann['id'] = ann_id
            ann['image_id'] = img_id_convert[ann['image_id']]
            ann['category_id'] = category_id_convert[ann['category_id']]

            ann_id = ann_id + 1
        result['annotations'].extend(annotations)
    print(list(map(lambda x: x['name'], result['categories'])))
    PyFile.save_json(result, r'E:\Projects\mmdet\data\data\result.json')


if __name__ == '__main__':
    merge_coco_data_all()
