#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字幕编码检测和转换模块
Subtitle Encoding Detection and Conversion Module
"""

import os
import chardet
import codecs


# 常见字幕编码映射
SUBTITLE_ENCODINGS = {
    'AR': ['windows-1256', 'iso-8859-6', 'utf-8'],  # 阿拉伯语
    'FA': ['windows-1256', 'utf-8'],  # 波斯语
    'CN': ['gbk', 'gb2312', 'gb18030', 'utf-8'],  # 简体中文
    'TW': ['big5', 'utf-8'],  # 繁体中文
    'JP': ['shift_jis', 'euc-jp', 'iso-2022-jp', 'utf-8'],  # 日语
    'KR': ['euc-kr', 'cp949', 'utf-8'],  # 韩语
    'TH': ['windows-874', 'tis-620', 'utf-8'],  # 泰语
    'HE': ['windows-1255', 'iso-8859-8', 'utf-8'],  # 希伯来语
    'RU': ['windows-1251', 'koi8-r', 'utf-8'],  # 俄语
    'EL': ['windows-1253', 'iso-8859-7', 'utf-8'],  # 希腊语
    'TR': ['windows-1254', 'iso-8859-9', 'utf-8'],  # 土耳其语
}


def detect_file_encoding(file_path):
    """
    检测文件编码

    Args:
        file_path: 文件路径

    Returns:
        dict: {'encoding': 编码名称, 'confidence': 置信度, 'language': 语言}
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result
    except Exception as e:
        print(f"编码检测失败: {e}")
        return None


def is_utf8(file_path):
    """
    检查文件是否为 UTF-8 编码

    Args:
        file_path: 文件路径

    Returns:
        bool: 是否为 UTF-8
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False


def convert_to_utf8(input_path, output_path=None, source_encoding=None):
    """
    将字幕文件转换为 UTF-8 编码

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（默认覆盖原文件）
        source_encoding: 源编码（如果为None则自动检测）

    Returns:
        tuple: (success: bool, encoding: str, message: str)
    """
    if output_path is None:
        output_path = input_path

    try:
        # 检测源编码
        if source_encoding is None:
            result = detect_file_encoding(input_path)
            if result:
                source_encoding = result['encoding']
                confidence = result.get('confidence', 0)

                # 如果检测置信度低，尝试常见编码
                if confidence < 0.7:
                    print(f"⚠️ 编码检测置信度较低 ({confidence:.2f}), 将尝试多种编码")
            else:
                return False, None, "编码检测失败"

        # 如果已经是 UTF-8，直接返回
        if source_encoding and source_encoding.lower() in ['utf-8', 'utf8', 'ascii']:
            if is_utf8(input_path):
                return True, 'utf-8', "文件已经是UTF-8编码"

        # 读取原始内容
        content = None
        tried_encodings = []

        # 首先尝试检测到的编码
        if source_encoding:
            try:
                with open(input_path, 'r', encoding=source_encoding) as f:
                    content = f.read()
                tried_encodings.append(source_encoding)
            except (UnicodeDecodeError, LookupError):
                pass

        # 如果失败，尝试常见编码
        if content is None:
            common_encodings = [
                'utf-8',
                'utf-8-sig',  # UTF-8 with BOM
                'windows-1256',  # 阿拉伯语
                'windows-1252',  # 西欧语言
                'gbk',  # 中文
                'gb2312',
                'big5',  # 繁体中文
                'shift_jis',  # 日语
                'euc-kr',  # 韩语
                'windows-1251',  # 俄语
                'iso-8859-1',  # Latin-1
            ]

            for encoding in common_encodings:
                if encoding not in tried_encodings:
                    try:
                        with open(input_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        source_encoding = encoding
                        break
                    except (UnicodeDecodeError, LookupError):
                        tried_encodings.append(encoding)

        if content is None:
            return False, None, f"无法读取文件，尝试了编码: {', '.join(tried_encodings)}"

        # 写入 UTF-8 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True, source_encoding, f"成功转换 {source_encoding} -> UTF-8"

    except Exception as e:
        return False, None, f"转换失败: {str(e)}"


def convert_subtitle_encoding(file_path, language_code=None, backup=True):
    """
    智能转换字幕文件编码为 UTF-8

    Args:
        file_path: 字幕文件路径
        language_code: 语种代码（用于优先尝试对应编码）
        backup: 是否备份原文件

    Returns:
        tuple: (success: bool, message: str)
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return False, "文件不存在"

    # 检查是否已经是 UTF-8
    if is_utf8(file_path):
        return True, "文件已经是UTF-8编码，无需转换"

    # 备份原文件
    if backup:
        backup_path = file_path + '.bak'
        try:
            import shutil
            shutil.copy2(file_path, backup_path)
        except Exception as e:
            return False, f"备份失败: {e}"

    # 尝试转换
    success, source_encoding, message = convert_to_utf8(file_path)

    if success:
        return True, f"✅ {message}"
    else:
        # 恢复备份
        if backup and os.path.exists(backup_path):
            try:
                import shutil
                shutil.copy2(backup_path, file_path)
                os.remove(backup_path)
            except:
                pass
        return False, f"❌ {message}"


def batch_convert_subtitles(subtitle_folder, language_code=None):
    """
    批量转换字幕文件夹中的所有字幕为 UTF-8

    Args:
        subtitle_folder: 字幕文件夹路径
        language_code: 语种代码

    Returns:
        dict: 转换结果统计
    """
    results = {
        'total': 0,
        'success': 0,
        'already_utf8': 0,
        'failed': 0,
        'details': []
    }

    if not os.path.exists(subtitle_folder):
        return results

    # 遍历所有 .srt 和 .str 文件
    for root, dirs, files in os.walk(subtitle_folder):
        for file in files:
            if file.endswith('.srt') or file.endswith('.str'):
                file_path = os.path.join(root, file)
                results['total'] += 1

                success, message = convert_subtitle_encoding(file_path, language_code)

                if success:
                    if "已经是UTF-8" in message:
                        results['already_utf8'] += 1
                    else:
                        results['success'] += 1
                else:
                    results['failed'] += 1

                results['details'].append({
                    'file': file_path,
                    'success': success,
                    'message': message
                })

    return results


def get_encoding_for_language(language_code):
    """
    根据语种代码获取推荐的编码列表

    Args:
        language_code: 语种代码

    Returns:
        list: 编码列表
    """
    lang = language_code.upper()
    return SUBTITLE_ENCODINGS.get(lang, ['utf-8'])


if __name__ == '__main__':
    # 测试代码
    import sys

    print("=== 字幕编码检测工具 ===\n")

    if len(sys.argv) > 1:
        test_file = sys.argv[1]

        print(f"测试文件: {test_file}\n")

        # 检测编码
        result = detect_file_encoding(test_file)
        if result:
            print(f"检测结果:")
            print(f"  编码: {result['encoding']}")
            print(f"  置信度: {result.get('confidence', 0):.2f}")
            print(f"  语言: {result.get('language', 'unknown')}")
            print()

        # 检查是否为 UTF-8
        is_utf = is_utf8(test_file)
        print(f"是否为 UTF-8: {'✅ 是' if is_utf else '❌ 否'}")
        print()

        # 如果不是 UTF-8，询问是否转换
        if not is_utf:
            response = input("是否转换为 UTF-8? (y/N): ").strip().lower()
            if response == 'y':
                success, message = convert_subtitle_encoding(test_file)
                print(message)
    else:
        print("用法: python subtitle_encoding.py <字幕文件路径>")
        print()
        print("示例:")
        print("  python subtitle_encoding.py subtitles/AR/001_AR.srt")
