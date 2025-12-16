#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体配置模块 - 为不同语种提供字体推荐和映射
Font Configuration Module - Provides font recommendations and mappings for different languages
"""

import os
from pathlib import Path

# 项目根目录下的fonts文件夹
FONTS_DIR = Path(__file__).parent / 'fonts'

# 语种代码到推荐字体的映射
# 格式: 语种代码 -> [推荐字体列表，按优先级排序]
LANGUAGE_FONT_MAP = {
    # 阿拉伯语系
    'AR': ['Noto Sans Arabic', 'Arial Unicode MS', 'Traditional Arabic', 'Simplified Arabic'],
    'FA': ['Noto Sans Arabic', 'Arial Unicode MS', 'Traditional Arabic'],  # 波斯语
    'UR': ['Noto Sans Arabic', 'Arial Unicode MS'],  # 乌尔都语

    # 东亚语言
    'CN': ['Noto Sans CJK SC', 'Microsoft YaHei', 'SimHei', 'PingFang SC', 'Noto Sans SC', '微软雅黑', '黑体'],
    'ZH': ['Noto Sans CJK SC', 'Microsoft YaHei', 'SimHei', 'PingFang SC', 'Noto Sans SC', '微软雅黑'],
    'TW': ['Noto Sans CJK TC', 'Microsoft JhengHei', 'PingFang TC', 'Noto Sans TC', '微軟正黑體'],
    'HK': ['Noto Sans CJK HK', 'Microsoft JhengHei', 'PingFang HK', 'Noto Sans HK'],
    'JP': ['Noto Sans CJK JP', 'Yu Gothic', 'Meiryo', 'MS Gothic', 'Hiragino Sans'],
    'JA': ['Noto Sans CJK JP', 'Yu Gothic', 'Meiryo', 'MS Gothic'],
    'KR': ['Noto Sans CJK KR', 'Malgun Gothic', 'Nanum Gothic', 'Apple SD Gothic Neo'],
    'KO': ['Noto Sans CJK KR', 'Malgun Gothic', 'Nanum Gothic'],

    # 东南亚语言
    'TH': ['Noto Sans Thai', 'Leelawadee', 'Tahoma', 'Arial Unicode MS'],  # 泰语
    'VI': ['Noto Sans', 'Arial Unicode MS', 'Times New Roman'],  # 越南语
    'MY': ['Noto Sans Myanmar', 'Myanmar Text', 'Arial Unicode MS'],  # 缅甸语
    'KM': ['Noto Sans Khmer', 'Khmer UI', 'Arial Unicode MS'],  # 高棉语
    'LO': ['Noto Sans Lao', 'DokChampa', 'Arial Unicode MS'],  # 老挝语

    # 南亚语言
    'HI': ['Noto Sans Devanagari', 'Mangal', 'Arial Unicode MS'],  # 印地语
    'BN': ['Noto Sans Bengali', 'Vrinda', 'Arial Unicode MS'],  # 孟加拉语
    'TA': ['Noto Sans Tamil', 'Latha', 'Arial Unicode MS'],  # 泰米尔语
    'TE': ['Noto Sans Telugu', 'Gautami', 'Arial Unicode MS'],  # 泰卢固语

    # 欧洲语言
    'EN': ['Arial', 'Helvetica', 'Noto Sans', 'Roboto'],
    'ES': ['Arial', 'Helvetica', 'Noto Sans'],  # 西班牙语
    'FR': ['Arial', 'Helvetica', 'Noto Sans'],  # 法语
    'DE': ['Arial', 'Helvetica', 'Noto Sans'],  # 德语
    'IT': ['Arial', 'Helvetica', 'Noto Sans'],  # 意大利语
    'PT': ['Arial', 'Helvetica', 'Noto Sans'],  # 葡萄牙语
    'RU': ['Noto Sans', 'Arial Unicode MS', 'DejaVu Sans'],  # 俄语
    'EL': ['Noto Sans', 'Arial Unicode MS', 'DejaVu Sans'],  # 希腊语

    # 其他语言
    'HE': ['Noto Sans Hebrew', 'Arial Unicode MS', 'David'],  # 希伯来语
    'TR': ['Noto Sans', 'Arial', 'Calibri'],  # 土耳其语
    'ID': ['Noto Sans', 'Arial', 'Calibri'],  # 印度尼西亚语
    'MS': ['Noto Sans', 'Arial', 'Calibri'],  # 马来语
}

# 通用回退字体列表（当没有找到语种特定字体时使用）
FALLBACK_FONTS = [
    'Noto Sans',
    'Arial Unicode MS',
    'DejaVu Sans',
    'FreeSans',
    'Liberation Sans'
]


def get_font_for_language(language_code):
    """
    根据语种代码获取推荐的字体列表

    Args:
        language_code: 语种代码（如 'AR', 'CN', 'EN'）

    Returns:
        list: 推荐字体列表，按优先级排序
    """
    # 转换为大写进行匹配
    lang = language_code.upper()

    # 尝试直接匹配
    if lang in LANGUAGE_FONT_MAP:
        return LANGUAGE_FONT_MAP[lang]

    # 尝试模糊匹配（前两个字符）
    lang_prefix = lang[:2] if len(lang) >= 2 else lang
    for key in LANGUAGE_FONT_MAP:
        if key.startswith(lang_prefix):
            return LANGUAGE_FONT_MAP[key]

    # 返回通用回退字体
    return FALLBACK_FONTS


def get_all_font_files(fonts_dir=None):
    """
    扫描fonts目录中的所有字体文件

    Args:
        fonts_dir: 字体目录路径，默认为项目fonts目录

    Returns:
        list: 字体文件信息列表 [{'name': 'xxx.ttf', 'path': '/path/to/xxx.ttf'}, ...]
    """
    if fonts_dir is None:
        fonts_dir = FONTS_DIR

    font_files = []
    font_extensions = ['.ttf', '.otf', '.ttc', '.woff', '.woff2']

    try:
        if os.path.exists(fonts_dir):
            for file in os.listdir(fonts_dir):
                if any(file.lower().endswith(ext) for ext in font_extensions):
                    font_files.append({
                        'name': file,
                        'path': os.path.join(fonts_dir, file)
                    })
    except Exception as e:
        print(f"扫描字体文件失败: {e}")

    return sorted(font_files, key=lambda x: x['name'])


def build_font_family_string(language_code, custom_font=None):
    """
    构建字体族字符串，用于FFmpeg的force_style参数
    支持字体回退机制

    Args:
        language_code: 语种代码
        custom_font: 用户自定义字体（可选）

    Returns:
        str: 字体族字符串，如 "Noto Sans Arabic,Arial Unicode MS,DejaVu Sans"
    """
    fonts = []

    # 优先使用用户自定义字体
    if custom_font:
        fonts.append(custom_font)

    # 添加语种特定的推荐字体
    recommended_fonts = get_font_for_language(language_code)
    fonts.extend(recommended_fonts)

    # 添加通用回退字体
    fonts.extend(FALLBACK_FONTS)

    # 去重并保持顺序
    seen = set()
    unique_fonts = []
    for font in fonts:
        if font not in seen:
            seen.add(font)
            unique_fonts.append(font)

    return ','.join(unique_fonts)


def is_font_file_path(font_str):
    """
    判断字符串是否为字体文件路径

    Args:
        font_str: 字体字符串

    Returns:
        bool: 是否为文件路径
    """
    if not font_str:
        return False

    # 检查是否包含路径分隔符
    if '/' in font_str or '\\' in font_str:
        return True

    # 检查是否有字体文件扩展名
    font_extensions = ['.ttf', '.otf', '.ttc', '.woff', '.woff2']
    return any(font_str.lower().endswith(ext) for ext in font_extensions)


def normalize_font_path(font_path):
    """
    标准化字体路径，用于FFmpeg
    Windows路径转换为FFmpeg兼容格式

    Args:
        font_path: 原始字体路径

    Returns:
        str: 标准化后的路径
    """
    # 替换反斜杠为正斜杠
    normalized = font_path.replace('\\', '/')
    # 转义冒号（Windows驱动器字母）
    normalized = normalized.replace(':', '\\:')
    return normalized


def check_system_font_exists(font_name):
    """
    检查系统是否安装了指定字体（仅Windows）

    Args:
        font_name: 字体名称

    Returns:
        bool: 字体是否存在
    """
    try:
        import platform
        if platform.system() == 'Windows':
            import winreg
            # 检查注册表中的字体
            key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        if font_name.lower() in name.lower():
                            winreg.CloseKey(key)
                            return True
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except:
                pass

            # 检查字体文件夹
            import os
            fonts_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
            if os.path.exists(fonts_dir):
                for file in os.listdir(fonts_dir):
                    if font_name.lower().replace(' ', '').replace('-', '') in file.lower().replace(' ', '').replace('-', ''):
                        return True
        return False
    except:
        return False


def find_font_file_for_language(language_code, fonts_dir=None):
    """
    在fonts目录中查找适合该语种的字体文件

    Args:
        language_code: 语种代码
        fonts_dir: 字体目录（默认为项目fonts目录）

    Returns:
        str: 字体文件路径，如果未找到返回None
    """
    if fonts_dir is None:
        fonts_dir = FONTS_DIR

    if not os.path.exists(fonts_dir):
        return None

    # 获取推荐字体列表
    recommended_fonts = get_font_for_language(language_code)

    # 语种相关的关键词（用于文件名匹配）
    keywords = {
        'AR': ['arabic', 'arab'],
        'FA': ['arabic', 'persian', 'farsi'],
        'UR': ['arabic', 'urdu'],
        'TH': ['thai'],
        'MY': ['myanmar', 'burma'],
        'HE': ['hebrew'],
        'HI': ['devanagari', 'hindi'],
        'BN': ['bengali'],
        'TA': ['tamil'],
        'CN': ['cjk', 'chinese', 'sc', 'hans', 'simp'],
        'ZH': ['cjk', 'chinese', 'sc', 'hans', 'simp'],
        'TW': ['cjk', 'chinese', 'tc', 'hant', 'trad'],
        'HK': ['cjk', 'chinese', 'hk'],
        'JP': ['cjk', 'japanese', 'jp'],
        'JA': ['cjk', 'japanese', 'jp'],
        'KR': ['cjk', 'korean', 'kr'],
        'KO': ['cjk', 'korean', 'kr'],
    }

    lang_keywords = keywords.get(language_code.upper(), [])

    # 扫描fonts目录
    font_files = get_all_font_files(fonts_dir)

    # 优先级1: 文件名包含推荐字体名称
    for font in recommended_fonts:
        font_lower = font.lower().replace(' ', '').replace('-', '')
        for font_file in font_files:
            file_name_lower = font_file['name'].lower().replace(' ', '').replace('-', '')
            if font_lower in file_name_lower:
                return font_file['path']

    # 优先级2: 文件名包含语种关键词
    if lang_keywords:
        for keyword in lang_keywords:
            for font_file in font_files:
                if keyword.lower() in font_file['name'].lower():
                    return font_file['path']

    return None


def get_available_font_for_language(language_code, fonts_dir=None):
    """
    根据语种代码获取实际可用的字体（字体文件路径或字体名称）

    Args:
        language_code: 语种代码
        fonts_dir: 字体目录（默认为项目fonts目录）

    Returns:
        tuple: (font_type, font_value)
            - font_type: 'file' 或 'name'
            - font_value: 字体文件路径 或 字体名称
    """
    # 优先级1: 检查fonts目录中的字体文件
    font_file = find_font_file_for_language(language_code, fonts_dir)
    if font_file:
        return ('file', font_file)

    # 优先级2: 检查系统字体
    recommended_fonts = get_font_for_language(language_code)
    for font in recommended_fonts:
        if check_system_font_exists(font):
            return ('name', font)

    # 优先级3: 回退到Arial Unicode MS
    if check_system_font_exists('Arial Unicode MS'):
        return ('name', 'Arial Unicode MS')

    # 最后回退到Arial
    return ('name', 'Arial')


# 小语种字体下载指南
FONT_DOWNLOAD_GUIDE = {
    'noto': {
        'name': 'Google Noto Fonts（推荐）',
        'url': 'https://fonts.google.com/noto',
        'description': '支持全球800+语言，是小语种字幕的最佳选择',
        'files': {
            'Arabic': 'NotoSansArabic-*.ttf',
            'CJK SC': 'NotoSansCJKsc-*.otf (简体中文)',
            'CJK TC': 'NotoSansCJKtc-*.otf (繁体中文)',
            'CJK JP': 'NotoSansCJKjp-*.otf (日文)',
            'CJK KR': 'NotoSansCJKkr-*.otf (韩文)',
            'Thai': 'NotoSansThai-*.ttf',
            'Myanmar': 'NotoSansMyanmar-*.ttf',
            'Hebrew': 'NotoSansHebrew-*.ttf',
            'Devanagari': 'NotoSansDevanagari-*.ttf (印地语)',
        }
    },
    'microsoft': {
        'name': 'Microsoft Unicode Fonts',
        'description': 'Windows系统自带，支持广泛的Unicode字符',
        'fonts': ['Arial Unicode MS', 'Microsoft YaHei', 'Microsoft JhengHei']
    }
}


if __name__ == '__main__':
    # 测试代码
    print("=== 字体配置测试 ===\n")

    test_languages = ['AR', 'CN', 'TH', 'EN', 'HE']
    for lang in test_languages:
        fonts = get_font_for_language(lang)
        print(f"{lang}: {', '.join(fonts[:3])}")

    print(f"\n字体文件扫描:")
    font_files = get_all_font_files()
    if font_files:
        for font in font_files:
            print(f"  - {font['name']}")
    else:
        print("  未找到字体文件，请将字体放入 fonts/ 目录")

    print(f"\n字体族字符串示例:")
    print(f"  AR: {build_font_family_string('AR')}")
    print(f"  CN自定义: {build_font_family_string('CN', 'MyCustomFont')}")
