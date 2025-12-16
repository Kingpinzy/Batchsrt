# 小语种字幕字体问题解决指南

## 📋 目录

- [问题描述](#问题描述)
- [解决方案总览](#解决方案总览)
- [快速开始](#快速开始)
- [三种字体配置模式详解](#三种字体配置模式详解)
- [实战案例](#实战案例)
- [常见问题](#常见问题)

---

## 问题描述

### 症状

在处理小语种字幕时，可能会遇到以下问题：

- ✖️ 阿拉伯语字幕显示为空白方框 □□□
- ✖️ 泰语字幕的声调标记缺失
- ✖️ 缅甸语、希伯来语等字符完全不显示
- ✖️ 部分字符正常，部分字符异常

### 根本原因

FFmpeg 使用的 libass 字幕渲染库依赖系统字体来显示字符。当字幕中的字符不在指定字体的字符集范围内时，就会出现显示问题。

**举例**：
- Windows 默认的 Arial 字体不包含阿拉伯语字符
- 系统字体可能不支持复杂的东南亚语言书写系统

---

## 解决方案总览

本工具现已集成 **智能字体管理系统**，提供三种配置模式：

| 模式 | 适用场景 | 优势 | 难度 |
|------|---------|------|------|
| **自动映射** | 多语种批量处理 | 无需配置，自动为每种语言选择最佳字体 | ⭐ 简单 |
| **字体名称** | 使用系统已安装字体 | 灵活，支持自定义字体回退链 | ⭐⭐ 中等 |
| **字体文件** | 使用自定义字体文件 | 完全可控，适合特殊需求 | ⭐⭐⭐ 较难 |

---

## 快速开始

### 方式一：自动模式（最简单）

**适合绝大多数用户，推荐首选！**

1. 启动 Web 界面：
   ```bash
   python app.py
   # 访问 http://localhost:5000
   ```

2. 配置路径并验证：
   - 原视频文件夹
   - 字幕文件夹（包含 AR, CN, TH 等语种子文件夹）
   - 输出文件夹

3. 启用字幕样式自定义：
   - ✅ 勾选"自定义字幕样式"
   - 展开"高级选项"
   - **字体配置模式**选择 **"自动映射（推荐）"**

4. 点击"开始批量合成"

**系统会自动处理**：
```
AR 文件夹 → 自动使用 Noto Sans Arabic (或系统的 Arial Unicode MS)
CN 文件夹 → 自动使用 Noto Sans CJK SC (或微软雅黑)
TH 文件夹 → 自动使用 Noto Sans Thai (或 Leelawadee)
...
```

### 方式二：下载推荐字体（可选，提升效果）

如果自动模式效果不理想，可以下载推荐字体：

1. 访问 [Google Noto Fonts](https://fonts.google.com/noto)

2. 下载您需要的语种字体：
   - 阿拉伯语：Noto Sans Arabic
   - 简体中文：Noto Sans CJK SC
   - 泰语：Noto Sans Thai
   - 等等...

3. 将 `.ttf` 或 `.otf` 文件放入项目的 `fonts/` 目录

4. 使用自动模式或字体文件模式即可

---

## 三种字体配置模式详解

### 模式 1: 自动映射（推荐）⭐

#### 工作原理

系统内置了 40+ 种语言的字体映射表，会根据语种代码（如 AR, CN, TH）自动选择最合适的字体。

#### 字体回退机制

每种语言都配置了多个回退字体，按优先级使用：

```
阿拉伯语 (AR):
1. Noto Sans Arabic      (最优先)
2. Arial Unicode MS      (通用回退)
3. Traditional Arabic    (Windows系统字体)
4. Noto Sans            (通用字体)
```

如果第一个字体缺少某些字符，自动使用第二个，以此类推。

#### 支持的语种

完整列表见 `fonts/README.md`，常用语种包括：

**东亚**：CN, TW, HK, JP, KR
**阿拉伯**：AR, FA, UR
**东南亚**：TH, VI, MY, KM, LO
**南亚**：HI, BN, TA, TE
**欧洲**：EN, ES, FR, DE, RU, EL
**其他**：HE (希伯来语), TR (土耳其语)

#### 何时使用

- ✅ 处理多种语言
- ✅ 不想手动配置字体
- ✅ 使用标准语种代码命名字幕文件夹

### 模式 2: 字体名称

#### 工作原理

手动指定系统已安装的字体名称。

#### 使用方法

1. 在"字体配置模式"选择"字体名称"
2. 输入字体名称，例如：
   ```
   Noto Sans Arabic
   ```

3. 支持多字体回退（用逗号分隔）：
   ```
   Noto Sans Arabic, Arial Unicode MS, Traditional Arabic
   ```

#### 如何查看系统字体

**Windows**:
- 打开"设置" → "个性化" → "字体"
- 或运行 `control fonts`

**macOS**:
- 打开"字体册"应用

**Linux**:
```bash
fc-list : family | sort | uniq
```

#### 何时使用

- ✅ 想使用特定的系统字体
- ✅ 需要自定义字体回退顺序
- ✅ 所有视频使用统一字体

### 模式 3: 字体文件

#### 工作原理

直接使用 `fonts/` 目录中的字体文件。

#### 使用方法

1. 将字体文件（.ttf, .otf）放入 `BatchSRT/fonts/` 目录

2. 在Web界面：
   - 选择"字体文件"模式
   - 从下拉列表选择字体
   - 点击"刷新字体列表"更新

#### 何时使用

- ✅ 使用自定义字体文件
- ✅ 系统未安装所需字体
- ✅ 需要特定的字体版本

---

## 实战案例

### 案例 1: 处理阿拉伯语字幕

**场景**：有 50 个视频，需要添加阿拉伯语 (AR) 字幕

**问题**：字幕显示为方框 □□□

#### 解决方案 A：自动模式（推荐）

```yaml
步骤：
1. 字幕文件夹结构：
   subtitles/
   └── AR/
       ├── video1_AR.srt
       ├── video2_AR.srt
       └── ...

2. Web界面配置：
   - 勾选"自定义字幕样式"
   - 字体模式：自动映射
   - 开始合成

结果：系统自动使用 Noto Sans Arabic 或 Arial Unicode MS
```

#### 解决方案 B：下载字体文件

```yaml
步骤：
1. 下载 Noto Sans Arabic：
   https://fonts.google.com/noto/specimen/Noto+Sans+Arabic

2. 将 NotoSansArabic-Regular.ttf 放入 fonts/ 目录

3. Web界面配置：
   - 字体模式：字体文件
   - 选择：NotoSansArabic-Regular.ttf

结果：所有阿拉伯语字幕完美显示
```

### 案例 2: 多语种混合（AR + CN + TH + EN）

**场景**：100 个视频，4 种语言，需要批量处理

#### 解决方案：自动模式

```yaml
文件夹结构：
videos/
├── video001.mp4
├── video002.mp4
└── ...

subtitles/
├── AR/
│   ├── video001_AR.srt
│   └── ...
├── CN/
│   ├── video001_CN.srt
│   └── ...
├── TH/
│   ├── video001_TH.srt
│   └── ...
└── EN/
    ├── video001_EN.srt
    └── ...

配置：
- 字体模式：自动映射（推荐）
- 其他样式：按需调整

结果：
- AR → Noto Sans Arabic
- CN → Noto Sans CJK SC / Microsoft YaHei
- TH → Noto Sans Thai / Leelawadee
- EN → Arial / Helvetica

总共 400 个任务（100视频 × 4语言），全自动完成！
```

### 案例 3: 泰语字幕声调缺失

**场景**：泰语字幕的声调标记显示不正常

**原因**：系统字体不支持泰语复杂书写规则

#### 解决方案

```yaml
方式1 - 自动模式：
  系统会自动使用 Noto Sans Thai 或 Leelawadee

方式2 - 下载专用字体：
  1. 下载 Noto Sans Thai
  2. 放入 fonts/ 目录
  3. 使用字体文件模式选择

推荐字体：
  - Noto Sans Thai (Google)
  - Leelawadee (Windows系统自带)
```

---

## 常见问题

### Q1: 自动模式下字幕还是有问题？

**A**: 可能原因：

1. **系统缺少推荐字体**
   - 下载对应语种的 Noto Sans 字体到 fonts/ 目录
   - 自动模式会优先使用 fonts/ 目录中的字体

2. **字幕文件编码问题**
   - 确保 .srt 文件为 **UTF-8** 编码（而非 ANSI 或 GBK）
   - 使用 Notepad++ 或 VS Code 转换编码

3. **FFmpeg 版本问题**
   - 确保 FFmpeg 包含 libass 支持：
     ```bash
     ffmpeg -version | grep libass
     ```

### Q2: 如何知道系统有没有某个字体？

**Windows**:
```cmd
# 打开字体设置
control fonts

# 或搜索字体
dir %windir%\Fonts | findstr /i "arabic"
```

**macOS**:
```bash
# 列出所有字体
system_profiler SPFontsDataType
```

**Linux**:
```bash
# 搜索字体
fc-list | grep -i "noto sans"
```

### Q3: Noto Sans CJK 文件太大（100MB+），有替代方案吗？

**A**: 有以下选择：

1. **只下载需要的语种**
   - SC (简体中文) - 单独下载
   - TC (繁体中文) - 单独下载
   - 不需要下载完整 CJK 包

2. **使用系统字体**（自动模式会自动选择）
   - 微软雅黑 (Microsoft YaHei) - Windows
   - 黑体 (SimHei) - Windows
   - PingFang SC - macOS

3. **使用字体名称模式**
   ```
   字体名称：Microsoft YaHei, SimHei
   ```

### Q4: 字体文件应该下载哪个版本？

**A**: 推荐选择：

- **Regular** (常规) - 适合大多数场景
- **Bold** (粗体) - 需要加粗效果时
- 避免使用 Light, Thin 等超细字体（视频中不易辨认）

**文件扩展名**：
- `.ttf` (TrueType) - 常用，兼容性好
- `.otf` (OpenType) - 较新，功能更强
- 两者都可以使用

### Q5: 能否为不同语种设置不同的字体大小或位置？

**A**: 目前版本的字幕样式（字体大小、位置等）是全局设置，应用于所有语种。

**变通方案**：
- 分批处理不同语种
- 第一批：AR + TH (相似设置)
- 第二批：CN + JP (相似设置)

### Q6: 如何测试字体效果？

**A**: 建议先小规模测试：

```yaml
1. 选择1个视频
2. 选择1种语言
3. 配置字体设置
4. 开始合成
5. 检查输出视频
6. 满意后再批量处理
```

### Q7: 自动映射的字体列表可以自定义吗？

**A**: 可以！编辑 `font_config.py` 文件：

```python
# 找到 LANGUAGE_FONT_MAP 字典
LANGUAGE_FONT_MAP = {
    'AR': ['MyCustomFont', 'Noto Sans Arabic', ...],
    # 添加或修改语种映射
}
```

保存后重启应用即可生效。

---

## 📚 延伸阅读

- **fonts/README.md** - 详细的字体下载和配置指南
- **font_config.py** - 字体映射配置源代码
- **Google Noto Fonts 官网** - https://fonts.google.com/noto
- **FFmpeg subtitles 滤镜文档** - https://ffmpeg.org/ffmpeg-filters.html#subtitles-1

---

## 💡 最佳实践总结

1. ✅ **优先使用自动映射模式** - 最简单，效果最好
2. ✅ **下载常用语种的 Noto Sans 字体** - 一劳永逸
3. ✅ **字幕文件使用 UTF-8 编码** - 避免编码问题
4. ✅ **先测试小批量** - 大规模处理前验证效果
5. ✅ **保持字体文件在 fonts/ 目录** - 方便管理
6. ✅ **使用轮廓(Outline)和阴影(Shadow)** - 复杂背景下提升可读性

---

**文档版本**: v1.0
**最后更新**: 2024
**问题反馈**: 请在项目 GitHub Issues 中报告
