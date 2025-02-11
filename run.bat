@echo off
:: 设置 Conda 环境
call C:\ProgramData\miniforge3\Scripts\activate.bat facefusion

REM 设置Python脚本的路径，如果脚本在当前目录下，则不需要修改  
SET "PYTHON_SCRIPT=."   
  
REM 检查Python是否已安装，并获取Python解释器的路径  
WHERE python >nul 2>&1  
IF %ERRORLEVEL% NEQ 0 (  
    ECHO Python没有安装或未添加到环境变量中。  
    EXIT /B %ERRORLEVEL%  
)  

set "target_dir=.\facefusion\.assets\data\target"  
set "output_dir=.\facefusion\.assets\data\output"  
  
rd /s /q "%target_dir%"  
rd /s /q "%output_dir%" 

REM 调用Python解释器执行脚本  
python "%PYTHON_SCRIPT%"/mapping.py -m copy -d "%target_dir%" 
python "%PYTHON_SCRIPT%"/run.py
python "%PYTHON_SCRIPT%"/mapping.py -m restore -s "%output_dir%"
pause
