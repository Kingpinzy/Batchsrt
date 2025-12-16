# 字体库目录 - 小语种字幕字体解决方案

## 📖 目录说明

此目录用于存放自定义字体文件，解决小语种字幕显示问题。

**支持的字体格式**：`.ttf`, `.otf`, `.ttc`, `.woff`, `.woff2`

---

## 🚨 小语种字幕丢失问题

### 问题原因

当使用FFmpeg将字幕烧录到视频时，如果字幕中包含的字符不在系统默认字体的字符集范围内，会导致：
- 字符显示为空白方框 □
- 字符完全不显示
- 部分字符显示异常

**常见问题语种**：
- 🇸🇦 阿拉伯语 (AR) - 需要从右到左显示支持
- 🇹🇭 泰语 (TH) - 复杂的元音和声调标记
- 🇲🇲 缅甸语 (MY) - 特殊的连笔字符
- 🇮🇱 希伯来语 (HE) - 从右到左显示
- 🇮🇳 印地语/泰米尔语等南亚语言 - 梵文字符

---

## ✨ 解决方案

本工具提供 **3种字体配置模式**：

### 1. 自动映射模式（推荐）⭐

启用自动模式后，系统会根据每种语言代码自动选择最合适的字体回退链。

**特点**：
- ✅ 自动为每种语言匹配最佳字体
- ✅ 支持字体回退（主字体缺字符时自动使用备用字体）
- ✅ 无需手动配置
- ✅ 支持40+种语言

**使用方法**：
1. 在Web界面勾选"自定义字幕样式"
2. 展开"高级选项"
3. 字体配置模式选择"自动映射（推荐）"
4. 开始合成，系统将自动处理

### 2. 字体名称模式

手动指定系统已安装的字体名称。

**使用方法**：
```
字体名称输入框：Arial, Microsoft YaHei, Noto Sans Arabic
```

**支持多字体回退**（用逗号分隔），当第一个字体缺少某些字符时，自动使用后续字体。

### 3. 字体文件模式

使用本目录（fonts/）中的字体文件。

**使用方法**：
1. 将字体文件放入 `fonts/` 目录
2. 在Web界面选择"字体文件"模式
3. 从下拉列表中选择字体
4. 点击"刷新字体列表"以更新

---

## 📥 推荐字体下载

### Google Noto Fonts（强烈推荐）✨

**官网**：https://fonts.google.com/noto

**特点**：
- ✅ 支持全球 800+ 种语言
- ✅ 完全免费，开源授权 (OFL)
- ✅ 字形统一，显示效果专业
- ✅ 是小语种字幕的最佳选择

#### 下载指南

根据您需要处理的语种，下载对应的字体：

