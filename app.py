#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量视频字幕合成工具 - Web版本后端
Batch Video Subtitle Merger Tool - Web Backend
"""

import os
import subprocess
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import time
from font_config import (
    get_font_for_language,
    build_font_family_string,
    get_all_font_files,
    is_font_file_path,
    normalize_font_path,
    get_available_font_for_language
)
from subtitle_encoding import (
    detect_file_encoding,
    is_utf8,
    convert_subtitle_encoding
)

app = Flask(__name__)
CORS(app)

# 全局变量存储处理状态
processing_status = {
    'is_processing': False,
    'current_task': '',
    'progress': 0,
    'total': 0,
    'logs': [],
    'completed': False,
    'error': None,
    'stop_requested': False
}

# 存储当前ffmpeg进程
current_process = None


class SubtitleMerger:
    """视频字幕合成核心类"""

    def scan_languages(self, subtitle_folder):
        """扫描字幕文件夹，获取所有语种"""
        languages = []
        try:
            if not os.path.exists(subtitle_folder):
                return languages

            for item in os.listdir(subtitle_folder):
                item_path = os.path.join(subtitle_folder, item)
                if os.path.isdir(item_path):
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

    def merge_subtitle(self, video_path, subtitle_path, output_path, use_gpu=False, gpu_type='auto', subtitle_style=None, language_code=None):
        """使用ffmpeg合并视频和字幕

        Args:
            video_path: 视频文件路径
            subtitle_path: 字幕文件路径
            output_path: 输出文件路径
            use_gpu: 是否使用GPU加速
            gpu_type: GPU类型 ('auto', 'nvidia', 'amd', 'intel', 'apple')
            subtitle_style: 字幕样式配置字典 (可选)
                - font_size: 字体大小 (默认: 原样式)
                - margin_v: 垂直边距 (默认: 原样式)
                - alignment: 对齐方式 1-9 (默认: 2 底部居中)
                - font_name: 字体名称或字体文件路径 (可选)
                - font_file: 字体文件路径 (可选，优先于font_name)
                - outline: 轮廓粗细 (可选)
                - shadow: 阴影深度 (可选)
                - auto_font: 是否启用自动字体映射 (默认: True)
            language_code: 语种代码，用于自动字体映射 (如 'AR', 'CN')
        """
        global current_process

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 构建ffmpeg命令
            cmd = ['ffmpeg']

            # 添加硬件加速参数
            if use_gpu:
                if gpu_type == 'nvidia' or (gpu_type == 'auto' and self._has_nvidia_gpu()):
                    # NVIDIA GPU (CUDA)
                    # subtitles滤镜需要CPU内存数据，不要强制输出CUDA格式
                    cmd.extend(['-hwaccel', 'cuda'])
                elif gpu_type == 'apple' or (gpu_type == 'auto' and self._is_apple_silicon()):
                    # Apple Silicon (VideoToolbox)
                    cmd.extend(['-hwaccel', 'videotoolbox'])
                elif gpu_type == 'amd':
                    # AMD GPU (AMF on Windows)
                    cmd.extend(['-hwaccel', 'dxva2'])
                elif gpu_type == 'intel':
                    # Intel GPU (QSV)
                    cmd.extend(['-hwaccel', 'qsv'])

            # 输入文件
            cmd.extend(['-i', video_path])

            # 字幕滤镜 - 需要处理Windows路径：替换反斜杠为正斜杠，并转义冒号
            filter_subtitle_path = subtitle_path.replace('\\', '/').replace(':', '\\:')

            # 构建字幕样式参数
            # 添加字符编码支持，确保FFmpeg正确解析UTF-8字幕
            # 初始化滤镜参数列表
            subtitle_filter_parts = [f"subtitles='{filter_subtitle_path}':charenc=UTF-8"]

            # 用于跟踪是否已添加 fontsdir
            fontsdir_added = False

            # 初始化样式参数列表（即使没有自定义样式也要设置默认值）
            style_params = []

            if subtitle_style:
                # 字体处理 - 支持自动映射、字体文件路径和字体名称
                font_applied = False
                auto_font = subtitle_style.get('auto_font', True)

                # 优先级1: 明确指定的字体文件路径
                if subtitle_style.get('font_file'):
                    font_file = subtitle_style['font_file']
                    if os.path.exists(font_file):
                        normalized_font = normalize_font_path(font_file)
                        subtitle_filter_parts.append(f"fontsdir='{os.path.dirname(normalized_font)}'")
                        style_params.append(f"FontName={os.path.basename(font_file)}")
                        font_applied = True
                    else:
                        self.log(f"⚠️ 字体文件不存在: {font_file}")

                # 优先级2: 用户指定的字体名称
                if not font_applied and subtitle_style.get('font_name'):
                    font_name = subtitle_style['font_name']

                    # 判断是否为文件路径
                    if is_font_file_path(font_name):
                        if os.path.exists(font_name):
                            normalized_font = normalize_font_path(font_name)
                            subtitle_filter_parts.append(f"fontsdir='{os.path.dirname(normalized_font)}'")
                            style_params.append(f"FontName={os.path.basename(font_name)}")
                            font_applied = True
                        else:
                            self.log(f"⚠️ 字体文件不存在: {font_name}")
                    else:
                        # 字体名称
                        style_params.append(f"FontName={font_name}")
                        font_applied = True

                # 优先级3: 自动语种字体映射（启用且有语种代码）
                if not font_applied and auto_font and language_code:
                    # 获取系统中实际可用的字体
                    font_type, font_value = get_available_font_for_language(language_code)

                    if font_type == 'file':
                        # 使用字体文件
                        if os.path.exists(font_value):
                            # 设置 fontsdir 参数（添加到主滤镜参数中）
                            font_dir = os.path.dirname(font_value)
                            normalized_dir = normalize_font_path(font_dir)

                            if not fontsdir_added:
                                subtitle_filter_parts[0] += f":fontsdir='{normalized_dir}'"
                                fontsdir_added = True

                            # 根据字体文件名确定 FontName
                            # 测试验证：使用标准字体家族名称最可靠
                            font_file_name = os.path.basename(font_value)

                            # 字体文件名到标准字体名的映射
                            font_name_map = {
                                'NotoSansArabic': 'Noto Sans Arabic',
                                'NotoSansCJKsc': 'Noto Sans CJK SC',
                                'NotoSansCJKtc': 'Noto Sans CJK TC',
                                'NotoSansCJKjp': 'Noto Sans CJK JP',
                                'NotoSansCJKkr': 'Noto Sans CJK KR',
                                'NotoSansThai': 'Noto Sans Thai',
                                'NotoSansMyanmar': 'Noto Sans Myanmar',
                                'NotoSansHebrew': 'Noto Sans Hebrew',
                                'NotoSansDevanagari': 'Noto Sans Devanagari',
                            }

                            # 查找匹配的字体名称
                            font_display_name = None
                            for key, value in font_name_map.items():
                                if key.lower() in font_file_name.lower():
                                    font_display_name = value
                                    break

                            if font_display_name is None:
                                # 如果没有匹配，使用文件名（去掉扩展名和variant）
                                font_basename = os.path.splitext(font_file_name)[0]
                                font_basename = font_basename.split('-')[0]
                                font_display_name = font_basename

                            style_params.append(f"FontName={font_display_name}")

                            self.log(f"🎨 为 {language_code} 使用字体: {font_display_name}")
                            self.log(f"   字体文件: {font_file_name}")
                            font_applied = True
                        else:
                            self.log(f"⚠️ 字体文件不存在: {font_value}")
                    elif font_type == 'name':
                        # 使用系统字体名称
                        style_params.append(f"FontName={font_value}")
                        self.log(f"🎨 为 {language_code} 使用系统字体: {font_value}")

                        # 如果是Arial回退，说明系统没有该语种的专用字体
                        if font_value == 'Arial':
                            recommended = get_font_for_language(language_code)[0]
                            self.log(f"⚠️ 系统未安装 {recommended}，使用 Arial 回退（可能显示为方框）")
                            self.log(f"💡 建议: 下载 {recommended} 字体并放入 fonts/ 目录")

                        font_applied = True

                # 其他样式参数
                if subtitle_style.get('font_size'):
                    style_params.append(f"FontSize={subtitle_style['font_size']}")
                if subtitle_style.get('margin_v'):
                    style_params.append(f"MarginV={subtitle_style['margin_v']}")
                if subtitle_style.get('alignment'):
                    style_params.append(f"Alignment={subtitle_style['alignment']}")

            # 黑边和阴影参数 - 始终显式设置以覆盖ASS文件内部样式
            # 如果用户设置了值则使用用户的值，否则默认为0（无黑边/无阴影）
            if subtitle_style and subtitle_style.get('outline') is not None:
                style_params.append(f"Outline={subtitle_style['outline']}")
            else:
                style_params.append("Outline=0")

            if subtitle_style and subtitle_style.get('shadow') is not None:
                style_params.append(f"Shadow={subtitle_style['shadow']}")
            else:
                style_params.append("Shadow=0")

            # 应用样式参数
            if style_params:
                force_style = ','.join(style_params)
                subtitle_filter_parts.append(f"force_style='{force_style}'")

            subtitle_filter = ':'.join(subtitle_filter_parts)

            cmd.extend(['-vf', subtitle_filter])

            # 视频编码器设置
            video_codec = 'libx264'
            if use_gpu:
                if gpu_type == 'nvidia' or (gpu_type == 'auto' and self._has_nvidia_gpu()):
                    video_codec = 'h264_nvenc'
                    # NVENC 参数优化: 恒定质量模式 (p4=medium preset, qp=23 similar to crf 23)
                    cmd.extend(['-preset', 'p4', '-rc', 'constqp', '-qp', '23'])
                elif gpu_type == 'apple' or (gpu_type == 'auto' and self._is_apple_silicon()):
                    video_codec = 'h264_videotoolbox'
                    # VideoToolbox 质量参数 (0-100, 65 is roughly high quality)
                    cmd.extend(['-q:v', '65'])
                elif gpu_type == 'intel':
                    video_codec = 'h264_qsv'
                    cmd.extend(['-global_quality', '23'])
                elif gpu_type == 'amd':
                    video_codec = 'h264_amf'
                    # AMF 质量参数
                    cmd.extend(['-rc', 'cqp', '-qp_i', '23', '-qp_p', '23', '-qp_b', '23'])

            cmd.extend(['-c:v', video_codec])

            # 音频直接复制
            cmd.extend(['-c:a', 'copy'])

            # 覆盖输出文件
            cmd.extend(['-y', output_path])

            # 打印完整命令以便调试
            # print("Executing:", " ".join(cmd)) 

            # 使用Popen以便可以终止进程
            current_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'  # 遇到无法解码的字符时用替换字符代替
            )

            # 等待进程完成
            stdout, stderr = current_process.communicate()
            returncode = current_process.returncode
            current_process = None

            return returncode == 0, stderr

        except Exception as e:
            current_process = None
            return False, str(e)

    def _has_nvidia_gpu(self):
        """检测是否有NVIDIA GPU"""
        try:
            result = subprocess.run(
                ['nvidia-smi'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace'
            )
            return result.returncode == 0
        except:
            return False

    def _is_apple_silicon(self):
        """检测是否为Apple Silicon"""
        try:
            import platform
            return platform.system() == 'Darwin' and platform.machine() == 'arm64'
        except:
            return False

    def batch_merge(self, video_folder, subtitle_folder, output_folder, use_gpu=False, gpu_type='auto', subtitle_style=None):
        """批量合成视频字幕

        Args:
            video_folder: 视频文件夹
            subtitle_folder: 字幕文件夹
            output_folder: 输出文件夹
            use_gpu: 是否使用GPU加速
            gpu_type: GPU类型
            subtitle_style: 字幕样式配置
        """
        global processing_status

        processing_status['is_processing'] = True
        processing_status['logs'] = []
        processing_status['completed'] = False
        processing_status['error'] = None
        processing_status['progress'] = 0
        processing_status['stop_requested'] = False

        # 记录加速模式和字幕样式
        if use_gpu:
            self.log(f"🚀 已启用GPU加速 (类型: {gpu_type})")
        else:
            self.log("💻 使用CPU处理模式")

        if subtitle_style:
            style_info = []
            if subtitle_style.get('font_size'):
                style_info.append(f"字体大小={subtitle_style['font_size']}")
            if subtitle_style.get('margin_v'):
                style_info.append(f"底部边距={subtitle_style['margin_v']}")
            if subtitle_style.get('alignment'):
                alignment_map = {1: '左下', 2: '底部居中', 3: '右下', 4: '左中', 5: '居中', 6: '右中', 7: '左上', 8: '顶部居中', 9: '右上'}
                style_info.append(f"位置={alignment_map.get(subtitle_style['alignment'], subtitle_style['alignment'])}")
            if style_info:
                self.log(f"🎨 字幕样式: {', '.join(style_info)}")

        try:
            # 获取所有视频文件
            video_files = self.get_video_files(video_folder)
            if not video_files:
                processing_status['error'] = "未找到视频文件"
                return

            # 获取所有语种
            languages = self.scan_languages(subtitle_folder)
            if not languages:
                processing_status['error'] = "未找到语种文件夹"
                return

            total_tasks = len(video_files) * len(languages)
            processing_status['total'] = total_tasks

            self.log(f"开始处理: {len(video_files)} 个视频 × {len(languages)} 种语言 = {total_tasks} 个任务")

            completed_tasks = 0

            # 遍历每个语种
            for lang in languages:
                # 检查是否请求停止
                if processing_status['stop_requested']:
                    self.log("\n⚠ 用户请求终止任务")
                    break

                self.log(f"\n=== 处理语种: {lang} ===")

                lang_subtitle_folder = os.path.join(subtitle_folder, lang)
                lang_output_folder = os.path.join(output_folder, lang)

                # 遍历每个视频
                for video_file in video_files:
                    # 检查是否请求停止
                    if processing_status['stop_requested']:
                        self.log("\n⚠ 用户请求终止任务")
                        break

                    video_name = os.path.splitext(video_file)[0]
                    video_ext = os.path.splitext(video_file)[1]

                    # 构建路径
                    video_path = os.path.join(video_folder, video_file)

                    # 查找对应的字幕文件
                    subtitle_file = None
                    for ext in ['.srt', '.str']:
                        potential_subtitle = f"{video_name}_{lang}{ext}"
                        subtitle_path = os.path.join(lang_subtitle_folder, potential_subtitle)
                        if os.path.exists(subtitle_path):
                            subtitle_file = potential_subtitle
                            break

                    if not subtitle_file:
                        self.log(f"⚠ 跳过: {video_file} (未找到对应字幕)")
                        completed_tasks += 1
                        processing_status['progress'] = completed_tasks
                        continue

                    subtitle_path = os.path.join(lang_subtitle_folder, subtitle_file)
                    output_file = f"{video_name}_{lang}{video_ext}"
                    output_path = os.path.join(lang_output_folder, output_file)

                    # 更新当前任务
                    processing_status['current_task'] = f"{video_file} -> {lang}"
                    self.log(f"正在处理: {output_file}")

                    # 检查并转换字幕编码为 UTF-8
                    if not is_utf8(subtitle_path):
                        self.log(f"⚠️ 检测到非UTF-8编码字幕，正在自动转换...")
                        encoding_result = detect_file_encoding(subtitle_path)
                        if encoding_result:
                            detected_encoding = encoding_result.get('encoding', 'unknown')
                            confidence = encoding_result.get('confidence', 0)
                            self.log(f"   检测到编码: {detected_encoding} (置信度: {confidence:.2f})")

                        conv_success, conv_message = convert_subtitle_encoding(subtitle_path, lang)
                        if conv_success:
                            self.log(f"✅ {conv_message}")
                        else:
                            self.log(f"⚠️ 编码转换失败: {conv_message}")
                            self.log(f"   将尝试使用原始编码处理...")

                    # 合成视频和字幕 - 传递语种代码用于自动字体映射
                    success, error_msg = self.merge_subtitle(video_path, subtitle_path, output_path, use_gpu, gpu_type, subtitle_style, language_code=lang)

                    if success:
                        self.log(f"✓ 完成: {output_file}")
                    else:
                        # 检查是否因为终止导致失败
                        if processing_status['stop_requested']:
                            self.log(f"⚠ 已终止: {output_file}")
                        else:
                            self.log(f"✗ 失败: {output_file}")
                            if error_msg:
                                # 显示更多错误信息（取最后2000字符），因为ffmpeg错误通常在最后
                                self.log(f"  错误信息: ...{error_msg[-2000:]}")

                    completed_tasks += 1
                    processing_status['progress'] = completed_tasks

                    progress_percent = (completed_tasks / total_tasks) * 100
                    self.log(f"总进度: {completed_tasks}/{total_tasks} ({progress_percent:.1f}%)")

            if processing_status['stop_requested']:
                self.log(f"\n{'='*50}\n任务已被终止!")
                processing_status['error'] = "任务已被用户终止"
            else:
                self.log(f"\n{'='*50}\n所有任务完成!")
                processing_status['completed'] = True

        except Exception as e:
            processing_status['error'] = str(e)
            self.log(f"✗ 发生错误: {str(e)}")

        finally:
            processing_status['is_processing'] = False

    def log(self, message):
        """添加日志"""
        processing_status['logs'].append(message)


merger = SubtitleMerger()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/scan_languages', methods=['POST'])
def scan_languages():
    """扫描语种"""
    data = request.json
    subtitle_folder = data.get('subtitle_folder', '')

    if not subtitle_folder or not os.path.exists(subtitle_folder):
        return jsonify({'success': False, 'error': '字幕文件夹不存在'})

    languages = merger.scan_languages(subtitle_folder)
    return jsonify({'success': True, 'languages': languages})


@app.route('/api/validate_folder', methods=['POST'])
def validate_folder():
    """验证单个文件夹"""
    data = request.json
    folder_path = data.get('folder_path', '')
    folder_type = data.get('folder_type', 'video')  # video, subtitle, output

    result = {
        'valid': False,
        'exists': False,
        'is_dir': False,
        'count': 0,
        'message': ''
    }

    if not folder_path:
        result['message'] = '路径不能为空'
        return jsonify(result)

    # 检查路径是否存在
    result['exists'] = os.path.exists(folder_path)
    if not result['exists']:
        result['message'] = '路径不存在'
        return jsonify(result)

    # 检查是否为文件夹
    result['is_dir'] = os.path.isdir(folder_path)
    if not result['is_dir']:
        result['message'] = '该路径不是文件夹'
        return jsonify(result)

    # 根据类型检查内容
    if folder_type == 'video':
        video_files = merger.get_video_files(folder_path)
        result['count'] = len(video_files)
        if result['count'] > 0:
            result['valid'] = True
            result['message'] = f'找到 {result["count"]} 个视频文件'
        else:
            result['message'] = '未找到视频文件'

    elif folder_type == 'subtitle':
        languages = merger.scan_languages(folder_path)
        result['count'] = len(languages)
        if result['count'] > 0:
            result['valid'] = True
            result['message'] = f'找到 {result["count"]} 种语言'
            result['languages'] = languages
        else:
            result['message'] = '未找到语种文件夹'

    elif folder_type == 'output':
        # 输出文件夹只需要存在且可写即可
        result['valid'] = True
        result['message'] = '输出路径有效'

    return jsonify(result)


@app.route('/api/start_merge', methods=['POST'])
def start_merge():
    """开始批量合成"""
    global processing_status

    if processing_status['is_processing']:
        return jsonify({'success': False, 'error': '正在处理中，请等待'})

    data = request.json
    video_folder = data.get('video_folder', '')
    subtitle_folder = data.get('subtitle_folder', '')
    output_folder = data.get('output_folder', '')
    use_gpu = data.get('use_gpu', False)
    gpu_type = data.get('gpu_type', 'auto')

    # 获取字幕样式配置
    subtitle_style = None
    if data.get('subtitle_style'):
        style_data = data['subtitle_style']
        subtitle_style = {}
        if style_data.get('font_size'):
            subtitle_style['font_size'] = int(style_data['font_size'])
        if style_data.get('margin_v'):
            subtitle_style['margin_v'] = int(style_data['margin_v'])
        if style_data.get('alignment'):
            subtitle_style['alignment'] = int(style_data['alignment'])
        if style_data.get('font_name'):
            subtitle_style['font_name'] = style_data['font_name']
        if style_data.get('outline'):
            subtitle_style['outline'] = int(style_data['outline'])
        if style_data.get('shadow'):
            subtitle_style['shadow'] = int(style_data['shadow'])

    # 验证输入
    if not all([video_folder, subtitle_folder, output_folder]):
        return jsonify({'success': False, 'error': '请填写所有文件夹路径'})

    if not os.path.exists(video_folder):
        return jsonify({'success': False, 'error': '原视频文件夹不存在'})

    if not os.path.exists(subtitle_folder):
        return jsonify({'success': False, 'error': '字幕文件夹不存在'})

    # 检查ffmpeg
    try:
        subprocess.run(
            ['ffmpeg', '-version'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            check=True,
            encoding='utf-8',
            errors='replace'
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return jsonify({'success': False, 'error': '未检测到ffmpeg，请先安装'})

    # 在新线程中执行处理
    thread = threading.Thread(
        target=merger.batch_merge,
        args=(video_folder, subtitle_folder, output_folder, use_gpu, gpu_type, subtitle_style)
    )
    thread.daemon = True
    thread.start()

    return jsonify({'success': True})


@app.route('/api/detect_gpu', methods=['GET'])
def detect_gpu():
    """检测可用的GPU"""
    result = {
        'has_gpu': False,
        'gpu_types': [],
        'recommended': 'cpu'
    }

    # 检测 NVIDIA GPU
    if merger._has_nvidia_gpu():
        result['has_gpu'] = True
        result['gpu_types'].append({'value': 'nvidia', 'label': 'NVIDIA GPU (CUDA)', 'icon': '🎮'})
        result['recommended'] = 'nvidia'

    # 检测 Apple Silicon
    if merger._is_apple_silicon():
        result['has_gpu'] = True
        result['gpu_types'].append({'value': 'apple', 'label': 'Apple Silicon (VideoToolbox)', 'icon': '🍎'})
        result['recommended'] = 'apple'

    # 其他GPU选项（用户可手动选择）
    result['gpu_types'].extend([
        {'value': 'amd', 'label': 'AMD GPU (VAAPI)', 'icon': '🔴'},
        {'value': 'intel', 'label': 'Intel GPU (QSV)', 'icon': '🔵'}
    ])

    # 自动检测选项
    result['gpu_types'].insert(0, {'value': 'auto', 'label': '自动检测', 'icon': '✨'})

    return jsonify(result)


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取处理状态"""
    return jsonify(processing_status)


