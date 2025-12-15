@echo off
REM 批量视频字幕合成工具 - 一键环境配置脚本 (Windows)

echo.
echo ==========================================
echo 批量视频字幕合成工具 - 环境配置器
echo ==========================================
echo.

REM 运行Python配置脚本
python setup.py

REM 检查退出码
if %ERRORLEVEL% EQU 0 (
    echo.
    echo √ 配置完成！现在可以运行 python app.py 启动应用
    echo.
) else (
    echo.
    echo × 配置过程遇到问题，请查看上方错误信息
    echo.
    exit /b 1
)

pause
