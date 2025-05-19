import os
import shutil
import tools as tos

'''
如果有一个文件夹，里面有非常复杂的文件结构，但是最末级，有着一个相对简单的结构，
最末级是这样的，一个文件夹，里面有许多以语种命名的文件夹，每个文件夹里都有多个json文件，
不同语种之间的文件名存在对应，那么就可以用这个脚本处理。
把文件从原来的地方移动到新的地方，顺便重命名，这样就可以直接下一道工序。
'''
def different_folder(source, target):
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)#原文件的位置
            if file_path.endswith('.json'):
                sourc = [i for i, char in enumerate(file_path) if char == '\\']
                parts = root.split('\\')
                sectarget = os.path.join(target, parts[-1])#目标文件夹的位置
                fintarget = os.path.join(target, parts[-1], tos.ha(file_path[:sourc[-2]] + file) + ".json")#目标文件的位置
                if not os.path.exists(sectarget):
                    os.makedirs(sectarget)
                shutil.copy(file_path, fintarget)
    return 0

'''
如果有一个文件夹，里面有非常复杂的文件结构，但是最末级，有着一个相对简单的结构，
最末级是这样的，一个文件夹，里面有许多以语种命名的json文件，那么就可以用这个脚本处理。
把文件从原来的地方移动到新的地方，顺便重命名，这样就可以直接下一道工序。
'''
def same_folder(source, target):
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)#原文件的位置
            if file_path.endswith('.json'):
                sourc = [i for i, char in enumerate(file_path) if char == '\\']
                parts = root.split('\\')
                partss = file.split('.')[0]
                sectarget = os.path.join(target, partss)#目标文件夹的位置
                fintarget = os.path.join(sectarget, tos.ha(file_path[:sourc[-1]]) + ".json")#目标文件的位置
                if not os.path.exists(sectarget):
                    os.makedirs(sectarget)
                shutil.copy(file_path, fintarget)
    return 0

'''
如果有一个文件夹，里面有非常复杂的文件结构，但是最末级，有着一个相对简单的结构，
最末级是这样的，一个文件夹，里面有许多以语种命名的文件夹，每个文件夹里都有多个文件夹，
每个文件夹里面有多个json文件，那么就可以用这个脚本处理。
把文件移动到更外面的文件夹并且重命名，这样就可以使用其他函数进行整理格式。
'''
def to_the_out_folder(source):
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)#原文件的位置
            if file_path.endswith('.json'):
                sourc = [i for i, char in enumerate(file_path) if char == '\\']
                parts = root.split('\\')
                filenameparts = file.split('.')
                filename = parts[-1] + "_" + filenameparts[0]
                fintarget = os.path.join(source, parts[-2], filename + ".json")#目标文件的位置
                sectarget = os.path.join(source, parts[-2])
                if not os.path.exists(sectarget):
                    os.makedirs(sectarget)
                shutil.copy(file_path, fintarget)
    return 0

'''
这个函数是用于处理文件结构的。
假设每一个文件名的按照此规律：xxx_languages，则可以用这个函数。
'''
def do(source, target):
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)#原文件的位置
            sourc = [i for i, char in enumerate(file_path) if char == '\\']
            parts = file_path.split('\\')
            lan = parts[-1].split('_')[1]
            name = parts[-1].split('_')[0]
            sectarget = os.path.join(target, name)#目标文件夹的位置
            fintarget = os.path.join(target, name, lan + ".json")#目标文件的位置
            print(fintarget)
            if not os.path.exists(sectarget):
                os.makedirs(sectarget)
            shutil.copy(file_path, fintarget)
    return 0

source = r"D:\MNBVC\DysonSphereProgram"
target = r"D:\sandbox\data"
# to_the_out_folder(source)
different_folder(source, target)
# same_folder(source, target)
# do(source, target)