# Facefusion-Batch 项目使用指南
## 一、项目概述
FaceFusion是一个强大的图像和视频处理项目，能够实现面部融合等功能。本项目提供了一系列脚本和工具，方便用户进行文件管理、任务执行和界面操作。其中`mapping.py`脚本提供了文件编码、复制与恢复功能，在文件处理流程中扮演重要角色。

## 二、环境搭建
### （一）安装Conda
1. 从Conda官方网站下载并安装Conda，确保安装过程中勾选“Add Anaconda to my PATH environment variable”选项，以便将Conda添加到系统环境变量中。

### （二）创建并激活虚拟环境
1. 打开命令提示符或终端，运行以下命令创建名为`facefusion`的虚拟环境，指定Python版本为3.12：
```bash
conda create --name facefusion python=3.12
```
2. 激活虚拟环境：
```bash
conda activate facefusion
```

### （三）安装OpenVINO
在激活的虚拟环境中，运行以下命令安装OpenVINO 2025.0.0版本：
```bash
conda install conda-forge::openvino=2025.0.0
```

### （四）安装项目依赖
1. 运行`install.bat`文件（Windows系统）：
 - 下载项目代码及相关文件，确保包含`install.bat`文件。
 - 以管理员身份运行`install.bat`，该脚本会执行以下操作：
    - 检查`facefusion`目录是否存在，如果不存在，则从指定的GitHub仓库（`https://github.com/xiongyumail/facefusion.git`）克隆项目代码，分支为`v3.1.0.nsfw`。
    - 将`.\.assets`目录下的所有文件（包括子目录和文件）复制到`.\facefusion\.assets`目录中。
2. 或者手动安装（如果`install.bat`不适用）：
 - 按照项目需求，使用`pip`或其他包管理工具安装所需的Python依赖包。依赖包可能包括`concurrent.futures`、`glob`、`subprocess`、`os`、`sys`、`threading`、`time`等，这些通常是Python标准库的一部分，无需额外安装。但对于一些特定的功能，如`openvino`相关的依赖，需要按照上述步骤进行安装。

## 三、文件结构说明
### （一）主要文件和目录
1. **`facefusion`目录**：项目的核心目录，包含主要的Python脚本和配置文件。
2. **`data`目录**：存放数据文件，包括`source`（源文件目录）、`target`（目标文件目录）、`output`（输出文件目录）。
3. **`config`目录**：包含配置文件`facefusion.ini`，用于配置项目的各种参数。
4. **`run.py`**：主要的运行脚本，负责文件扫描、任务创建和执行等操作。
5. **`run.bat`**：Windows批处理文件，用于执行一系列操作，包括删除目标和输出目录、调用`mapping.py`进行文件操作、运行`run.py`。
6. **`run_ui.bat`**：用于启动项目的用户界面，通过运行`facefusion.py run`命令并配置相关参数来打开浏览器显示界面。
7. **`install.bat`**：用于安装项目，包括克隆项目代码和复制相关文件。
8. **`mapping.py`**：实现文件编码、复制和恢复功能的Python脚本，通过MD5算法对文件路径进行编码，以改变文件存储命名方式，同时记录编码路径与原始路径的映射关系，方便后续文件恢复操作。

### （二）文件路径配置
在`run.py`中，通过`BASE_PATHS`和`EXTENSIONS`字典配置了文件路径和文件扩展名：
```python
BASE_PATHS = {
   'source': ('data','source'),
    'target': ('data', 'target'),
    'output': ('data', 'output'),
    'config': ('config', 'facefusion.ini')
}
EXTENSIONS = {
   'source': {'.jpg', '.jpeg', '.png'},
    'target': {'.jpg', '.jpeg', '.png', '.mp4'}
}
```
这些配置决定了项目在运行时查找和处理文件的路径及文件类型。

## 四、`mapping.py`使用方法
### （一）功能说明
1. **文件拷贝与编码**：将源目录中的文件复制到目标目录，并使用MD5算法对文件的相对路径进行编码，生成新的文件名。同时，记录编码后的文件名与原始文件相对路径的映射关系，存储在指定的跟踪文件中。
2. **文件恢复**：根据跟踪文件中记录的映射关系，将编码后的文件从指定目录恢复到原始路径。

