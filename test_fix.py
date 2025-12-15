#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试FFmpeg修复效果
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import SubtitleMerger

def create_test_environment():
    """创建测试环境"""
    # 创建临时目录
    test_dir = tempfile.mkdtemp(prefix="subtitle_test_")

    # 创建测试文件夹
    video_folder = os.path.join(test_dir, "videos")
    subtitle_folder = os.path.join(test_dir, "subtitles")
    output_folder = os.path.join(test_dir, "output")

    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(subtitle_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # 创建语言子目录
    en_folder = os.path.join(subtitle_folder, "EN")
    zh_folder = os.path.join(subtitle_folder, "ZH")
    os.makedirs(en_folder, exist_ok=True)
    os.makedirs(zh_folder, exist_ok=True)

    return {
        'test_dir': test_dir,
        'video_folder': video_folder,
        'subtitle_folder': subtitle_folder,
        'output_folder': output_folder,
        'en_folder': en_folder,
        'zh_folder': zh_folder
    }

def create_test_video(video_path, duration=5):
    """使用FFmpeg创建测试视频"""
    cmd = [
        'ffmpeg', '-f', 'lavfi', '-i', f'testsrc=duration={duration}:size=320x240:rate=30',
        '-f', 'lavfi', '-i', f' sine=frequency=1000:duration={duration}',
        '-c:v', 'libx264', '-c:a', 'aac', '-shortest',
        '-y', video_path
    ]

    result = os.system(' '.join(cmd))
    return result == 0

def create_test_subtitle(subtitle_path, content="Test subtitle content"):
    """创建测试字幕文件"""
    srt_content = f"""1
00:00:01,000 --> 00:00:03,000
{content}

2
00:00:03,500 --> 00:00:05,000
This is a test subtitle
"""

    with open(subtitle_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    return True

def test_subtitle_merger():
    """测试字幕合成功能"""
    print("="*60)
    print("\u6b63在创建测试环境...")
    print("="*60)

    # 创建测试环境
    test_env = create_test_environment()

    try:
        # 创建测试视频
        video_path = os.path.join(test_env['video_folder'], "001.mp4")
        print(f"\u6b63在创建测试视频: {video_path}")

        if not create_test_video(video_path):
            print("\u2757 \u65e0法创建测试视频，请确保FFmpeg已安装")
            return False

        # 创建测试字幕（多种命名模式）
        test_cases = [
            ("001_EN.srt", "English subtitle"),
            ("EN_001.srt", "English subtitle (reversed)"),
            ("001.EN.srt", "English subtitle (dot)"),
            ("EN.srt", "English subtitle (language only)"),
        ]

        for filename, content in test_cases:
            subtitle_path = os.path.join(test_env['en_folder'], filename)
            print(f"\u6b63在创建字幕: {filename}")
            create_test_subtitle(subtitle_path, content)

        # 创建中文字幕
        zh_subtitle_path = os.path.join(test_env['zh_folder'], "001_ZH.srt")
        create_test_subtitle(zh_subtitle_path, "\u4e2d文字幕\u6d4b\u8bd5")

        print("\n" + "="*60)
        print("\u6b63在\u6d4b\u8bd5\u5b57\u5e55\u5408\u6210...")
        print("="*60)

        # 创建合成器实例
        merger = SubtitleMerger()

        # 测试合成
        success_count = 0
        total_tests = 0

        # 测试每个字幕文件
        for filename, _ in test_cases:
            total_tests += 1
            subtitle_path = os.path.join(test_env['en_folder'], filename)
            output_path = os.path.join(test_env['output_folder'], f"test_{filename.replace('.srt', '.mp4')}")

            print(f"\n\u6b63在\u6d4b\u8bd5: {filename}")
            success, error_msg = merger.merge_subtitle(video_path, subtitle_path, output_path)

            if success and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"\u2705 \u6210\u529f: {filename}")
                success_count += 1
            else:
                print(f"\u274c \u5931\u8d25: {filename}")
                if error_msg:
                    print(f"   \u9519\u8bef\u4fe1\u606f: {error_msg[:200]}")

        # 测试批量合成
        print(f"\n\u6b63\u5728\u6d4b\u8bd5\u6279\u91cf\u5408\u6210...")
        merger.batch_merge(
            test_env['video_folder'],
            test_env['subtitle_folder'],
            test_env['output_folder']
        )

        # 检\u67e5\u8f93\u51fa\u7ed3\u679c
        output_files = []
        for root, dirs, files in os.walk(test_env['output_folder']):
            for file in files:
                if file.endswith('.mp4'):
                    output_files.append(os.path.join(root, file))

        print(f"\n\u6210\u529f\u521b\u5efa {len(output_files)} \u4e2a\u8f93\u51fa\u6587\u4ef6:")
        for f in output_files:
            print(f"  - {f}")

        print(f"\n" + "="*60)
        print(f"\u6d4b\u8bd5\u7ed3\u679c: {success_count}/{total_tests} \u4e2a\u5355\u4e2a\u5408\u6210\u6d4b\u8bd5\u901a\u8fc7")
        print(f"\u6279\u91cf\u5408\u6210\u521b\u5efa\u4e86 {len(output_files)} \u4e2a\u6587\u4ef6")
        print("="*60)

        return success_count == total_tests

    finally:
        # \u6e05\u7406\u4e34\u65f6\u6587\u4ef6
        print(f"\n\u6b63\u5728\u6e05\u7406\u4e34\u65f6\u6587\u4ef6...")
        shutil.rmtree(test_env['test_dir'], ignore_errors=True)

if __name__ == "__main__":
    print("\u5b57\u5e55\u5408\u6210\u6d4b\u8bd5\u5de5\u5177")
    print("\u8fd9\u4e2a\u6d4b\u8bd5\u5c06\u9a8c\u8bc1FFmpeg\u4fee\u590d\u662f\u5426\u6709\u6548")

    # \u68c0\u67e5FFmpeg\u662f\u5426\u5b89\u88c5
    try:
        result = os.system("ffmpeg -version > nul 2>&1")
        if result != 0:
            print("\u2757 \u672a\u68c0\u6d4b\u5230FFmpeg\uff0c\u8bf7\u5148\u5b89\u88c5FFmpeg")
            sys.exit(1)
    except:
        print("\u2757 \u672a\u68c0\u6d4b\u5230FFmpeg\uff0c\u8bf7\u5148\u5b89\u88c5FFmpeg")
        sys.exit(1)

    # \u8fd0\u884c\u6d4b\u8bd5
    success = test_subtitle_merger()

    if success:
        print("\n\u2705 \u6240\u6709\u6d4b\u8bd5\u5747\u901a\u8fc7\uff01\u4fee\u590d\u6709\u6548")
    else:
        print("\n\u274c \u90e8\u5206\u6d4b\u8bd5\u5931\u8d25\uff0c\u8bf7\u68c0\u67e5\u9519\u8bef\u4fe1\u606f")