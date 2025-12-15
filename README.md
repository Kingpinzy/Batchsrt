# 批量视频字幕合成工具 (Batch Subtitle Merger)

一个简单易用的批量视频字幕合成工具，支持将多个视频文件与多语言字幕批量合成。

## 功能特点

- 🎬 批量处理多个视频文件
- 🌍 支持多语言字幕同时合成
- 🌐 现代化Web界面（推荐）或传统桌面GUI
- 📊 实时进度显示和日志记录
- ✅ 自动检测语种文件夹
- 🔄 多线程处理，界面不卡顿
- ⚡ GPU硬件加速支持（NVIDIA/Apple/AMD/Intel）
- 🛑 支持任务中途终止
- 🎨 简洁黑白配色设计
- 🚀 一键环境配置

## 系统要求

- Python 3.7+
- FFmpeg（必须安装）
- 4GB+ RAM
- macOS 10.14+ / Ubuntu 18.04+ / Windows 10+

## 快速开始（一键配置）

### 自动配置环境（推荐）

根据您的操作系统选择：

**macOS / Linux:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

配置脚本会自动：
- ✓ 检查Python版本
- ✓ 安装Python依赖包
- ✓ 检测FFmpeg安装状态
- ✓ 检测GPU硬件加速支持
- ✓ 验证所有组件

详细配置说明请查看 [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 手动安装步骤

如果需要手动安装，请按以下步骤操作：

### 1. 安装 Python

确保系统已安装 Python 3.7 或更高版本。

### 2. 安装 FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
1. 从 [FFmpeg官网](https://ffmpeg.org/download.html) 下载
2. 解压并将 `bin` 目录添加到系统 PATH

**Linux:**
```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg      # CentOS/RHEL
```

### 3. 安装 Python 依赖

```bash
pip3 install -r requirements.txt
```

## 使用方法

### 方式一：Web界面（推荐）

**启动程序：**
```bash
python3 app.py
```

启动后，在浏览器中打开：`http://localhost:5000`

**操作步骤：**

1. **填写原视频文件夹路径**
   - 输入完整路径，例如：`/Users/username/Videos`
   - 点击"验证"按钮检查文件夹是否有效

2. **填写字幕文件夹路径**
   - 输入完整路径
   - 点击"扫描语种"按钮，自动检测并显示所有语种

3. **填写输出文件夹路径**
   - 输入希望保存合成视频的路径

4. **开始批量合成**
   - 点击"开始批量合成"按钮
   - 查看实时处理日志、进度条和当前任务

### 方式二：桌面GUI（可选）

```bash
python3 batch_subtitle_merger.py
```

使用文件浏览对话框选择文件夹，操作更直观。

## 文件结构要求

### 输入文件结构

```
原始视频/
├── 001.mp4
├── 002.mp4
└── ...

字幕文件/
├── AR/
│   ├── 001_AR.srt
│   ├── 002_AR.srt
│   └── ...
├── CN/
│   ├── 001_CN.srt
│   ├── 002_CN.srt
│   └── ...
└── ...
```

### 输出文件结构

```
输出视频文件/
├── AR/
│   ├── 001_AR.mp4
│   ├── 002_AR.mp4
│   └── ...
├── CN/
│   ├── 001_CN.mp4
│   ├── 002_CN.mp4
│   └── ...
└── ...
```

## 注意事项

1. **字幕文件命名规则**
   - 字幕文件必须与视频文件名对应
   - 格式：`视频名_语种代码.srt` 或 `视频名_语种代码.str`
   - 例如：`001.mp4` 对应 `001_AR.srt`

2. **支持的字幕格式**
   - `.srt` (SubRip)
   - `.str` (自定义格式，需与SRT格式兼容)

3. **支持的视频格式**
   - `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`

4. **字幕烧录方式**
   - 使用硬字幕方式，字幕会永久烧录到视频中
   - 音频流直接复制，不进行重新编码

## 常见问题

### Q: 提示"未检测到ffmpeg"怎么办？

A: 请按照"安装步骤"中的说明安装FFmpeg，并确保已添加到系统PATH。

### Q: 处理速度慢怎么办？

A: 字幕烧录需要重新编码视频，处理时间取决于：
- 视频文件大小和分辨率
- CPU性能
- 输出视频编码参数

### Q: 字幕文件找不到怎么办？

A: 请检查：
1. 字幕文件命名是否正确（`视频名_语种.srt`）
2. 字幕是否放在对应的语种文件夹内
3. 文件扩展名是否为 `.srt` 或 `.str`

### Q: 可以修改输出视频质量吗？

A: 当前版本使用默认设置。如需自定义，可以修改 `batch_subtitle_merger.py` 中的 FFmpeg 命令参数。

## 技术细节

- **GUI框架**: Tkinter
- **视频处理**: FFmpeg
- **多线程**: 避免界面卡顿
- **字幕烧录**: 使用 FFmpeg 的 `subtitles` 滤镜

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系金并。
