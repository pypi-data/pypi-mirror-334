#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-05-13 15:48
# @Author  : Jack
# @File    : PyLabelStudio

"""
PyLabelStudio
"""
import json
import os

from NStudyPy import PyString, PyWeb


def convert_to_UIEX(file_paths: [str], main_dir='./data', domain=None, auth=None) -> None:
    """
    将LabelStudio的json文件转换为UIEX格式
    :param file_paths: 文件路径列表
    :param main_dir: 文件保存目录
    :param domain: 图片域名
    :param auth: 网站授权
    :return: None
    """
    skip_list = [
        '8_1693_1148_2e393926_286672_8a8087e78f135286018f9a26ca877240.jpg'
    ]
    _list = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                project_id = item["project"]
                task_id = item["id"]
                data_image = item["data"].get("image")

                annotation = item["annotations"][0]
                ann_result = annotation["result"]
                if ann_result is None or len(ann_result) == 0 or sum(1 for x in ann_result if x['type'] == 'rectanglelabels') == 0:
                    continue
                task_completion_id = annotation["id"]
                new_image_name = f'{project_id}_{task_id}_{task_completion_id}_{str(item["file_upload"]).replace("-", "_")}'
                if new_image_name in skip_list:
                    continue
                image_path = os.path.join(main_dir, 'images', new_image_name)
                if not os.path.exists(image_path):
                    if domain is None:
                        raise Exception('domain or auth is None')
                    PyWeb.save_file_from_url(f'{domain}{data_image}', image_path,
                                             {
                                                 "Authorization": f"Token {auth}"
                                             })
                item["data"]["image"] = new_image_name
                _list.append(item)
    if len(_list) > 0:
        json_str = json.dumps(_list, indent=4, ensure_ascii=False)
        with open(os.path.join(main_dir, 'label_studio.json'), "w", encoding='utf8') as f:
            f.write(json_str)


def stat_UIEX_cert(file_paths: [str]) -> dict:
    """
    统计标签数量(有一个choices标签)
    :param file_paths: 文件路径列表
    :return: 标签数量字典
    """
    map_stat = {}
    for p in file_paths:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                # project_id = item["project"]
                # task_id = item["id"]

                result = item["annotations"][0]['result']
                choices = list(filter(lambda x: x['type'] == 'choices', result))
                if len(choices) == 0:
                    # print(f'project_id: {project_id} task_id:{task_id} this ann no choices')
                    continue
                choice_type = choices[0]['value']['choices'][0]

                choice_type_name = ''
                if choice_type == '1':
                    choice_type_name = '旧版本'
                elif choice_type == '2':
                    choice_type_name = '新版本'
                elif choice_type == '3':
                    choice_type_name = '电子版'

                for ann in result:
                    if ann['type'] == 'rectanglelabels':
                        label = ann['value']['rectanglelabels'][0]
                        choice_map = map_stat.get(label)
                        if choice_map is None:
                            map_stat.update({
                                label: {
                                    '旧版本': 0,
                                    '新版本': 0,
                                    '电子版': 0
                                }
                            })
                        choice_map = map_stat.get(label)
                        v = choice_map.get(choice_type_name)
                        choice_map.update({choice_type_name: v + 1})
                        map_stat.update({label: choice_map})

    print(f'{"类型":5}\t{"标签":10}\t{"标签个数":10} ')
    # 遍历并打印每个标签及其数量
    for t in ['电子版', '旧版本', '新版本']:
        for label, counts in map_stat.items():
            if t in counts:
                print(f"{t:<5}\t{PyString.pad_string(label, 10)}\t{counts[t]:10}")
    return map_stat


def get_new_image_name(item: dict) -> str:
    """
    获取新文件名
    :param item: label studio item
    :return: 新文件名
    """
    project_id = item["project"]
    task_id = item["id"]
    task_completion_id = item["annotations"][0]["id"]

    return f'{project_id}_{task_id}_{task_completion_id}_{str(item["file_upload"]).replace("-", "_")}'


def get_UIEX_cert_type(file_paths: [str]) -> dict:
    """
    获取标签类型(有一个choices标签)
    :param file_paths: 文件路径列表
    :return: 标签选择类型字典
    """
    map_stat = {}
    for p in file_paths:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                annotation = item["annotations"][0]
                ann_result = annotation["result"]
                if ann_result is None or len(ann_result) == 0 or sum(1 for x in ann_result if x['type'] == 'rectanglelabels') == 0:
                    continue
                new_image_name = get_new_image_name(item)

                choices = list(filter(lambda x: x['type'] == 'choices', ann_result))
                if len(choices) == 0:
                    print(f'project_id: {item["project"]} task_id:{ item["id"]} this ann no choices')
                    continue

                choice_type = choices[0]['value']['choices'][0]
                choice_type_name = ''
                if choice_type == '1':
                    choice_type_name = '旧版本'
                elif choice_type == '2':
                    choice_type_name = '新版本'
                elif choice_type == '3':
                    choice_type_name = '电子版'
                map_stat.update({
                    new_image_name: choice_type_name
                })
    return map_stat


def stat_UIEX_cert_acc(file_paths: [str]) -> dict:
    """
    统计标签准确率
    """
    map_stat = {}
    for p in file_paths:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                project_id = item["project"]
                task_id = item["id"]

                annotation = item["annotations"][0]
                task_completion_id = annotation["id"]

                ann_result = annotation["result"]
                if ann_result is None or len(ann_result) == 0 or sum(1 for x in ann_result if x['type'] == 'rectanglelabels') == 0:
                    continue
                new_image_name = f'{project_id}_{task_id}_{task_completion_id}_{str(item["file_upload"]).replace("-", "_")}'

                stat_value = {}
                _no_stat_value = {}
                map_label = {}
                for ann in ann_result:
                    if 'rectanglelabels' == ann['type']:
                        map_label.update({
                            ann['id']: ann['value']['rectanglelabels'][0]
                        })
                    elif 'textarea' == ann['type']:
                        _key = ann['id']
                        if _key in map_label:
                            stat_value.update({
                                map_label[_key]: ann['value']['text'][0]
                            })
                        else:
                            _no_stat_value.update({
                                _key: ann['value']['text'][0]
                            })
                for k, v in _no_stat_value.items():
                    stat_value.update({
                        map_label[k]: v
                    })
                map_stat.update({
                    new_image_name: stat_value
                })
    return map_stat


def get_real_points(ann):
    """
    get real points from annotation
    :param ann: label studio annotation
    :return: real points array
    """
    if 'original_width' not in ann or 'original_height' not in ann:
        return None
    w, h = ann['original_width'], ann['original_height']
    points = ann['value']['points']
    if points:
        return [[w * point[0] / 100.0, h * point[1] / 100.0] for point in points]
    return None


def convert_to_box(ann):
    """
    转换标注格式
    :param ann: 标注信息
    :return: [x, y, w, h]
    """
    if 'original_width' not in ann or 'original_height' not in ann:
        return None
    value = ann['value']
    w, h = ann['original_width'], ann['original_height']
    if all([key in value for key in ['x', 'y', 'width', 'height']]):
        x, y, w, h = w * value['x'] / 100.0, h * value['y'] / 100.0, w * value['width'] / 100.0, h * value['height'] / 100.0
        return [int(x), int(y), int(x + w), int(y + h)]
    return None
