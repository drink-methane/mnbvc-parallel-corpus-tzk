'''
去除<后面的乱七八糟的内容。
'''

import json
import os

directory = r"D:\MNBVC\OxygenNotIncluded"
for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        json_file_path = os.path.splitext(file_path)[0] + '.json'
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding = "UTF-8") as f:
                content = json.load(f)
            result_dict = {}
            for key in content.keys():
                result_dict[key] = content[key].split("<")[0]
            with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                json.dump(result_dict, f, ensure_ascii=False, indent=4)