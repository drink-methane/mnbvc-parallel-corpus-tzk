import os
import shutil
import tools as tos
import subprocess
import json
from pathlib import Path

def aliandmove(source, target):
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)#原文件的位置
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding = "UTF-8") as f:# 读取文件内容
                    content = json.load(f)
                text = content["m_texts"]
                end, jad, zhsd, zhtd = {}, {}, {}, {}
                for i in text:
                    end[i["m_stringID"]] = i["m_stringEN"]
                    jad[i["m_stringID"]] = i["m_stringJP"]
                    zhsd[i["m_stringID"]] = i["m_stringSC"]
                    zhtd[i["m_stringID"]] = i["m_stringTC"]
                # enf, jaf, zhsf, zhtf = r""# 各自的目标路径
                enf = os.path.join(target, "en", tos.ha(file_path) + ".json")
                jaf = os.path.join(target, "ja", tos.ha(file_path) + ".json")
                zhsf = os.path.join(target, "zhs", tos.ha(file_path) + ".json")
                zhtf = os.path.join(target, "zht", tos.ha(file_path) + ".json")
                if not os.path.exists(os.path.join(target, "en")):
                    os.makedirs(os.path.join(target, "en"))
                if not os.path.exists(os.path.join(target, "ja")):
                    os.makedirs(os.path.join(target, "ja"))
                if not os.path.exists(os.path.join(target, "zhs")):
                    os.makedirs(os.path.join(target, "zhs"))
                if not os.path.exists(os.path.join(target, "zht")):
                    os.makedirs(os.path.join(target, "zht"))
                with open(enf, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(end, f, ensure_ascii=False, indent=4)
                with open(jaf, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(jad, f, ensure_ascii=False, indent=4)
                with open(zhsf, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(zhsd, f, ensure_ascii=False, indent=4)
                with open(zhtf, 'w', encoding='utf-8') as f:# 将数据写入新的.json文件
                    json.dump(zhtd, f, ensure_ascii=False, indent=4)
    return 0

source = r"D:\MNBVC\SpiceAndWolfVR1"
target = r"D:\sandbox\data"
aliandmove(source, target)