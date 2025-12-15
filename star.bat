@echo off
REM 批量视频字幕合成工具 - 一键启动脚本 (Windows)
chcp 65001 > nul

echo.
echo ==========================================
echo 批量视频字幕合成工具 - 正在启动...
echo ==========================================
echo.

REM 1. 检查Python是否安装
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 2. 检查并安装依赖 (静默安装，只显示错误)
if exist requirements.txt (
    echo [信息] 正在检查依赖更新...
    pip install -r requirements.txt >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [警告] 依赖安装可能遇到问题，尝试继续运行...
    )
)

REM 3. 打开浏览器 (延迟3秒)
start "" "msedge" http://localhost:5000 >nul 2>&1 || start "" http://localhost:5000

REM 4. 启动应用
echo.
echo [信息] 服务已启动，请保持此窗口打开
echo [信息] 如果浏览器未自动打开，请访问: http://localhost:5000
echo.
python app.py

pause