@app.route('/api/stop', methods=['POST'])
def stop_processing():
    """停止处理"""
    global processing_status, current_process

    if not processing_status['is_processing']:
        return jsonify({'success': False, 'error': '当前没有正在运行的任务'})

    # 设置停止标志
    processing_status['stop_requested'] = True

    # 如果有正在运行的ffmpeg进程，终止它
    if current_process:
        try:
            current_process.terminate()
            current_process.wait(timeout=5)
        except Exception as e:
            # 如果terminate失败，尝试强制kill
            try:
                current_process.kill()
            except:
                pass

    return jsonify({'success': True, 'message': '正在终止任务...'})


@app.route('/api/font_files', methods=['GET'])
def get_font_files():
    """获取fonts目录中的字体文件列表"""
    try:
        font_files = get_all_font_files()
        return jsonify({
            'success': True,
            'fonts': font_files,
            'count': len(font_files)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/font_recommendation', methods=['POST'])
def get_font_recommendation():
    """根据语种代码获取推荐字体"""
    data = request.json
    language_code = data.get('language_code', '')

    if not language_code:
        return jsonify({'success': False, 'error': '缺少语种代码'})

    try:
        recommended_fonts = get_font_for_language(language_code)
        return jsonify({
            'success': True,
            'language': language_code,
            'fonts': recommended_fonts[:5]  # 返回前5个推荐字体
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("批量视频字幕合成工具 - Web版本")
    print("="*60)
    print("\n请在浏览器中打开: http://localhost:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