| 语种 | 推荐字体 | 下载链接 |
|------|---------|---------|
| **阿拉伯语** (AR/FA/UR) | Noto Sans Arabic | [下载](https://fonts.google.com/noto/specimen/Noto+Sans+Arabic) |
| **简体中文** (CN/ZH) | Noto Sans CJK SC | [下载](https://github.com/googlefonts/noto-cjk/releases) |
| **繁体中文** (TW/HK) | Noto Sans CJK TC | [下载](https://github.com/googlefonts/noto-cjk/releases) |
| **日语** (JP/JA) | Noto Sans CJK JP | [下载](https://github.com/googlefonts/noto-cjk/releases) |
| **韩语** (KR/KO) | Noto Sans CJK KR | [下载](https://github.com/googlefonts/noto-cjk/releases) |
| **泰语** (TH) | Noto Sans Thai | [下载](https://fonts.google.com/noto/specimen/Noto+Sans+Thai) |
| **缅甸语** (MY) | Noto Sans Myanmar | [下载](https://fonts.google.com/noto/specimen/Noto+Sans+Myanmar) |
| **希伯来语** (HE) | Noto Sans Hebrew | [下载](https://fonts.google.com/noto/specimen/Noto+Sans+Hebrew) |
| **印地语** (HI) | Noto Sans Devanagari | [下载](https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari) |
| **孟加拉语** (BN) | Noto Sans Bengali | [下载](https://fonts.google.com/noto/specimen/Noto+Sans+Bengali) |
| **泰米尔语** (TA) | Noto Sans Tamil | [下载](https://fonts.google.com/noto/specimen/Noto+Sans+Tamil) |
| **高棉语** (KM) | Noto Sans Khmer | [下载](https://fonts.google.com/noto/specimen/Noto+Sans+Khmer) |

#### 快速下载（批量）

对于需要处理多种语言的用户，推荐下载 **Noto Sans 完整包**：

```bash
# 使用 Git 克隆（包含所有语种）
git clone https://github.com/googlefonts/noto-fonts.git
```

---

### Microsoft 系统字体

Windows/macOS 自带字体，无需下载：

| 字体名称 | 支持语种 | 可用性 |
|---------|---------|--------|
| Arial Unicode MS | 多语言通用 | Windows, macOS |
| Microsoft YaHei (微软雅黑) | 简体中文 | Windows |
| Microsoft JhengHei (微軟正黑體) | 繁体中文 | Windows |
| Malgun Gothic | 韩语 | Windows |
| Yu Gothic | 日语 | Windows 10+ |
| Traditional Arabic | 阿拉伯语 | Windows |

---

## 📋 完整语种映射表

本工具的自动映射模式支持以下语种代码：

### 阿拉伯语系
- `AR` - 阿拉伯语
- `FA` - 波斯语
- `UR` - 乌尔都语

### 东亚语言
- `CN`/`ZH` - 简体中文
- `TW` - 繁体中文（台湾）
- `HK` - 繁体中文（香港）
- `JP`/`JA` - 日语
- `KR`/`KO` - 韩语

### 东南亚语言
- `TH` - 泰语
- `VI` - 越南语
- `MY` - 缅甸语
- `KM` - 高棉语（柬埔寨）
- `LO` - 老挝语
- `ID` - 印尼语
- `MS` - 马来语

### 南亚语言
- `HI` - 印地语
- `BN` - 孟加拉语
- `TA` - 泰米尔语
- `TE` - 泰卢固语

### 欧洲语言
- `EN` - 英语
- `ES` - 西班牙语
- `FR` - 法语
- `DE` - 德语
- `IT` - 意大利语
- `PT` - 葡萄牙语
- `RU` - 俄语
- `EL` - 希腊语
- `TR` - 土耳其语

### 其他语言
- `HE` - 希伯来语

---

## 🛠️ 使用示例

### 示例 1：处理阿拉伯语字幕

**问题**：阿拉伯语字幕显示为方框

**解决方案**：

**方式 A：自动模式（推荐）**
```
1. 启用"自定义字幕样式"
2. 选择"自动映射"模式
3. 系统自动使用：Noto Sans Arabic → Arial Unicode MS → 其他回退字体
```

**方式 B：字体文件模式**
```
1. 下载 NotoSansArabic-Regular.ttf
2. 放入 fonts/ 目录
3. 选择"字体文件"模式，选择该文件
```

### 示例 2：处理多种语言（AR + CN + TH）

**方式 A：自动模式（最简单）**
```
直接使用自动映射模式，系统会为每种语言自动选择最佳字体：
- AR 文件夹 → 使用 Noto Sans Arabic
- CN 文件夹 → 使用 Noto Sans CJK SC
- TH 文件夹 → 使用 Noto Sans Thai
```

**方式 B：通用字体（不推荐）**
```
使用 Arial Unicode MS，但可能显示效果不佳
```

---

## ❓ 常见问题

### Q1: 字体文件下载后放在哪里？

**A**: 将 `.ttf` 或 `.otf` 文件直接放在 `BatchSRT/fonts/` 目录下即可。

```
BatchSRT/
├── fonts/
│   ├── NotoSansArabic-Regular.ttf
│   ├── NotoSansCJKsc-Regular.otf
│   └── NotoSansThai-Regular.ttf
├── app.py
└── ...
```

### Q2: 自动模式需要下载字体吗？

**A**:
- 如果系统已安装推荐字体（如 Windows 的 Arial Unicode MS），可以直接使用
- 如果字幕仍有问题，建议下载对应的 Noto Sans 字体到 fonts/ 目录
- 自动模式会优先使用 fonts/ 目录中的字体

### Q3: 为什么有些字符还是显示不出来？

**A**: 可能的原因：
1. **字体未包含该字符** - 尝试使用 Noto Sans 系列字体
2. **字幕文件编码问题** - 确保 .srt 文件为 UTF-8 编码
3. **FFmpeg 版本问题** - 确保 FFmpeg 编译时包含 libass 支持

### Q4: CJK 字体文件太大怎么办？

**A**: Noto Sans CJK 完整版约 100MB+，可以下载简化版：
- 简体中文：只下载 SC (Simplified Chinese)
- 繁体中文：只下载 TC (Traditional Chinese)
- 或使用系统自带的中文字体（微软雅黑、黑体等）

### Q5: 如何测试字体是否支持某种语言？

**A**: 使用系统字体查看器：
- **Windows**: 双击字体文件，查看字符集
- **macOS**: 使用"字体册"应用
- **Linux**: 使用 `fc-list` 命令

---

## 🔧 高级配置

### 字体回退链自定义

如果您想自定义字体回退逻辑，可以编辑 `font_config.py` 文件中的 `LANGUAGE_FONT_MAP` 字典。

例如，为阿拉伯语添加自定义字体：

```python
'AR': ['MyCustomArabicFont', 'Noto Sans Arabic', 'Arial Unicode MS'],
```

### 命令行测试字体配置

```bash
# 测试字体配置
python font_config.py

# 输出示例：
# AR: Noto Sans Arabic, Arial Unicode MS, Traditional Arabic
# CN: Noto Sans CJK SC, Microsoft YaHei, SimHei
```

---

## 📚 相关资源

- **Google Noto Fonts 官网**: https://fonts.google.com/noto
- **Noto Fonts GitHub**: https://github.com/googlefonts/noto-fonts
- **FFmpeg libass 文档**: https://ffmpeg.org/ffmpeg-filters.html#subtitles-1
- **Unicode 字符集查询**: https://unicode-table.com/

---

## 💡 最佳实践

1. **优先使用自动映射模式** - 最省心的方案
2. **下载常用语种的 Noto Sans 字体** - 一次下载，长期使用
3. **保持字体文件在 fonts/ 目录** - 方便管理和备份
4. **使用 UTF-8 编码保存字幕文件** - 避免编码问题
5. **测试小片段视频** - 在大批量处理前先测试效果

---

**最后更新**: 2024
**维护者**: BatchSRT 项目组
**许可证**: 本文档遵循项目许可证

