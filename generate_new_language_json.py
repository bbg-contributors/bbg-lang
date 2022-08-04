#!/usr/bin/python3
"""
Usage:
$ python generate_new_language_json.py --id vw_50
"""

import argparse
import json


parser = argparse.ArgumentParser(description='获取语言id')
parser.add_argument('--id',
                    type=str,
                    help='语言id',
                    required=True)
args = parser.parse_args()

with open('meta.json', 'r') as f:
    lang_meta = json.load(f)

key_dict = dict.fromkeys(lang_meta["需要翻译的键值"], "")

with open(f'multi_language/{args.id}.json', 'w') as f:
    json.dump(key_dict, f, indent=4)
