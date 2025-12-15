#!/bin/bash

# 批量视频字幕合成工具 - 一键启动脚本 (Linux/macOS)

echo ""
echo "=========================================="
echo "批量视频字幕合成工具 - 正在启动..."
echo "=========================================="
echo ""

# 1. 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装"
    exit 1
fi

# 2. 检查依赖
if [ -f "requirements.txt" ]; then
    echo "[信息] 正在检查依赖更新..."
    pip3 install -r requirements.txt > /dev/null 2>&1
fi

# 3. 启动应用
echo ""
echo "[信息] 服务已启动"
echo "[信息] 请访问: http://localhost:5000"
echo ""

# 后台启动打开浏览器的操作 (根据系统)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sleep 2 && open "http://localhost:5000" &
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sleep 2 && xdg-open "http://localhost:5000" &
fi

python3 app.py

