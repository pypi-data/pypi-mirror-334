#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-06-28 18:20
# @Author  : Jack
# @File    : test_LabelStudio_mmdet

"""
test_LabelStudio_mmdet
"""
import shutil
import time
import random
import os
import cv2
from NStudyPy import PyFile


def merge_coco_data():
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
        r'E:\Projects\mmdet\ls_source\11\result.json',
        r'E:\Projects\mmdet\ls_source\12\result.json',
        r'E:\Projects\mmdet\ls_source\13\result.json'
    ]
    ann_id = 0
    img_id = 10000
    for idx, file_path in enumerate(json_files):
        data = PyFile.read_json(file_path)
        if idx == 1:
            result['categories'] = list(map(lambda x: {'id': x['id'] - 3, 'name': x['name']}, data['categories'][3:]))
            print(list(map(lambda x: x['name'], result['categories'])))
        images = data['images']
        annotations = data['annotations']

        img_id_convert = {}
        for img in images:
            file_name = img['file_name']
            target_file_path = os.path.join(r'E:\Projects\mmdet\data\data', file_name)
            if not os.path.exists(target_file_path):
                shutil.copyfile(os.path.join(PyFile.get_directory(file_path), file_name), target_file_path)

            img_id_convert[img['id']] = img_id
            img['id'] = img_id

            img_id = img_id + 1

        result['images'].extend(images)

        for ann in annotations:
            ann['id'] = ann_id
            ann['image_id'] = img_id_convert[ann['image_id']]
            ann['category_id'] = ann['category_id'] - 3

            ann_id = ann_id + 1

        result['annotations'].extend(annotations)

    PyFile.save_json(result, r'E:\Projects\mmdet\data\data\result.json')


def spilt_data(spilt=(0.95, 0.05)):
    data = PyFile.read_json(r'E:\Projects\mmdet\data\data\result.json')
    images = data['images']
    annotations = data['annotations']
    categories = data['categories']
    info = data['info']

    random.shuffle(images)
    train_images = images[:int(len(images) * spilt[0])]
    val_images = images[len(train_images):]
    print(len(images), len(train_images), len(val_images))

    train_result = {
        "images": train_images,
        "categories": categories,
        "annotations": [],
        "info": info
    }
    val_result = {
        "images": val_images,
        "categories": categories,
        "annotations": [],
        "info": info
    }
    for ann in annotations:
        if ann['image_id'] in map(lambda x: x['id'], train_images):
            train_result['annotations'].append(ann)
        else:
            val_result['annotations'].append(ann)
    PyFile.save_json(train_result, r'E:\Projects\mmdet\data\data\train.json')
    PyFile.save_json(val_result, r'E:\Projects\mmdet\data\data\val.json')


def show_data():
    image_path = r'E:\Projects\mmdet\data\data'
    result = PyFile.read_json(rf'{image_path}\result.json')
    categories = result['categories']
    annotations = result['annotations']
    images = result['images']

    for image in images[:2]:
        img = cv2.imread(os.path.join(image_path, image['file_name']))

        anns = list(filter(lambda x: x['image_id'] == image['id'], annotations))
        for ann in anns:
            x1, y1, w, h = ann['bbox']
            x2 = x1 + w
            y2 = y1 + h
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255))

            cat_id = ann['category_id']
            cat_name = list(filter(lambda x: x['id'] == cat_id, categories))[0]['name']
            cv2.putText(img, str(cat_id), (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.imshow(image['file_name'], img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # merge_coco_data()

    spilt_data()

    # show_data()
