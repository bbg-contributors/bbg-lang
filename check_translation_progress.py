#!/usr/bin/python3
'''
Usage:
$ python3 check_translation_progress.py --help
$ python3 check_translation_progress.py --id zh_CN
$ python3 check_translation_progress.py --id ja_JP --target-id en_US --verbose
$ python3 check_translation_progress.py --id en_US --reverse
$ python3 check_translation_progress.py --all
$ python3 check_translation_progress.py --all --fix --sort
'''

import argparse
import os
import json


def is_valid(lang_data):
    required_keys = ['LANG', 'LANG_NAME']
    return all(key in lang_data for key in required_keys)


def check_selected(lang_data,
                   lang_target,
                   verbose=False,
                   reverse=False,
                   fix=False):
    lang_id = lang_data['LANG']
    target_id = lang_target['LANG']
    if reverse:
        print(f'\n现在使用 ID 为 {lang_id} 的语言，反向检查 {target_id}。')
        lang_data, lang_target = lang_target, lang_data
        lang_id = lang_data['LANG']
        target_id = lang_target['LANG']
    else:
        print(f'\n现在检查 ID 为 {lang_id} 的语言的翻译进度。')

    translated_num = 0
    for key in lang_target:
        if key not in lang_data:
            if verbose:
                print(f'{key} 不在 {lang_id} 中。')
            if fix:
                lang_data[key] = lang_target[key]
                if verbose:
                    print(f'已将 {key} 的值设置为 {lang_target[key]}。')
        else:
            translated_num += 1

    if translated_num != len(lang_target) and verbose:
        print()

    print(f'目标语言共有 {len(lang_target)} 个条目，其中 {translated_num} 个已翻译。')
    print(f'翻译进度为 {translated_num / len(lang_target) * 100:.2f}%。\n\n')

    return lang_data


parser = argparse.ArgumentParser(description='检查已有语种的翻译进度')
parser.add_argument('--id',
                    type=str,
                    help='语言id',
                    default=None,
                    required=False)
parser.add_argument('--target-id',
                    type=str,
                    help='目标语言id',
                    default=None,
                    required=False)
parser.add_argument('-a', '--all', action='store_true', help='检查所有语言')
parser.add_argument('-r', '--reverse', action='store_true', help='反向检查语言')
parser.add_argument('-v', '--verbose', action='store_true', help='输出详细信息')
parser.add_argument('-f', '--fix', action='store_true', help='修复语言')
parser.add_argument('-s', '--sort', action='store_true', help='修复时，按照键值排序')
args = parser.parse_args()

if args.id is None and not args.all:
    print('请输入语言 ID。')
    exit(1)

if args.target_id is None:
    if args.id == 'zh_CN':
        args.target_id = 'en_US'
    else:
        args.target_id = 'zh_CN'

lang_target = None
for i in os.listdir('multi_language'):
    with open(f'multi_language/{i}', 'r') as f:
        lang_data = json.load(f)
    if is_valid(lang_data):
        if lang_data['LANG'] == args.target_id:
            lang_target = lang_data

if lang_target is None:
    print(f'没有找到 ID 为 {args.target_id} 的语言。')
    exit(1)

for i in os.listdir('multi_language'):
    with open(f'multi_language/{i}', 'r') as f:
        lang_data = json.load(f)
    if is_valid(lang_data):
        lang_name = lang_data['LANG_NAME']
        lang_id = lang_data['LANG']
        if args.all or lang_id == args.id:
            if lang_id != args.target_id:
                print(f'语言名称：{lang_name}')
                print(f'语言 ID：{lang_id}')
                if lang_id != args.target_id:
                    lang_data = check_selected(lang_data, lang_target,
                                               args.verbose, args.reverse,
                                               args.fix)
                    if args.fix:
                        with open(f'multi_language/{i}', 'w') as f:
                            json.dump(lang_data,
                                      f,
                                      sort_keys=args.sort,
                                      ensure_ascii=False,
                                      indent=4)
                            print(f'已将 {lang_id} 的语言文件保存。')
            else:
                print(f'跳过 ID 为 {lang_id} 的语言。\n\n')
    else:
        if args.all:
            print(f'文件 {i} 不完整。\n\n')
