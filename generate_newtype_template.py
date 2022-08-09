#!/usr/bin/env python3
import json

j = {"lang": "", "name": "", "data": {}}
with open('meta.json', 'r') as f:
    x = json.loads(f.read())["需要翻译的键值"]
for i in x:
    j["data"][i] = ""
with open('template.json', 'w') as f:
    f.write(json.dumps(j, indent=4))
