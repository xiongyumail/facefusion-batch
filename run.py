import os
import subprocess
import sys
import threading
from glob import glob

# 常量配置
MIN_SIZE = 10 * 1024  # 10KB
BASE_PATHS = {
    'source': ('data', 'source'),
    'target': ('data', 'target'),
    'output': ('data', 'output'),
    'config': ('config', 'facefusion.ini')
}
EXTENSIONS = {
    'source': {'.jpg', '.jpeg', '.png'},
    'target': {'.jpg', '.jpeg', '.png', '.mp4'}
}

# 初始化工作目录
os.chdir("./facefusion")
base_dir = lambda *p: os.path.join(".assets", *p)
dirs = {k: base_dir(*v) for k, v in BASE_PATHS.items()}
dirs.update({'assets': base_dir()})

# 打印路径信息
print("系统路径配置：")
for k in ['assets', 'source', 'target', 'output', 'config']:
    print(f"{k.upper():<8}: {dirs[k]}")

# 验证必要目录
missing = [k for k in ('source', 'target') if not os.path.exists(dirs[k])]
if missing:
    sys.exit(f"错误：缺失必要目录: {', '.join(missing)}")

def validate_file(path, exts, min_size):
    return os.path.splitext(path)[1].lower() in exts and os.path.getsize(path) >= min_size

def scan_files(folder, exts, min_size, group_subdirs=False):
    found = {}
    for root, _, files in os.walk(folder):
        rel_path = os.path.relpath(root, folder)
        group = rel_path if group_subdirs and rel_path != "." else "main"
        valid = [os.path.join(root, f) for f in files 
                if validate_file(os.path.join(root, f), exts, min_size)]
        if valid:
            found.setdefault(group, []).extend(valid)
    return found

# 收集文件数据
source_data = scan_files(dirs['source'], EXTENSIONS['source'], MIN_SIZE, True)
target_data = scan_files(dirs['target'], EXTENSIONS['target'], MIN_SIZE)

# 打印文件统计
def show_stats(data, name):
    print(f"\n{name}文件分布：")
    for group, files in data.items():
        print(f"{group:<15}: {len(files):>3} 文件")

show_stats(source_data, "源")
show_stats(target_data, "目标")

def execute(cmd):
    """执行命令并实时输出"""
    full_cmd = ['python', 'facefusion.py'] + cmd
    print("\n▶ 执行命令:", ' '.join(full_cmd))
    
    process = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              text=True, bufsize=1)

    def stream_reader(stream, prefix):
        while True:
            line = stream.readline()
            if not line:
                break
            print(f"{prefix}{line}", end='')

    threads = [
        threading.Thread(target=stream_reader, args=(process.stdout, "")),
        threading.Thread(target=stream_reader, args=(process.stderr, ""))
    ]
    for t in threads: t.start()
    for t in threads: t.join()

    if process.wait() != 0:
        print("命令执行异常")

def process_jobs():
    """主处理流程"""
    execute(['job-delete-all'])

    for group, sources in source_data.items():
        output_dir = os.path.join(dirs['output'], group)
        os.makedirs(output_dir, exist_ok=True)

        execute(['job-create', group])
        
        for target in target_data.get('main', []):
            # 判断 target 是否是 mp4 文件
            if target.endswith('.mp4'):
                pixel_size = '128x128'
            else:
                pixel_size = '512x512'
            output = os.path.join(output_dir, os.path.basename(target))
            cmd = [
                'job-add-step', group,
                '--config-path', dirs['config'],
                '--face-swapper-pixel-boost', pixel_size,
                '-s', *sources,
                '-t', target,
                '-o', output
            ]
            execute(cmd)

        execute(['job-submit', group])

    # 启动任务执行
    execute([
        'job-run-all',
        '--execution-providers', 'openvino',
        '--execution-device-id', '0',
        '--execution-thread-count', '32',
        '--execution-queue-count', '2',
        '--video-memory-strategy', 'tolerant',
        '--system-memory-limit', '0'
    ])

if __name__ == "__main__":
    process_jobs()