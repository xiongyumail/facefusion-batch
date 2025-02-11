@echo off  
  
REM 设置源目录和目标目录  
set "sourceDir=.\.assets"  
set "destDir=.\facefusion"  
set "gitRepo=https://github.com/xiongyumail/facefusion.git"  
set "version=v3.1.0.nsfw"
  
REM 检查目标目录是否存在  
if not exist "%destDir%" (  
    REM 克隆 facefusion 仓库到 %destDir% ...  
    git clone "%gitRepo%" --branch "%version%" --single-branch "%destDir%"  
    if errorlevel 1 (  
        REM 克隆失败，请检查 Git 是否已安装且可用。 
        pause 
        exit /b 1  
    )  
) else (  
    REM facefusion 目录已存在，跳过克隆步骤。  
) 

REM 复制目录（包括子目录和文件）到目标目录  
xcopy /E /I "%sourceDir%" "%destDir%\.assets\"  
if errorlevel 1 (  
    REM 复制文件失败。  
    pause
    exit /b 1  
) 
  
endlocal
pause
