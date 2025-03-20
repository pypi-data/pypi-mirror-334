#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-06-04 16:09
# @Author  : Jack
# @File    : test_PyFile

"""
test_PyFile
"""
import json

from NStudyPy import PyFile


def test_random_split_s():
    tag = '职称证'
    PyFile.random_split_s(source_dir=rf'F:\temp\cards\{tag}', target_dir=rf'F:\temp\target\{tag}')


def test_convert_json():
    file_name = r'pred_3.json'
    map_json = PyFile.read_json(file_name)
    new_map = {}
    for key, value in map_json.items():
        try:
            new_map[key] = json.loads(value)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    PyFile.save_json(new_map, file_name)


if __name__ == '__main__':
    # PyFile.delete_repeat_file(r'F:\temp\cards\xxxx')
    # test_random_split_s
    # test_convert_json()
    print(PyFile.get_filename(r'F:\temp\cards\xxxx\user.txt'))
    print(PyFile.get_directory(r'F:\temp\cards\xxxx'))
