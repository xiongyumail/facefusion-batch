import os
import subprocess
import sys
import threading
from glob import glob

# 配置目录路径
os.chdir("./facefusion")

assets = os.path.abspath(".assets")
config = os.path.abspath(os.path.join(assets, "config"))
source = os.path.abspath(os.path.join(assets, "data", "source"))
target = os.path.abspath(os.path.join(assets, "data", "target"))
output = os.path.abspath(os.path.join(assets, "data", "output"))
print(f"assets path: {assets}")
print(f"source path: {source}")
print(f"target path: {target}")
print(f"output path: {output}")

config_path = os.path.join(config, "facefusion.ini")
print(f"Config path: {config_path}")

# 验证参数是否已设置
if not all([source, target, output]):
    print("Error: source, target, and output directories must be provided.")
    exit(1)

# 获取源文件列表
source_files = glob(os.path.join(source, "*"))
source_files = [f for f in source_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f"source_files: {source_files}")

# 获取目标文件列表
target_files = glob(os.path.join(target, "*"))
target_files = [f for f in target_files if f.lower().endswith(('.mp4', '.png', '.jpg', '.jpeg'))]
print(f"target_files: {target_files}")

def run_command(command):
    command = ['python', 'facefusion.py'] + command
    print(f"command: {command}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # 行缓冲
    )

    stdout_lines = []
    stderr_lines = []

    def read_stream(stream, buffer, is_stderr):
        while True:
            line = stream.readline()
            if not line:
                break
            buffer.append(line)
            if is_stderr:
                print(line, end='', file=sys.stderr)
            else:
                print(line, end='')

    # 启动线程读取输出
    stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, stdout_lines, False))
    stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, stderr_lines, True))

    stdout_thread.start()
    stderr_thread.start()

    # 等待进程结束
    process.wait()

    # 确保线程结束
    stdout_thread.join()
    stderr_thread.join()

    # 合并输出内容
    stdout_str = ''.join(stdout_lines)
    stderr_str = ''.join(stderr_lines)

    if process.returncode != 0:
        print("\n命令执行失败。")
        print(f"错误详情：\n{stderr_str}")

command = ['job-delete-all']
run_command(command)

# 遍历源文件夹中的所有文件
for source_file_path in source_files:
    # 提取源文件名（不含扩展名）
    source_file_base = os.path.basename(source_file_path)
    source_file_name = os.path.splitext(source_file_base)[0]

    # 构造输出路径并验证其安全性
    output_path = os.path.join(output, source_file_name)
    os.makedirs(output_path, exist_ok=True)

    # 获取目标文件总数
    total_files = len(target_files)

    command = ['job-create', source_file_name]
    run_command(command)

    # 遍历目标文件列表
    for i, target_file_path in enumerate(target_files):
        target_file_base = os.path.basename(target_file_path)
        target_file_name = os.path.splitext(target_file_base)[0]

        output_file_path = os.path.join(output_path, target_file_base)

        # 打印当前进度
        print(f"Processing file {i + 1} of {total_files}: {source_file_path} with {target_file_path} to {output_file_path}")

        # 调用 Python 脚本并检查其返回值
        # 执行命令
        command = [
            'job-add-step', source_file_name,
            '--config-path', config_path,
            '-s', source_file_path,
            '-t', target_file_path,
            '-o', output_file_path
        ]

        run_command(command)

    command = ['job-submit', source_file_name]
    run_command(command)

command = [
    'job-run-all',
    '--execution-providers', 'openvino',
    '--execution-device-id', '0',
    '--execution-thread-count', '32',
    '--execution-queue-count', '2',
    '--video-memory-strategy', 'tolerant', # warmup
    '--system-memory-limit', '0'
]
run_command(command)