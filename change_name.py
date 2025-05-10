'''
这个脚本是不成功的。
'''

import tools as tos
from pathlib import Path
import os
import json

folder = r"D:\sandbox\data"
filename = "GGS_1.jsonl"

# for root, dirs, files in os.walk(folder):
#     for file in files:
#         file_path = os.path.join(root, file)
#         target_path = os.path.join(root, filename)
#         if file_path.endswith('.jsonl'):#处理jsonl文件
#             with open(file_path, 'r', encoding = "UTF-8") as f:
#                 for line in f:
#                     data = json.loads(line)
#                     data["文件名"] = filename
#                     with open(target_path, 'a', encoding='utf-8') as fi:# 将数据写入新的.json文件
#                         json.dump(data, fi, ensure_ascii=False)
#                         fi.write('\n')

for root, dirs, files in os.walk(folder):
    for file in files:
        file_path = os.path.join(root, file)
        target_path = os.path.join(root, filename)
        if file_path.endswith('.jsonl'):
            with open(file_path, 'r', encoding="UTF-8") as f:
                for line in f:
                    data = json.loads(line)
                    data["文件名"] = filename
                    # 生成 JSON 并手动处理转义
                    json_str = json.dumps(data, ensure_ascii=False)
                    json_str = json_str.replace('\\/', '/')  # 移除斜杠转义
                    with open(target_path, 'a', encoding='utf-8') as fi:
                        fi.write(json_str + '\n')