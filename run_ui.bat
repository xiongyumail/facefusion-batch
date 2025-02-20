@echo off
:: 设置 Conda 环境
call C:\ProgramData\miniforge3\Scripts\activate.bat facefusion

REM 设置Python脚本的路径，如果脚本在当前目录下，则不需要修改  
SET "PYTHON_SCRIPT=./facefusion"   
set GRADIO_SERVER_NAME=0.0.0.0

REM 切换到脚本目录
cd /d "%PYTHON_SCRIPT%"
  
REM 检查Python是否已安装，并获取Python解释器的路径  
WHERE python >nul 2>&1  
IF %ERRORLEVEL% NEQ 0 (  
    ECHO Python没有安装或未添加到环境变量中。  
    EXIT /B %ERRORLEVEL%  
)  

REM 调用Python解释器执行脚本  
python facefusion.py run --config-path .assets/config/facefusion.ini --open-browser
pause
