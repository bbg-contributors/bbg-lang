# bbg-lang

此仓库包含着 bbg 的 i18n 数据文件。

This repository contains the i18n data of bbg.

## 增加新翻译条目

程序通过读取简体中文和英语的翻译文件来判断哪些条目需要翻译，若要增加新翻译条目，只需先在简体中文（```zh_CN.json```）或英语（```en_US.json```）的翻译文件中添加该条目的翻译，然后再在其它语言的翻译文件中添加该条目的翻译。现在无需在```meta.json```中手动添加需要翻译的键值名。

## 检查已有语种的翻译进度

```
python ./check_translation_progress.py
```