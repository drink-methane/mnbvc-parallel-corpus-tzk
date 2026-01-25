import json
import os
# from collections import defaultdict
import tools as tos

# 输入数据
directory = r"C:\files\MNBVC\774181_RhythmDoctor\localization"
languages = ["en", "zhs", "zht", "es", "ko", "pt", "pl", "jp", "fr", "de"]

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        file=file.split(".")[0]
        contentl={}
        for language in languages:
            contentl[language]={}
        with open(file_path, 'r', encoding = "utf-8") as f:
            content = json.load(f)
        for key in content:
            for index in range(len(languages)):
                contentl[languages[index]][key]=content[key][index]
        for language in languages:
            json_file_path=os.path.join(root, file, language+".json")
            if not os.path.exists(os.path.join(root, file)):
                os.makedirs(os.path.join(root, file))
            result=contentl[language]
            with open(json_file_path, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                json.dump(result, f, ensure_ascii=False, indent=4)