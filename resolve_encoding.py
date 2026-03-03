import json
import os
import tools as tos
import stat

directory = r"C:\files\MNBVC\zimuku_ass_srt_classify_askmodel\111"

for root, dirs, files in os.walk(directory):
    for file in files:
        file_path = os.path.join(root, file)
        extension="."+file.split(".")[-1]
        content=tos.readfile(file_path, extension)
        os.chmod(file_path, stat.S_IWRITE)#去除只读属性
        os.remove(file_path)
        if extension == ".json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=4)
        else:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)