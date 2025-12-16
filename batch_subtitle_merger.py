#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量视频字幕合成工具
Batch Video Subtitle Merger Tool
"""

import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import threading
import subprocess
from pathlib import Path
import queue


class SubtitleMerger:
    """视频字幕合成核心类"""

    def __init__(self):
        self.video_folder = ""
        self.subtitle_folder = ""
        self.output_folder = ""
        self.languages = []

    def scan_languages(self, subtitle_folder):
        """扫描字幕文件夹，获取所有语种"""
        languages = []
        try:
            if not os.path.exists(subtitle_folder):
                return languages

            for item in os.listdir(subtitle_folder):
                item_path = os.path.join(subtitle_folder, item)
                if os.path.isdir(item_path):
                    # 检查文件夹内是否有.srt或.str文件
                    files = os.listdir(item_path)
                    subtitle_files = [f for f in files if f.endswith('.srt') or f.endswith('.str')]
                    if subtitle_files:
                        languages.append(item)
        except Exception as e:
            print(f"扫描语种出错: {e}")

        return sorted(languages)

    def get_video_files(self, video_folder):
        """获取视频文件列表"""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        video_files = []

        try:
            for file in os.listdir(video_folder):
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    video_files.append(file)
        except Exception as e:
            print(f"获取视频文件出错: {e}")

        return sorted(video_files)

    def merge_subtitle(self, video_path, subtitle_path, output_path, progress_callback=None):
        """
        使用ffmpeg合并视频和字幕

        Args:
            video_path: 原始视频路径
            subtitle_path: 字幕文件路径
            output_path: 输出视频路径
            progress_callback: 进度回调函数
        """
        try:
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 构建ffmpeg命令
            # 使用硬字幕方式，将字幕烧录到视频中
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f"subtitles='{subtitle_path}'",
                '-c:a', 'copy',  # 音频直接复制
                '-y',  # 覆盖已存在文件
                output_path
            ]

            if progress_callback:
                progress_callback(f"正在处理: {os.path.basename(output_path)}")

            # 执行ffmpeg命令
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'  # 遇到无法解码的字符时用替换字符代替
            )

            if process.returncode == 0:
                if progress_callback:
                    progress_callback(f"✓ 完成: {os.path.basename(output_path)}")
                return True
            else:
                error_msg = process.stderr
                if progress_callback:
                    progress_callback(f"✗ 失败: {os.path.basename(output_path)}\n错误: {error_msg[:200]}")
                return False

        except Exception as e:
            if progress_callback:
                progress_callback(f"✗ 异常: {os.path.basename(output_path)}\n{str(e)}")
            return False

    def batch_merge(self, video_folder, subtitle_folder, output_folder, progress_callback=None):
        """
        批量合成视频字幕

        Args:
            video_folder: 原始视频文件夹
            subtitle_folder: 字幕文件夹
            output_folder: 输出文件夹
            progress_callback: 进度回调函数
        """
        # 获取所有视频文件
        video_files = self.get_video_files(video_folder)
        if not video_files:
            if progress_callback:
                progress_callback("错误: 未找到视频文件")
            return

        # 获取所有语种
        languages = self.scan_languages(subtitle_folder)
        if not languages:
            if progress_callback:
                progress_callback("错误: 未找到语种文件夹")
            return

        total_tasks = len(video_files) * len(languages)
        completed_tasks = 0

        if progress_callback:
            progress_callback(f"开始处理: {len(video_files)} 个视频 × {len(languages)} 种语言 = {total_tasks} 个任务\n")

        # 遍历每个语种
        for lang in languages:
            if progress_callback:
                progress_callback(f"\n=== 处理语种: {lang} ===")

            lang_subtitle_folder = os.path.join(subtitle_folder, lang)
            lang_output_folder = os.path.join(output_folder, lang)

            # 遍历每个视频
            for video_file in video_files:
                video_name = os.path.splitext(video_file)[0]
                video_ext = os.path.splitext(video_file)[1]

                # 构建路径
                video_path = os.path.join(video_folder, video_file)

                # 查找对应的字幕文件 - 支持多种命名模式
                subtitle_file = None
                possible_patterns = [
                    f"{video_name}_{lang}",      # 原始模式: Movie_EN
                    f"{lang}_{video_name}",      # 反转模式: EN_Movie
                    f"{video_name}.{lang}",      # 点分隔模式: Movie.EN
                    lang,                        # 只语言名: EN
                ]

                for pattern in possible_patterns:
                    for ext in ['.srt', '.str']:
                        potential_subtitle = f"{pattern}{ext}"
                        subtitle_path = os.path.join(lang_subtitle_folder, potential_subtitle)
                        if os.path.exists(subtitle_path):
                            subtitle_file = potential_subtitle
                            break
                    if subtitle_file:
                        break

                # 如果上面都没找到，尝试模糊匹配
                if not subtitle_file:
                    for ext in ['.srt', '.str']:
                        # 查找包含语言代码的任意字幕文件
                        for file in os.listdir(lang_subtitle_folder):
                            if file.endswith(ext) and lang in file:
                                subtitle_file = file
                                break
                        if subtitle_file:
                            break

                if not subtitle_file:
                    if progress_callback:
                        progress_callback(f"⚠ 跳过: {video_file} (未找到对应字幕)")
                    completed_tasks += 1
                    continue

                subtitle_path = os.path.join(lang_subtitle_folder, subtitle_file)
                output_file = f"{video_name}_{lang}{video_ext}"
                output_path = os.path.join(lang_output_folder, output_file)

                # 合成视频和字幕
                success = self.merge_subtitle(video_path, subtitle_path, output_path, progress_callback)

                completed_tasks += 1

                if progress_callback:
                    progress_percent = (completed_tasks / total_tasks) * 100
                    progress_callback(f"总进度: {completed_tasks}/{total_tasks} ({progress_percent:.1f}%)\n")

        if progress_callback:
            progress_callback(f"\n{'='*50}\n所有任务完成!\n")


class SubtitleMergerGUI:
    """GUI界面类"""

    def __init__(self, root):
        self.root = root
        self.root.title("批量视频字幕合成工具 - Batch Subtitle Merger")
        self.root.geometry("800x700")

        self.merger = SubtitleMerger()
        self.is_processing = False
        self.message_queue = queue.Queue()

        self.setup_ui()
        self.check_message_queue()

    def setup_ui(self):
        """设置UI界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 标题
        title_label = ttk.Label(main_frame, text="批量视频字幕合成工具", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # 原视频文件夹选择
        row = 1
        ttk.Label(main_frame, text="原视频文件夹:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.video_folder_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.video_folder_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="浏览", command=self.select_video_folder).grid(row=row, column=2, padx=5)

        # 字幕文件夹选择
        row += 1
        ttk.Label(main_frame, text="字幕文件夹:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.subtitle_folder_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.subtitle_folder_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="浏览", command=self.select_subtitle_folder).grid(row=row, column=2, padx=5)

        # 输出文件夹选择
        row += 1
        ttk.Label(main_frame, text="输出文件夹:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.output_folder_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.output_folder_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="浏览", command=self.select_output_folder).grid(row=row, column=2, padx=5)

        # 检测到的语种显示
        row += 1
        ttk.Label(main_frame, text="检测到的语种:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.languages_var = tk.StringVar(value="未检测")
        ttk.Label(main_frame, textvariable=self.languages_var, foreground="blue").grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Button(main_frame, text="刷新", command=self.refresh_languages).grid(row=row, column=2, padx=5)

        # 分隔线
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # 开始按钮
        row += 1
        self.start_button = ttk.Button(main_frame, text="开始批量合成", command=self.start_merge, style="Accent.TButton")
        self.start_button.grid(row=row, column=0, columnspan=3, pady=10, ipadx=20, ipady=10)

        # 进度显示区域
        row += 1
        ttk.Label(main_frame, text="处理日志:").grid(row=row, column=0, sticky=tk.W, pady=5)

        row += 1
        self.log_text = scrolledtext.ScrolledText(main_frame, height=20, width=80, wrap=tk.WORD)
        self.log_text.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(row, weight=1)

        # 状态栏
        row += 1
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

    def select_video_folder(self):
        """选择原视频文件夹"""
        folder = filedialog.askdirectory(title="选择原视频文件夹")
        if folder:
            self.video_folder_var.set(folder)
            self.log_message(f"已选择视频文件夹: {folder}")

    def select_subtitle_folder(self):
        """选择字幕文件夹"""
        folder = filedialog.askdirectory(title="选择字幕文件夹")
        if folder:
            self.subtitle_folder_var.set(folder)
            self.log_message(f"已选择字幕文件夹: {folder}")
            self.refresh_languages()

    def select_output_folder(self):
        """选择输出文件夹"""
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_folder_var.set(folder)
            self.log_message(f"已选择输出文件夹: {folder}")

    def refresh_languages(self):
        """刷新检测到的语种"""
        subtitle_folder = self.subtitle_folder_var.get()
        if not subtitle_folder:
            self.languages_var.set("未选择字幕文件夹")
            return

        languages = self.merger.scan_languages(subtitle_folder)
        if languages:
            self.languages_var.set(", ".join(languages))
            self.log_message(f"检测到 {len(languages)} 种语言: {', '.join(languages)}")
        else:
            self.languages_var.set("未检测到语种")
            self.log_message("未检测到任何语种文件夹")

    def log_message(self, message):
        """记录日志消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.update()

    def check_message_queue(self):
        """检查消息队列并更新UI"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.log_message(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_message_queue)

    def progress_callback(self, message):
        """进度回调函数（从工作线程调用）"""
        self.message_queue.put(message)

    def start_merge(self):
        """开始批量合成"""
        if self.is_processing:
            messagebox.showwarning("警告", "正在处理中，请等待完成")
            return

        # 验证输入
        video_folder = self.video_folder_var.get()
        subtitle_folder = self.subtitle_folder_var.get()
        output_folder = self.output_folder_var.get()

        if not video_folder or not os.path.exists(video_folder):
            messagebox.showerror("错误", "请选择有效的原视频文件夹")
            return

        if not subtitle_folder or not os.path.exists(subtitle_folder):
            messagebox.showerror("错误", "请选择有效的字幕文件夹")
            return

        if not output_folder:
            messagebox.showerror("错误", "请选择输出文件夹")
            return

        # 检查ffmpeg是否安装
        if not self.check_ffmpeg():
            messagebox.showerror("错误", "未检测到ffmpeg，请先安装ffmpeg\n\nmacOS: brew install ffmpeg\nWindows: 下载ffmpeg并添加到系统PATH")
            return

        # 确认开始
        languages = self.merger.scan_languages(subtitle_folder)
        video_files = self.merger.get_video_files(video_folder)

        if not languages:
            messagebox.showerror("错误", "未检测到任何语种文件夹")
            return

        if not video_files:
            messagebox.showerror("错误", "未检测到任何视频文件")
            return

        total_tasks = len(video_files) * len(languages)
        confirm = messagebox.askyesno(
            "确认",
            f"将处理:\n"
            f"- {len(video_files)} 个视频文件\n"
            f"- {len(languages)} 种语言\n"
            f"- 共 {total_tasks} 个任务\n\n"
            f"是否继续?"
        )

        if not confirm:
            return

        # 清空日志
        self.log_text.delete(1.0, tk.END)

        # 在新线程中执行处理
        self.is_processing = True
        self.start_button.config(state='disabled')
        self.status_var.set("处理中...")

        thread = threading.Thread(target=self.merge_worker, args=(video_folder, subtitle_folder, output_folder))
        thread.daemon = True
        thread.start()

    def check_ffmpeg(self):
        """检查ffmpeg是否可用"""
        try:
            subprocess.run(
                ['ffmpeg', '-version'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                check=True,
                encoding='utf-8',
                errors='replace'
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def merge_worker(self, video_folder, subtitle_folder, output_folder):
        """工作线程执行合成任务"""
        try:
            self.merger.batch_merge(video_folder, subtitle_folder, output_folder, self.progress_callback)
            self.message_queue.put("\n✓ 所有任务已完成!")
            self.status_var.set("完成")
            messagebox.showinfo("完成", "所有视频字幕合成已完成!")
        except Exception as e:
            self.message_queue.put(f"\n✗ 发生错误: {str(e)}")
            self.status_var.set("错误")
            messagebox.showerror("错误", f"处理过程中发生错误:\n{str(e)}")
        finally:
            self.is_processing = False
            self.start_button.config(state='normal')


def main():
    """主函数"""
    root = tk.Tk()
    app = SubtitleMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
