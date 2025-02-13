import sys
import os
import hashlib
import shutil
import json
import argparse
import tkinter as tk  
from tkinter import filedialog  

def encode_name(relative_path):
    """使用MD5算法编码文件的相对路径，返回编码后的文件名和后缀名"""
    file_name, file_ext = os.path.splitext(relative_path)
    md5_hash = hashlib.md5(file_name.encode('utf-8'))
    encoded_name = md5_hash.hexdigest() + file_ext
    return encoded_name

def copy_and_encode_files(source_dir, target_dir, track_file):
    """将文件拷贝到目标目录，并存储编码路径信息"""
    path_map = {}
    
    # 遍历源目录中的所有文件
    for dirpath, _, filenames in os.walk(source_dir):
        for filename in filenames:
            original_path = os.path.join(dirpath, filename)

            # 获取相对于源目录的文件相对路径
            relative_path = os.path.relpath(original_path, start=source_dir)
            # 编码相对路径
            encoded_name = encode_name(relative_path)
            target_path = os.path.join(target_dir, encoded_name)

            # 确保目标路径的文件夹存在
            os.makedirs(target_dir, exist_ok=True)

            # 拷贝文件到目标路径
            shutil.copy2(original_path, target_path)

            # 记录编码路径与相对路径的映射
            path_map[encoded_name] = relative_path

    # 将路径映射存储到跟踪文件
    with open(track_file, 'w', encoding='utf-8') as f:
        json.dump(path_map, f, ensure_ascii=False)

    print(f"文件已拷贝到 {target_dir} 并记录在 {track_file}")

def restore_files(encoded_dir, restore_dir, track_file):
    """从编码路径中恢复文件到原始路径"""
    try:
        with open(track_file, 'r', encoding='utf-8') as f:
            path_map = json.load(f)
    except FileNotFoundError:
        print(f"跟踪文件 {track_file} 未找到。")
        return
    except json.JSONDecodeError:
        print(f"跟踪文件 {track_file} 格式错误，无法读取。")
        return

    # 获取当前目录及所有子文件夹
    subfolders = [root for root, dirs, _ in os.walk(encoded_dir)]

    # 遍历每个子文件夹
    for subfolder in subfolders:
        restore_subfolder_path = os.path.join(restore_dir, os.path.relpath(subfolder, encoded_dir))
        
        # 遍历 path_map 中的每对路径
        for encoded_file, relative_file_path in path_map.items():
            original_file_path = os.path.join(restore_subfolder_path, relative_file_path)
            source_encoded_file_path = os.path.join(subfolder, encoded_file)

            # 检查文件存在并复制
            if os.path.exists(source_encoded_file_path):
                os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
                shutil.copy2(source_encoded_file_path, original_file_path)

    print(f"文件已从 {encoded_dir} 恢复到原始路径")

def select_directory(title):  
    root = tk.Tk()  
    root.withdraw()  
    directory = filedialog.askdirectory(title=title)  
    return directory  

def main(): 
    parser = argparse.ArgumentParser(description='文件拷贝与编码工具')  
    parser.add_argument('-m', '--mode', type=str, help='模式：copy（拷贝并编码）或 restore（恢复）') 
    parser.add_argument('-s', '--src', type=str, help='源文件夹路径')  
    parser.add_argument('-d', '--dst', type=str, help='目标文件夹路径')  
    parser.add_argument('-t', '--track', type=str, default='path_mapping.json', help='跟踪文件名')
    args = parser.parse_args()  

    if not args.mode:  
        parser.print_help()
        sys.exit("未选择模式，程序退出。")

    src_folder = args.src if args.src else select_directory("请选择源文件夹")  
    if not src_folder:  
        sys.exit("未选择源文件夹，程序退出。")  

    dst_folder = args.dst if args.dst else select_directory("请选择目标文件夹")  
    if not dst_folder:  
        sys.exit("未选择目标文件夹，程序退出。")  

    try:
        if args.mode == 'copy':  
            copy_and_encode_files(src_folder, dst_folder, args.track)
            print("文件已编码复制。")
        elif args.mode == 'restore': 
            restore_files(src_folder, dst_folder, args.track)
            print("文件已恢复。")  
        else:
            sys.exit("错误：无效模式。请使用 'copy' 或 'restore'。")
    except Exception as e:
        sys.exit(f"发生错误：{str(e)}")

if __name__ == "__main__":  
    main()