#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量视频字幕合成工具 - 环境配置脚本
一键配置所有依赖环境
"""

import os
import sys
import subprocess
import platform
import shutil

class EnvironmentSetup:
    """环境配置器"""

    def __init__(self):
        self.system = platform.system()
        self.python_version = sys.version_info
        self.errors = []
        self.warnings = []

    def print_header(self):
        """打印标题"""
        print("\n" + "="*60)
        print("批量视频字幕合成工具 - 环境配置器")
        print("Environment Setup for Batch Subtitle Merger")
        print("="*60 + "\n")

    def print_step(self, step, message):
        """打印步骤信息"""
        print(f"[{step}] {message}")

    def print_success(self, message):
        """打印成功信息"""
        print(f"✓ {message}")

    def print_error(self, message):
        """打印错误信息"""
        print(f"✗ {message}")
        self.errors.append(message)

    def print_warning(self, message):
        """打印警告信息"""
        print(f"⚠ {message}")
        self.warnings.append(message)

    def check_python_version(self):
        """检查Python版本"""
        self.print_step("1/5", "检查Python版本...")

        if self.python_version >= (3, 7):
            self.print_success(f"Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro} ✓")
            return True
        else:
            self.print_error(f"Python版本过低: {self.python_version.major}.{self.python_version.minor}")
            self.print_error("需要Python 3.7或更高版本")
            return False

    def check_pip(self):
        """检查pip是否可用"""
        self.print_step("2/5", "检查pip包管理器...")

        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', '--version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                pip_version = result.stdout.strip()
                self.print_success(f"pip可用: {pip_version}")
                return True
            else:
                self.print_error("pip不可用")
                return False

        except Exception as e:
            self.print_error(f"pip检查失败: {str(e)}")
            return False

    def install_python_packages(self):
        """安装Python依赖包"""
        self.print_step("3/5", "安装Python依赖包...")

        requirements_file = 'requirements.txt'

        if not os.path.exists(requirements_file):
            self.print_error(f"未找到{requirements_file}文件")
            return False

        try:
            print("\n正在安装依赖包，请稍候...")
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', requirements_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                self.print_success("Python依赖包安装完成")
                print(result.stdout)
                return True
            else:
                self.print_error("依赖包安装失败")
                print(result.stderr)
                return False

        except Exception as e:
            self.print_error(f"安装过程出错: {str(e)}")
            return False

    def check_ffmpeg(self):
        """检查FFmpeg是否安装"""
        self.print_step("4/5", "检查FFmpeg...")

        ffmpeg_path = shutil.which('ffmpeg')

        if ffmpeg_path:
            try:
                result = subprocess.run(
                    ['ffmpeg', '-version'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                if result.returncode == 0:
                    # 提取版本信息
                    version_line = result.stdout.split('\n')[0]
                    self.print_success(f"FFmpeg已安装: {version_line}")

                    # 检查硬件加速支持
                    self.check_ffmpeg_hwaccel()
                    return True

            except Exception as e:
                self.print_warning(f"FFmpeg版本检查失败: {str(e)}")

        self.print_warning("未检测到FFmpeg")
        self.print_install_ffmpeg_guide()
        return False

    def check_ffmpeg_hwaccel(self):
        """检查FFmpeg硬件加速支持"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-hwaccels'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                hwaccels = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                if hwaccels:
                    print(f"  支持的硬件加速: {', '.join(hwaccels)}")

        except Exception:
            pass

    def print_install_ffmpeg_guide(self):
        """打印FFmpeg安装指南"""
        print("\n" + "-"*60)
        print("FFmpeg安装指南:")
        print("-"*60)

        if self.system == 'Darwin':  # macOS
            print("macOS系统安装方法:")
            print("  1. 使用Homebrew (推荐):")
            print("     brew install ffmpeg")
            print("\n  2. 或从官网下载:")
            print("     https://ffmpeg.org/download.html")

        elif self.system == 'Linux':
            print("Linux系统安装方法:")
            print("  Ubuntu/Debian:")
            print("     sudo apt-get update")
            print("     sudo apt-get install ffmpeg")
            print("\n  CentOS/RHEL:")
            print("     sudo yum install ffmpeg")
            print("\n  Arch Linux:")
            print("     sudo pacman -S ffmpeg")

        elif self.system == 'Windows':
            print("Windows系统安装方法:")
            print("  1. 从官网下载:")
            print("     https://ffmpeg.org/download.html")
            print("\n  2. 解压后将bin目录添加到系统PATH")
            print("\n  3. 或使用Chocolatey:")
            print("     choco install ffmpeg")

        print("-"*60 + "\n")

    def verify_installation(self):
        """验证安装结果"""
        self.print_step("5/5", "验证安装...")

        # 验证Python包
        try:
            import flask
            import flask_cors
            self.print_success("Flask和Flask-CORS导入成功")
        except ImportError as e:
            self.print_error(f"Python包导入失败: {str(e)}")
            return False

        # 检查项目文件
        required_files = ['app.py', 'templates/index.html', 'requirements.txt']
        missing_files = []

        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)

        if missing_files:
            self.print_warning(f"缺少项目文件: {', '.join(missing_files)}")
        else:
            self.print_success("所有项目文件完整")

        return True

    def print_summary(self):
        """打印配置摘要"""
        print("\n" + "="*60)
        print("配置摘要")
        print("="*60)

        if not self.errors:
            print("\n✓ 环境配置成功!")
            print("\n启动应用:")
            print("  python3 app.py")
            print("\n然后在浏览器中访问:")
            print("  http://localhost:5000")

            if self.warnings:
                print("\n注意事项:")
                for warning in self.warnings:
                    print(f"  • {warning}")

        else:
            print("\n✗ 配置过程中遇到问题:")
            for error in self.errors:
                print(f"  • {error}")

            if self.warnings:
                print("\n警告:")
                for warning in self.warnings:
                    print(f"  • {warning}")

        print("\n" + "="*60 + "\n")

    def run(self):
        """运行配置流程"""
        self.print_header()

        # 系统信息
        print(f"操作系统: {self.system}")
        print(f"Python版本: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print()

        # 执行配置步骤
        if not self.check_python_version():
            self.print_summary()
            return False

        if not self.check_pip():
            self.print_summary()
            return False

        self.install_python_packages()
        self.check_ffmpeg()
        self.verify_installation()

        # 打印摘要
        self.print_summary()

        return len(self.errors) == 0


def main():
    """主函数"""
    setup = EnvironmentSetup()
    success = setup.run()

    # 返回退出码
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
