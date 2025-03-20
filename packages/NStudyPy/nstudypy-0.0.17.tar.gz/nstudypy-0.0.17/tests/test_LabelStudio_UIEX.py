#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-06-04 15:21
# @Author  : Jack
# @File    : test_LabelStudio_UIEX

"""
test_LabelStudio_UIEX
"""

from NStudyPy import PyLabelStudio, PyFile, PyEnv, PyString
import json

def get_train_UIEX_cert_stats():
    """
    get stats of label studio data
    """
    file_paths = PyFile.get_file_list(r'E:\Projects\pp-uiex-certs\anns\train')

    # 医师执业证
    print("#######################医师执业证###############################")
    classify_file = list(filter(lambda x: int(x.rsplit('-', 8)[1]) in [3, 4, 5], file_paths))
    PyLabelStudio.stat_UIEX_cert(file_paths=classify_file)
    # 医师资格证
    print("#######################医师资格证###############################")
    classify_file = list(filter(lambda x: int(x.rsplit('-', 8)[1]) in [7, 8, 9], file_paths))
    PyLabelStudio.stat_UIEX_cert(file_paths=classify_file)
    # 职称证
    print("#######################职称证###############################")
    classify_file = list(filter(lambda x: int(x.rsplit('-', 8)[1]) in [11, 12, 13], file_paths))
    PyLabelStudio.stat_UIEX_cert(file_paths=classify_file)

    # 合计结果
    print("#######################合计结果###############################")
    PyLabelStudio.stat_UIEX_cert(file_paths=file_paths)


def get_test_UIEX_cert_stats():
    """
    get stats of label studio data
    """
    file_paths = PyFile.get_file_list(r'E:\Projects\pp-uiex-certs\anns\test')
    # 医师执业证
    print("#######################医师执业证###############################")
    classify_file = list(filter(lambda x: int(x.rsplit('-', 8)[1]) in [6], file_paths))
    PyLabelStudio.stat_UIEX_cert(file_paths=classify_file)
    # 医师资格证
    print("#######################医师资格证###############################")
    classify_file = list(filter(lambda x: int(x.rsplit('-', 8)[1]) in [10], file_paths))
    PyLabelStudio.stat_UIEX_cert(file_paths=classify_file)
    # 职称证
    print("#######################职称证###############################")
    classify_file = list(filter(lambda x: int(x.rsplit('-', 8)[1]) in [14], file_paths))
    PyLabelStudio.stat_UIEX_cert(file_paths=classify_file)

    # 合计结果
    print("#######################合计结果###############################")
    PyLabelStudio.stat_UIEX_cert(file_paths=file_paths)


def generate_UIEX_cert_train_data():
    """
    generate train data from label studio data
    """
    file_paths = PyFile.get_file_list(r'E:\Projects\pp-uiex-certs\anns\train')
    classify_file = list(filter(lambda x: int(x.rsplit('-', 8)[1]) in [3, 4, 5], file_paths))
    PyLabelStudio.convert_to_UIEX(file_paths=classify_file, main_dir=r'E:\Projects\pp-uiex-certs\data_license', domain=PyEnv.get_env('ls_domain'), auth=PyEnv.get_env('ls_auth'))


def generate_UIEX_cert_test_data():
    """
    generate train data from label studio data
    """
    file_paths = PyFile.get_file_list(r'E:\Projects\pp-uiex-certs\anns\test')
    PyLabelStudio.convert_to_UIEX(file_paths=file_paths, main_dir=r'E:\Projects\pp-uiex-certs\data_test', domain=PyEnv.get_env('ls_domain'), auth=PyEnv.get_env('ls_auth'))


def stat_UIEX_cert_acc():
    """
    统计标签准确率
    stat_map = {
        'label': {
            'tag_count': 10,
            'pred_count': 4
        }
    }
    """
    cert_type_map = PyLabelStudio.get_UIEX_cert_type(PyFile.get_file_list(r'E:\Projects\pp-uiex-certs\anns\test'))

    stat_map = {}
    tag = 'all'
    # E:\Projects\pp-uiex-certs\anns\pred
    # E:\Projects\mmdet\data\anns\pred
    # E:\Projects\mmdet\data\anns-glm-4v\pred
    dir_prefix = r'E:\Projects\mmdet\data\anns-glm-4v\pred'
    tag_map = PyFile.read_json(rf'{dir_prefix}\tag_{tag}.json')
    pred_map = PyFile.read_json(rf'{dir_prefix}\pred_{tag}.json')
    for image_id, m in tag_map.items():
        for label, v in m.items():
            label_key = f'{cert_type_map[image_id]}_{label}'
            label_v = stat_map.get(label_key, {
                'tag_count': 0,
                'pred_count': 0
            })

            # pred_v = pred_map.get(image_id, {}).get(label, '')
            pred_v = json.loads(pred_map.get(image_id, {})).get(label, '')
            pred_v = label_amend(v.strip(), label, pred_v).strip()
            if v.strip().replace(' ', '') == pred_v:
                label_v['pred_count'] += 1
            else:
                print(f'{image_id:20} \t {PyString.pad_string(label, 10)}\t\t{cert_type_map[image_id]}\n'
                      f'\t\t打标值: {v}\n'
                      f'\t\t预测值: {pred_v}')
            label_v['tag_count'] += 1

            stat_map.update({
                label_key: label_v
            })

    print(f'{"版本":5}\t{"标签":10}\t{"总标签个数":5}\t{"预测对个数":5}\t{"准确率":10}')
    sum_tag = 0
    sum_pred = 0
    for label_key, v in sorted(stat_map.items(), key=lambda item: item[0]):
        cert_type, label = label_key.split('_')
        sum_tag += v['tag_count']
        sum_pred += v['pred_count']
        print(f"{cert_type:5}\t{PyString.pad_string(label, 10)}\t{v['tag_count']:5}\t{v['pred_count']:10}\t{v['pred_count'] / v['tag_count']:>10.4f}")
    print(f"{'合计':5}\t{'ALL':10}\t{sum_tag:5}\t{sum_pred:10}\t{sum_pred / sum_tag:>10.4f}")
    # for i in _temp:
    #    print(i)


