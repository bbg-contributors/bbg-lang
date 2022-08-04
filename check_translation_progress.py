import argparse
import json

parser = argparse.ArgumentParser(description='获取语言id')
parser.add_argument('id', type=str, help='语言id')
args = parser.parse_args()

with open('meta.json', 'r') as f:
    lang_meta = json.load(f)

is_valid_query = False

print(f"\n现在检查 id 为 {args.id} 的语言的翻译进度。\n")

for i in range(len(lang_meta["名称与文件名之间的映射关系"])):
    if args.id == lang_meta["名称与文件名之间的映射关系"][i]["id"]:
        is_valid_query = True

        print(f"语言名称：{lang_meta['名称与文件名之间的映射关系'][i]['name']}")
        print(f"语言id：{lang_meta['名称与文件名之间的映射关系'][i]['id']}\n")

        with open(f"multi_language/{args.id}.json", 'r') as f:
            lang_current = json.load(f)

        keysTotalNumber = len(lang_meta["需要翻译的键值"])

        keysCurrentNumber = 0

        for j in range(keysTotalNumber):
            if lang_meta["需要翻译的键值"][j] in lang_current:
                keysCurrentNumber += 1

        print(f"有效的已翻译键值数：{keysCurrentNumber}")
        print(f"总共需要翻译的键值数：{keysTotalNumber}\n")

        print(f"翻译进度百分比：{keysCurrentNumber / keysTotalNumber * 100}%\n")

if not is_valid_query:
    print(f"元文件中没有记录 id 为 {args.id} ，所以检查失败。", )
    print("如果这是你打算翻译的新语言，请先在元文件（meta.json）中加入有关该语言的信息。\n")
