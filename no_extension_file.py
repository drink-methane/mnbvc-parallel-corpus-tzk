'''
处理所有没有扩展名的文件，全部改成txt文件方便后续处理。
'''

import os
# import argparse

directory = r"D:\MNBVC\AstralParty"

for root, dirs, files in os.walk(directory):
    for file in files:
        # 获取文件名和扩展名
        filename, ext = os.path.splitext(file)
        
        # 如果没有扩展名且不是隐藏文件（以点开头）
        if not ext and not file.startswith('.'):
            original_path = os.path.join(root, file)
            new_path = os.path.join(root, file + '.txt')
            
            try:
                os.rename(original_path, new_path)
            except Exception as e:
                print(f"错误: 无法重命名 {original_path} - {str(e)}")
