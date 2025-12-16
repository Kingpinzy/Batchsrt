# 阿拉伯语字幕方框问题 - 最终解决方案

## 🔍 问题确认

- ✅ 字幕文件编码：UTF-8
- ✅ 字幕内容：正确的阿拉伯语文本
- ✅ 字体文件：已下载 NotoSansArabic-Regular.ttf
- ❌ 合成后：仍然显示方框 □□

## 💡 根本原因

FFmpeg 的 `subtitles` 滤镜在 Windows 上加载字体文件时可能存在路径或字体名称匹配问题。

## ✅ 解决方案：手动测试最佳配置

### 步骤 1：手动测试 FFmpeg 命令

打开命令提示符（CMD），运行以下命令测试不同配置：

#### 测试 A：使用 fontsdir 参数

```cmd
cd /d F:\seaart\zimu\BatchSRT

ffmpeg -i "f:\Project\moveTest\原始视频\001.mp4" ^
  -vf "subtitles='f\:/Project/moveTest/字幕文件/AR/001_AR.srt':charenc=UTF-8:fontsdir='F\:/seaart/zimu/BatchSRT/fonts':force_style='FontName=Noto Sans Arabic,FontSize=24,Outline=2'" ^
  -c:a copy -t 15 -y test_A.mp4
```

#### 测试 B：尝试不同的字体名称

```cmd
ffmpeg -i "f:\Project\moveTest\原始视频\001.mp4" ^
  -vf "subtitles='f\:/Project/moveTest/字幕文件/AR/001_AR.srt':charenc=UTF-8:fontsdir='F\:/seaart/zimu/BatchSRT/fonts':force_style='FontName=NotoSansArabic,FontSize=24,Outline=2'" ^
  -c:a copy -t 15 -y test_B.mp4
```

#### 测试 C：只用 fontsdir，不强制字体

```cmd
ffmpeg -i "f:\Project\moveTest\原始视频\001.mp4" ^
  -vf "subtitles='f\:/Project/moveTest/字幕文件/AR/001_AR.srt':charenc=UTF-8:fontsdir='F\:/seaart/zimu/BatchSRT/fonts'" ^
  -c:a copy -t 15 -y test_C.mp4
```

#### 测试 D：使用 Arial Unicode MS（如果系统有）

```cmd
ffmpeg -i "f:\Project\moveTest\原始视频\001.mp4" ^
  -vf "subtitles='f\:/Project/moveTest/字幕文件/AR/001_AR.srt':charenc=UTF-8:force_style='FontName=Arial Unicode MS,FontSize=24'" ^
  -c:a copy -t 15 -y test_D.mp4
```

**注意**: 将上面命令中的路径替换成您实际的路径！

### 步骤 2：播放测试视频

播放生成的 `test_A.mp4`, `test_B.mp4`, `test_C.mp4`, `test_D.mp4`，检查哪个视频的阿拉伯语字幕显示正确。

### 步骤 3：告诉我哪个测试成功

告诉我哪个测试（A/B/C/D）的字幕显示正确，我会相应地更新应用代码。

---

## 🔧 临时手动解决方案

如果急需处理，可以直接使用成功的 FFmpeg 命令：

```cmd
REM 假设测试 A 成功
ffmpeg -i "原始视频.mp4" ^
  -vf "subtitles='字幕文件.srt':charenc=UTF-8:fontsdir='F\:/seaart/zimu/BatchSRT/fonts':force_style='FontName=Noto Sans Arabic,FontSize=24'" ^
  -c:a copy -y "输出视频.mp4"
```

---

## 📋 路径格式说明

FFmpeg 在 Windows 上的路径格式要求：

**原始路径**:
```
F:\seaart\zimu\BatchSRT\fonts
```

**FFmpeg 格式**（反斜杠改正斜杠，冒号前加反斜杠转义）:
```
F\:/seaart/zimu/BatchSRT/fonts
```

**示例转换**:
- `C:\Users\文件\test.srt` → `C\:/Users/文件/test.srt`
- `D:\Project\字幕\AR\001.srt` → `D\:/Project/字幕/AR/001.srt`

---

## 🆘 如果所有测试都失败

### 备选方案 1：安装系统字体

1. 双击 `F:\seaart\zimu\BatchSRT\fonts\NotoSansArabic-Regular.ttf`
2. 点击"为所有用户安装"
3. 重启应用，选择"字体名称"模式
4. 输入字体名称：`Noto Sans Arabic`

### 备选方案 2：使用 ass 滤镜

如果 subtitles 滤镜不行，可以尝试 ass 滤镜：

```cmd
ffmpeg -i "视频.mp4" ^
  -vf "ass='字幕.srt'" ^
  -c:a copy -y "输出.mp4"
```

但 ass 滤镜需要 .ass 格式的字幕文件。

---

## 📞 需要更多帮助

请提供：
1. 测试结果（哪个测试成功/失败）
2. FFmpeg 的错误信息（如果有）
3. 您的 FFmpeg 版本：`ffmpeg -version`

我会根据您的反馈提供精确的解决方案。
