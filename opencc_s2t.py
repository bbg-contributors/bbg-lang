import opencc
import json
import sys

converter = opencc.OpenCC('s2t.json')


def convert(text):
    assert type(text) == str
    return converter.convert(text)


def recursive_convert(value):
    if type(value) == str:
        return converter.convert(value)
    elif type(value) == list:
        return [recursive_convert(item) for item in value]
    else:
        print('Unsupported type:', type(value))
        sys.exit(1)


def convert_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return converter.convert(text)


custom_dict = {
    # "KEY": "瘋狂星期四",
    # "KEY_WITH_LIST_VALUE": [
    #     "v我",
    #     "50"
    # ],
}

if __name__ == '__main__':
    with open("multi_language/zh_CN.json", 'r') as f:
        lang_cn = json.load(f)

    for key in lang_cn:
        if key in custom_dict:
            lang_cn[key] = custom_dict[key]
        else:
            lang_cn[key] = recursive_convert(lang_cn[key])

    with open("multi_language/zh_TW.json", 'w') as f:
        json.dump(lang_cn, f, ensure_ascii=False, indent=4)
