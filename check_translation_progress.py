#!/usr/bin/python3
"""
Usage:
$ python3 check_translation_progress.py --id zh_CN
$ python3 check_translation_progress.py --id zh_CN --reverse
$ python3 check_translation_progress.py --all
$ python3 check_translation_progress.py --all --reverse
"""

import argparse
import json


def is_valid_query(lang_id):
    for i in range(len(lang_meta["名称与文件名之间的映射关系"])):
        if lang_id == lang_meta["名称与文件名之间的映射关系"][i]["id"]:
            print(f"语言名称：{lang_meta['名称与文件名之间的映射关系'][i]['name']}")
            print(f"语言id：{lang_meta['名称与文件名之间的映射关系'][i]['id']}\n")
            return True
    print(f"元文件中没有记录 id 为 {lang_id} ，所以检查失败。", )
    print("如果这是你打算翻译的新语言，请先在元文件（meta.json）中加入有关该语言的信息。\n")
    return False


def check_selected(lang_id):
    print(f"\n现在检查 id 为 {lang_id} 的语言的翻译进度。\n")

    if is_valid_query(lang_id):
        with open(f"multi_language/{lang_id}.json", 'r') as f:
            lang_current = json.load(f)

        keysTotalNumber = len(lang_meta["需要翻译的键值"])

        keysCurrentNumber = 0

        for j in range(keysTotalNumber):
            if lang_meta["需要翻译的键值"][j] in lang_current:
                keysCurrentNumber += 1

        print(f"有效的已翻译键值数：{keysCurrentNumber}")
        print(f"总共需要翻译的键值数：{keysTotalNumber}\n")

        print(f"翻译进度百分比：{keysCurrentNumber / keysTotalNumber * 100}%\n")

        return [keysCurrentNumber, keysTotalNumber]
    else:
        return None


def check_reverse(lang_id):
    print(f"\n现在使用 id 为 {lang_id} 的语言，反向检查 meta.json。\n")

    if is_valid_query:
        with open(f"multi_language/{lang_id}.json", 'r') as f:
            lang_current = json.load(f)

        keysTotalNumber = len(lang_current)

        keysCurrentNumber = 0

        for key in lang_current:
            if key in lang_meta["需要翻译的键值"]:
                keysCurrentNumber += 1
            else:
                print(f"{key} 不在 meta.json 中。")

        print(f"有效的需要翻译的键值数：{keysCurrentNumber}")
        print(f"总共存在的键值数：{keysTotalNumber}\n")

        print(f"键值百分比：{keysCurrentNumber / keysTotalNumber * 100}%\n")

        return [keysCurrentNumber, keysTotalNumber]
    else:
        return None


parser = argparse.ArgumentParser(description='获取参数')
parser.add_argument('--id',
                    type=str,
                    help='语言id',
                    default=None,
                    required=False)
parser.add_argument('-a', '--all', action='store_true', help='检查所有语言')
parser.add_argument('-r', '--reverse', action='store_true', help='反向检查语言')
args = parser.parse_args()

with open('meta.json', 'r') as f:
    lang_meta = json.load(f)

if args.all:
    for i in range(len(lang_meta["名称与文件名之间的映射关系"])):
        if args.reverse:
            check_reverse(lang_meta["名称与文件名之间的映射关系"][i]["id"])
        else:
            check_selected(lang_meta["名称与文件名之间的映射关系"][i]["id"])
else:
    if args.id is None:
        print("请输入语言id。")
    else:
        if args.reverse:
            check_reverse(args.id)
        else:
            check_selected(args.id)