### （二）运行方式
1. **命令行参数运行**：在命令提示符或终端中，进入项目所在目录并激活`facefusion`虚拟环境，运行以下命令：
```bash
python mapping.py -m <mode> -s <src_folder> -d <dst_folder> -t <track_file>
```
    - `<mode>`：指定运行模式，`copy`表示拷贝并编码文件，`restore`表示恢复文件。
    - `<src_folder>`：源文件夹路径。如果不指定，运行脚本时会弹出图形化界面让用户选择。
    - `<dst_folder>`：目标文件夹路径。如果不指定，运行脚本时会弹出图形化界面让用户选择。
    - `<track_file>`：跟踪文件名，用于记录文件路径映射关系，默认值为`path_mapping.json`。
2. **图形化界面运行（参数未指定时）**：
    - 若运行命令时未指定`-s`（源文件夹路径）或`-d`（目标文件夹路径）参数，脚本会自动调用Tkinter库打开文件选择对话框。
    - 对于`-s`参数缺失的情况，会弹出“请选择源文件夹”的对话框，用户选择源文件夹后，程序继续执行后续操作。
    - 对于`-d`参数缺失的情况，会弹出“请选择目标文件夹”的对话框，用户选择目标文件夹后，程序继续执行相应的文件拷贝与编码或恢复操作。

### （三）示例
1. **文件拷贝与编码示例**：
```bash
python mapping.py -m copy -s /path/to/source -d /path/to/target -t custom_track.json
```
该命令会将`/path/to/source`目录下的所有文件复制到`/path/to/target`目录，并对文件名进行编码，编码后的路径映射关系记录在`custom_track.json`文件中。
2. **文件恢复示例**：
```bash
python mapping.py -m restore -s /path/to/encoded -d /path/to/restore -t custom_track.json
```
该命令会根据`custom_track.json`中记录的映射关系，将`/path/to/encoded`目录下编码后的文件恢复到`/path/to/restore`目录的原始路径下。

## 五、项目整体使用流程
### （一）准备文件
1. 将源文件（图片格式为`.jpg`、`.jpeg`、`.png`，大小不小于10KB）放置在`.\facefusion\.assets\data\source`目录下。
2. 通过`mapping.py`将目标文件（图片格式为`.jpg`、`.jpeg`、`.png`，视频格式为`.mp4`）放置在`.\facefusion\.assets\data\target`目录下。

### （二）运行项目
1. **命令行运行**：
 - 运行`run.bat`文件（Windows系统）：
    - 以管理员身份运行`run.bat`，该脚本会先删除`.\facefusion\.assets\data\target`和`.\facefusion\.assets\data\output`目录及其内容。
    - 调用`mapping.py`进行文件复制操作（`-m copy -d "%target_dir%"`），按照上述`mapping.py`文件拷贝与编码的逻辑，将相关文件进行处理。
    - 运行`run.py`，`run.py`会执行以下操作：
      - 扫描源文件和目标文件目录，统计符合条件的文件数量和分布情况。
      - 根据源文件分组和目标文件批次，创建并提交任务，每个任务包含多个处理步骤。
      - 启动所有任务的执行，使用`job-run-all`命令，并配置相关执行参数，如执行提供程序为`openvino`，设备ID为`0`，线程数为`32`等。
 - 如果在非Windows系统或需要手动运行，可以在激活的虚拟环境中运行`python run.py`，但需要确保相关依赖已正确安装，并且文件路径和配置符合项目要求。
2. **用户界面运行**：
 - 运行`run_ui.bat`文件（Windows系统）：
    - 以管理员身份运行`run_ui.bat`，该脚本会切换到`facefusion`目录，检查Python是否安装，然后运行`python facefusion.py run --config-path .assets/config/facefusion.ini --open-browser`。
    - 此命令会启动项目的用户界面，并在浏览器中打开，用户可以在界面上进行操作和配置。

## 六、注意事项
1. **文件路径和权限**：确保所有文件路径正确，并且运行脚本的用户具有足够的权限进行文件读写和目录操作。在使用`mapping.py`时，要注意源文件夹和目标文件夹的读写权限，避免因权限不足导致文件操作失败。
2. **依赖版本**：按照上述步骤安装指定版本的依赖包，不同版本可能会导致兼容性问题。
3. **任务执行时间**：任务执行时间可能较长，特别是在处理大量文件或复杂任务时，请耐心等待。在`run.py`中，`job-run-all`命令的执行时间会在控制台输出，方便用户了解任务执行进度。
4. **错误处理**：如果在运行过程中出现错误，如命令执行异常、文件缺失等，根据控制台输出的错误信息进行排查和解决。例如，如果提示缺失必要目录，需要检查文件放置位置是否正确；如果命令执行异常，需要检查命令参数和依赖是否正确安装。在使用`mapping.py`时，如果跟踪文件不存在或格式错误，脚本会给出相应提示，用户需要根据提示检查和修复问题。 