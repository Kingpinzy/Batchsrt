# 环境配置指南

## 快速开始

### 一键配置（推荐）

根据您的操作系统，选择相应的配置脚本：

#### macOS / Linux

```bash
./setup.sh
```

或

```bash
python3 setup.py
```

#### Windows

双击运行 `setup.bat` 或在命令行中执行：

```cmd
setup.bat
```

或

```cmd
python setup.py
```

## 配置内容

环境配置器会自动检查和安装以下依赖：

### 1. Python环境
- **要求版本**: Python 3.7+
- **当前推荐**: Python 3.10 或 3.11

### 2. Python依赖包
- `flask==3.0.0` - Web框架
- `flask-cors==4.0.0` - 跨域资源共享支持

### 3. FFmpeg（视频处理核心）
- **状态**: 配置器会检查是否安装
- **作用**: 视频字幕合成的核心工具
- **GPU加速**: 自动检测硬件加速支持

## 手动安装步骤

如果自动配置失败，可以按照以下步骤手动安装：

### 步骤1: 安装Python依赖

```bash
pip3 install -r requirements.txt
```

或逐个安装：

```bash
pip3 install flask==3.0.0
pip3 install flask-cors==4.0.0
```

### 步骤2: 安装FFmpeg

#### macOS

使用Homebrew安装：

```bash
brew install ffmpeg
```

验证安装：

```bash
ffmpeg -version
```

#### Linux

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**CentOS/RHEL:**

```bash
sudo yum install epel-release
sudo yum install ffmpeg
```

**Arch Linux:**

```bash
sudo pacman -S ffmpeg
```

#### Windows

1. 下载FFmpeg:
   - 访问 https://ffmpeg.org/download.html
   - 选择Windows版本下载

2. 解压缩到目录，例如：`C:\ffmpeg`

3. 添加到系统PATH:
   - 右键"此电脑" → "属性" → "高级系统设置"
   - "环境变量" → 编辑"Path"
   - 添加 `C:\ffmpeg\bin`

4. 验证安装:
   ```cmd
   ffmpeg -version
   ```

或使用Chocolatey (如果已安装):

```cmd
choco install ffmpeg
```

## 验证安装

运行配置脚本后，会自动验证：

1. ✓ Python版本 >= 3.7
2. ✓ pip包管理器可用
3. ✓ Flask和Flask-CORS已安装
4. ✓ FFmpeg已安装（如有）
5. ✓ 硬件加速支持检测

## 启动应用

配置完成后，启动应用：

```bash
python3 app.py
```

然后在浏览器中访问：

```
http://localhost:5000
```

## 常见问题

### Q1: Python版本过低

**问题**: Python版本低于3.7

**解决方案**:
- macOS: `brew install python3`
- Linux: 使用系统包管理器升级
- Windows: 从 https://python.org 下载安装最新版本

### Q2: pip不可用

**问题**: pip命令无法执行

**解决方案**:

```bash
python3 -m ensurepip --upgrade
```

或

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### Q3: 依赖包安装失败

**问题**: pip install出错

**解决方案**:

1. 升级pip:
   ```bash
   pip3 install --upgrade pip
   ```

2. 使用国内镜像源:
   ```bash
   pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

### Q4: FFmpeg未安装

**问题**: 提示"未检测到FFmpeg"

**解决方案**:
- 按照上方"安装FFmpeg"部分的说明安装
- 安装后重启终端，确保PATH生效

### Q5: 端口被占用

**问题**: 启动时提示"Address already in use"

**解决方案**:

macOS/Linux:
```bash
lsof -ti:5000 | xargs kill -9
```

Windows:
```cmd
netstat -ano | findstr :5000
taskkill /PID <进程ID> /F
```

或者修改 `app.py` 使用其他端口:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## GPU硬件加速配置

### NVIDIA GPU (CUDA)

**要求**:
- NVIDIA显卡 (GTX/RTX系列)
- 安装CUDA驱动

**验证**:
```bash
nvidia-smi
```

### Apple Silicon (M1/M2/M3)

**要求**:
- Mac with Apple Silicon芯片
- macOS系统

**验证**:
```bash
sysctl -n machdep.cpu.brand_string
```

### AMD GPU (VAAPI)

**要求**:
- AMD显卡
- Linux系统
- FFmpeg编译时包含VAAPI支持

### Intel GPU (QSV)

**要求**:
- Intel核显或独显
- FFmpeg编译时包含QSV支持

## 系统要求

### 最低要求
- **CPU**: 双核处理器
- **内存**: 4GB RAM
- **磁盘**: 1GB可用空间
- **系统**: macOS 10.14+, Ubuntu 18.04+, Windows 10+

### 推荐配置
- **CPU**: 四核或以上
- **内存**: 8GB+ RAM
- **GPU**: 独立显卡（用于硬件加速）
- **磁盘**: SSD存储

## 项目结构

```
Batchsrt/
├── app.py                 # Flask后端主程序
├── setup.py               # Python配置脚本
├── setup.sh               # macOS/Linux一键配置
├── setup.bat              # Windows一键配置
├── requirements.txt       # Python依赖列表
├── SETUP_GUIDE.md        # 本配置指南
├── README.md             # 项目说明
└── templates/
    └── index.html        # Web界面
```

## 技术支持

如果遇到问题：

1. 查看配置器输出的错误信息
2. 参考本指南的"常见问题"部分
3. 检查系统日志
4. 确保所有依赖版本正确

## 更新依赖

更新Python依赖包：

```bash
pip3 install --upgrade -r requirements.txt
```

更新FFmpeg：

```bash
# macOS
brew upgrade ffmpeg

# Linux (Ubuntu)
sudo apt-get update && sudo apt-get upgrade ffmpeg
```

## 卸载

如果需要卸载：

1. 删除Python包：
   ```bash
   pip3 uninstall flask flask-cors
   ```

2. 删除FFmpeg：
   ```bash
   # macOS
   brew uninstall ffmpeg

   # Linux (Ubuntu)
   sudo apt-get remove ffmpeg
   ```

3. 删除项目文件夹

## 开发模式

如果需要开发或调试：

1. 安装开发依赖（如有）
2. 启用Flask调试模式（默认已启用）
3. 查看日志输出

```bash
export FLASK_DEBUG=1
python3 app.py
```

## 生产部署

生产环境建议：

1. 使用生产级WSGI服务器（如Gunicorn）:
   ```bash
   pip3 install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. 配置反向代理（如Nginx）
3. 使用HTTPS
4. 设置防火墙规则

---

**配置完成后，祝您使用愉快！**
