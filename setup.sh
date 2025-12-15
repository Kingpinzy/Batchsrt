#!/bin/bash
# 批量视频字幕合成工具 - 一键环境配置脚本 (macOS/Linux)

echo ""
echo "=========================================="
echo "批量视频字幕合成工具 - 环境配置器"
echo "=========================================="
echo ""

# 运行Python配置脚本
python3 setup.py

# 检查退出码
if [ $? -eq 0 ]; then
    echo ""
    echo "✓ 配置完成！现在可以运行 python3 app.py 启动应用"
    echo ""
else
    echo ""
    echo "✗ 配置过程遇到问题，请查看上方错误信息"
    echo ""
    exit 1
fi
