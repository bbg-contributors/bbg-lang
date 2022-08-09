#!/usr/bin/python3
"""
Usage:
$ python3 check_translation_progress_next_generation.py --help
$ python3 check_translation_progress_next_generation.py --id zh_CN
$ python3 check_translation_progress_next_generation.py --id ja_JP --verbose
$ python3 check_translation_progress_next_generation.py --id en_US --reverse
$ python3 check_translation_progress_next_generation.py --all
$ python3 check_translation_progress_next_generation.py --all --fix --sort
"""

import argparse
import json


def is_valid_query(lang_id):
    for i in range(len(lang_meta["名称与文件名之间的映射关系"])):
        if lang_id == lang_meta["名称与文件名之间的映射关系"][i]['id']:
            print(f"语言名称：{lang_meta['名称与文件名之间的映射关系'][i]['name']}")
            print(f"语言id：{lang_meta['名称与文件名之间的映射关系'][i]['id']}\n")
            return True
    print(f"元文件中没有记录 id 为 {lang_id} ，所以检查失败。", )
    print("如果这是你打算翻译的新语言，请先在元文件（meta.json）中加入有关该语言的信息。\n")
    return False


def check_selected(lang_id):
    if args.reverse:
        print(f"\n现在使用 id 为 {lang_id} 的语言，反向检查 meta.json。\n")
    else:
        print(f"\n现在检查 id 为 {lang_id} 的语言的翻译进度。\n")

    if is_valid_query(lang_id):
        with open(f"multi_language_next_generation/{lang_id}.json", 'r') as f:
            lang_current = json.load(f)["data"]

        keysCurrentNumber = 0
        keysTranslatedNumber = 0

        if args.reverse:
            keysTotalNumber = len(lang_current)
            for key in lang_current:
                if key in lang_meta["需要翻译的键值"]:
                    keysCurrentNumber += 1
                else:
                    if args.verbose:
                        print(f"{key} 不在 meta.json 中。")
        else:
            keysTotalNumber = len(lang_meta["需要翻译的键值"])
            for key in lang_meta["需要翻译的键值"]:
                if key in lang_current:
                    if not args.reverse and lang_current[key] == "":
                        if args.verbose:
                            print(f"{key} 没有翻译。")
                    else:
                        keysTranslatedNumber += 1
                    keysCurrentNumber += 1
                else:
                    if args.verbose:
                        print(f"{key} 不在 {lang_id}.json 中。")

        if args.verbose:
            if keysCurrentNumber != keysTotalNumber:
                print()
            elif not args.reverse and keysTranslatedNumber != keysTotalNumber:
                print()

        print(f"有效的键值数：{keysCurrentNumber}")
        if not args.reverse:
            print(f"已翻译的键值数：{keysTranslatedNumber}")
        print(f"总键值数：{keysTotalNumber}\n")

        print(f"百分比：{keysCurrentNumber / keysTotalNumber * 100}%\n")

        if keysCurrentNumber == keysTotalNumber:
            return True
        else:
            return False


def fix_selected(lang_id):
    if args.reverse:
        print(f"\n现在使用 id 为 {lang_id} 的语言，反向修复 meta.json。\n")
    else:
        print(f"\n现在修复 id 为 {lang_id} 的语言。\n")
    if is_valid_query(lang_id):
        with open('meta.json', 'r') as f:
            lang_meta = json.load(f)
        with open(f"multi_language_next_generation/{lang_id}.json", 'r') as f:
            lang_current = json.load(f)["data"]

        if args.reverse:
            for key in lang_current:
                if key not in lang_meta["需要翻译的键值"]:
                    lang_meta["需要翻译的键值"].append(key)
                    if args.verbose:
                        print(f"{key} 已添加到 meta.json 中。")
            if args.sort:
                lang_meta["需要翻译的键值"].sort()

            with open('meta.json', 'w') as f:
                json.dump(lang_meta,
                          f,
                          sort_keys=args.sort,
                          ensure_ascii=False,
                          indent=4)

            print("已修复 meta.json \n")
        else:
            for key in lang_meta["需要翻译的键值"]:
                if key not in lang_current:
                    lang_current[key] = ""
                    if args.verbose:
                        print(f"{key} 已添加到 {lang_id}.json 中。")

            with open(f"multi_language_next_generation/{lang_id}.json",
                      'w') as f:
                json.dump(lang_current,
                          f,
                          sort_keys=args.sort,
                          ensure_ascii=False,
                          indent=4)

            print(f"已修复 id 为 {lang_id} 的语言。\n")


parser = argparse.ArgumentParser(description='检查已有语种的翻译进度')
parser.add_argument('--id',
                    type=str,
                    help='语言id',
                    default=None,
                    required=False)
parser.add_argument('-a', '--all', action='store_true', help='检查所有语言')
parser.add_argument('-r', '--reverse', action='store_true', help='反向检查语言')
parser.add_argument('-v', '--verbose', action='store_true', help='输出详细信息')
parser.add_argument('-f', '--fix', action='store_true', help='修复语言')
parser.add_argument('-s', '--sort', action='store_true', help='修复时，按照键值排序')
args = parser.parse_args()

with open('meta.json', 'r') as f:
    lang_meta = json.load(f)

if args.all:
    for i in range(len(lang_meta["名称与文件名之间的映射关系"])):
        lang_id = lang_meta["名称与文件名之间的映射关系"][i]['id']
        lang_stat = check_selected(lang_id)
        if args.fix:
            if not lang_stat:
                fix_selected(lang_id)
            else:
                print(f"id 为 {lang_id} 的语言无需修复。\n")
else:
    if args.id is None:
        print("请输入语言id。")
    else:
        lang_stat = check_selected(args.id)
        if args.fix:
            if not lang_stat:
                fix_selected(args.id)
            else:
                print(f"id 为 {args.id} 的语言无需修复。\n")
