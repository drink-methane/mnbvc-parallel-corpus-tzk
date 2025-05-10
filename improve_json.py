import json
import json5
# import re
import os
# from pathlib import Path
# import chardet#可用的

'''
处理文件，解决不太严重的格式问题，如果无法处理就直接删掉。
'''

def improve(fileadd):
    with open(fileadd, "r", encoding="utf-8") as f:
        malformed_content = f.read()

    # 使用json5解析非标准JSON内容（自动处理注释、单引号等格式问题）
    parsed_data = json5.loads(malformed_content)
    os.remove(fileadd)

    # 将解析后的数据用标准JSON格式写入（indent=4 添加美观缩进）
    with open(fileadd, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)

directory = r"D:\sandbox\data"

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            improve(file_path)
        except:
            os.remove(file_path)