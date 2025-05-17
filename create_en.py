'''
创建一个英文版本的。
'''

import json

path = r"D:\MNBVC\OxygenNotIncluded\zh.json"
with open(path, 'r', encoding = "UTF-8") as f:
    content = json.load(f)
result_dict = {}
for key in content.keys():
    result_dict[key] = key
with open(r"D:\MNBVC\OxygenNotIncluded\en.json", 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
    json.dump(result_dict, f, ensure_ascii=False, indent=4)