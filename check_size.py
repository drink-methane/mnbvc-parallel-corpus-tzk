'''
通过这个脚本可以知道一共制作了多少语料。
'''
import os

directory = r"D:\MNBVC备份"

Bsize = 0
for root, dirs, files in os.walk(directory):#获得总大小
    for file in files:
        file_path = os.path.join(root, file)
        if file_path.endswith('.jsonl'):
            Bsize = Bsize + os.path.getsize(file_path)
KBsize = round(Bsize /1024, 3)
MBsize = round(Bsize /1048576, 3)
GBsize = round(Bsize /1073741824, 3)
print("总共", Bsize, "B，", KBsize, "KB，", MBsize, "MB，", GBsize, "GB。")