import re

_temp = []
_reg_date = re.compile(r'(\d{4}).*?(\d{2}).*?(\d{2})')
_id_card = re.compile(r'(^\d{15}$)|(^\d{17}[\dXx]$)')


def format_date(date_string):
    match = _reg_date.search(date_string)
    if match:
        year, month, day = match.groups()
        return f"{year}年{month}月{day}日"
    else:
        return ""


def format_id_card(id_card_string):
    match = _id_card.search(id_card_string)
    if match:
        old_id_card, id_card = match.groups()
        return id_card or old_id_card
    else:
        return ""


def label_amend(tag, label, pred):
    pred = pred.replace(label, '').strip()
    if tag == pred:
        return pred
    if "：" in pred:
        pred = pred.rsplit("：", 1)[-1]

    if label in ['签发日期', '发证日期']:
        return format_date(pred)

    if label in ['证书编码']:
        return (pred.replace('证书', '').replace('编', '').replace("码", "")
                .replace('编号', '').replace('管理号', '').replace('资格号', ''))

    if label in ['姓名']:
        pred = pred.replace('Full Name', '')
        pred = re.sub(r'[#，]', '', pred)
        if pred.startswith('姓'):
            pred = pred[1:]
        if pred.startswith('名'):
            pred = pred[1:]
        if pred.endswith('姓'):
            pred = pred[:-1]
        return pred

    if label in ['专业']:
        pred = pred.replace('Category', '').replace('名称', '').replace('从事', '')
        return pred
    if label in ['学历']:
        if '中专' in pred:
            pred = '中专'
        elif '大专' in pred:
            pred = '大专'
        elif '本科' in pred:
            pred = '本科'
        elif '研究生' in pred:
            pred = '研究生'
        return pred

    if label in ['身份证号']:
        return format_id_card(pred)

    if label in ['资格名称/职称']:
        if '中级' in pred or '中' == pred:
            return '中级'

        pred = (pred.replace('卫生技术人员', '').replace('资格名称', '')
                .replace('职务名称', '').replace('评审通过', '').replace('合格', '')
                .replace('现有职称', '').replace('职务名称', ''))
        return pred

    if label in ['主要执业机构']:
        if pred.startswith('主要'):
            pred = pred[2:]
        if pred.endswith('执业机构'):
            pred = pred[:-4]
        return pred

    if label in ['备案机关']:
        pred = pred.replace('签发机关', '').replace('发证机关', '')
        return pred

    return pred


def gen_UIEX_cert_tag_data():
    """
    生产测试数据标签数据
    """
    file_paths = PyFile.get_file_list(r'E:\Projects\pp-uiex-certs\anns\test')
    # 医师执业证
    print("#######################医师执业证###############################")
    result = print_UIEX_cert_acc(tag=[6], file_paths=file_paths)
    PyFile.save_json(result, r'E:\Projects\pp-uiex-certs\anns\pred\tag_1.json')
    # 医师资格证
    print("#######################医师资格证###############################")
    result = print_UIEX_cert_acc(tag=[10], file_paths=file_paths)
    PyFile.save_json(result, r'E:\Projects\pp-uiex-certs\anns\pred\tag_2.json')
    # 职称证
    print("#######################职称证###############################")
    result = print_UIEX_cert_acc(tag=[14], file_paths=file_paths)
    PyFile.save_json(result, r'E:\Projects\pp-uiex-certs\anns\pred\tag_3.json')
    # 合计
    print("#######################合计###############################")
    result = print_UIEX_cert_acc(file_paths=file_paths)
    PyFile.save_json(result, r'E:\Projects\pp-uiex-certs\anns\pred\tag_all.json')


def print_UIEX_cert_acc(tag=[6, 10, 14], file_paths=[]):
    classify_file = list(filter(lambda x: int(x.rsplit('-', 8)[1]) in tag, file_paths))
    map_stat = PyLabelStudio.stat_UIEX_cert_acc(file_paths=classify_file)

    result_map = {}

    for k, v in map_stat.items():
        for kk, vv in v.items():
            # print(f'{kk}: {vv}')
            result_map.update({
                kk: result_map.get(kk, 0) + 1
            })

    print(f'{"标签":10}\t{"标签个数":10} ')
    for label, counts in sorted(result_map.items(), key=lambda item: item[0]):
        print(f"{PyString.pad_string(label, 10)}\t{counts:10}")

    print(f'{"标签总数":10}\t{sum(result_map.values()):10}')
    return map_stat


def merge_json():
    # _dir_prefix = r'E:\Projects\pp-uiex-certs\anns\pred'
    _dir_prefix = r'E:\Projects\mmdet\data\anns\pred'
    PyFile.merge_json(
        list(filter(lambda x: 'pred_' in x, PyFile.get_file_list(_dir_prefix))),
        rf"{_dir_prefix}\pred_all.json",
        data={}
    )


def ls_UIEX_cert():
    # get_train_UIEX_cert_stats()
    # get_test_UIEX_cert_stats()

    # generate_UIEX_cert_train_data()
    # generate_UIEX_cert_test_data()

    # gen_UIEX_cert_tag_data()

    # merge_json()

    stat_UIEX_cert_acc()


if __name__ == '__main__':
    ls_UIEX_cert()
