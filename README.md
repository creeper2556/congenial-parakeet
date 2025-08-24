# 定时关机提醒程序 Shutdown Reminder

一个使用Python开发的定时关机提醒应用程序，支持GUI和命令行两种界面，并通过GitHub Actions自动打包为可执行文件。

A scheduled shutdown reminder application developed in Python, supporting both GUI and command-line interfaces, with automatic executable packaging via GitHub Actions.

## 功能特性 Features

- 🕒 **自定义提醒时间** Custom reminder time setting
- 💻 **跨平台支持** Cross-platform support (Windows/Linux/macOS)
- 🖥️ **双界面支持** Both GUI and CLI versions available
- ⚠️ **安全确认** Safe shutdown confirmation with countdown
- ⏰ **灵活控制** Delay and cancel options
- 📦 **自动打包** Automatic executable packaging via GitHub Actions
- 🔄 **每日定时关机** Daily recurring shutdown functionality
- ⚙️ **配置持久化** Persistent configuration storage
- 🤖 **后台模式** Background daemon mode for unattended operation

## 使用方法 Usage

### GUI版本 (推荐 Recommended)

1. 运行 `shutdown_reminder.py`
2. 选择运行模式:
   - **单次关机提醒**: 设置一次性关机提醒
   - **每日定时关机**: 设置每天定时关机
3. 在界面中设置提醒时间（小时和分钟）
4. 每日模式可选择启用自动关机（无需用户确认）
5. 点击"开始提醒"启动定时器
6. 到达设定时间时会弹出提醒窗口

```bash
python shutdown_reminder.py
```

### 命令行版本 CLI Version

1. 运行 `shutdown_reminder_cli.py`
2. 选择运行模式:
   - **1. 单次关机提醒**: 传统的一次性提醒模式
   - **2. 每日定时关机**: 每天定时关机（需先配置）
   - **3. 配置每日关机**: 设置每日关机时间和选项
   - **4. 显示配置信息**: 查看当前每日关机配置
   - **5. 退出程序**: 退出应用
   - **6. 启动每日后台模式**: 后台运行每日关机（仅配置后可见）
3. 每日模式支持自动关机和后台运行
4. 配置信息自动保存，重启后仍然有效

```bash
python shutdown_reminder_cli.py
```

#### 每日模式配置示例 Daily Mode Configuration Example

```bash
# 配置每日23:30关机，启用自动关机
python shutdown_reminder_cli.py
选择选项 3 -> 设置时间 23:30 -> 选择 y (启用自动关机)

# 启动每日后台模式
python shutdown_reminder_cli.py
选择选项 6 -> 程序将在后台运行，每天23:30自动关机
```

## 安装依赖 Dependencies

本程序只使用Python标准库，无需额外安装依赖：
This program only uses Python standard libraries, no additional dependencies required:

- `tkinter` - GUI界面 (内置)
- `datetime`, `threading`, `time` - 时间和线程处理
- `subprocess`, `platform` - 系统调用
- `signal`, `os` - 系统信号处理

## 下载可执行文件 Download Executables

可以从 [Releases](https://github.com/creeper2556/congenial-parakeet/releases) 页面下载预编译的可执行文件：

You can download pre-compiled executables from the [Releases](https://github.com/creeper2556/congenial-parakeet/releases) page:

- **Windows**: `shutdown-reminder-windows.zip`
- **Linux**: `shutdown-reminder-linux.tar.gz`  
- **macOS**: `shutdown-reminder-macos.tar.gz`

## 构建说明 Build Instructions

### 本地构建 Local Build

使用 PyInstaller 构建可执行文件：
Use PyInstaller to build executables:

```bash
# 安装 PyInstaller
pip install pyinstaller

# 构建 CLI 版本
pyinstaller --onefile --console shutdown_reminder_cli.py

# 构建 GUI 版本
pyinstaller --onefile --windowed shutdown_reminder.py
```

### 自动构建 Automatic Build

代码推送到主分支后，GitHub Actions 会自动：
After pushing code to the main branch, GitHub Actions will automatically:

1. 在 Windows/Linux/macOS 上构建可执行文件
2. 运行基本测试验证程序功能
3. 将构建产物上传为 artifacts
4. 如果是标签推送，则创建 release 并上传文件

## 安全说明 Security Notes

⚠️ **重要警告 Important Warning**

此程序具有关闭计算机的能力，请谨慎使用：
This application has the ability to shut down your computer, use with caution:

- 程序会在执行关机前进行多重确认
- 提供倒计时和取消选项
- 建议先使用测试功能验证程序行为
- 不建议设置过短的提醒时间

## 系统支持 System Support

| 操作系统 OS | GUI支持 | CLI支持 | 关机命令 Shutdown Command |
|------------|---------|---------|---------------------------|
| Windows    | ✅      | ✅      | `shutdown /s /t 1`        |
| Linux      | ✅*     | ✅      | `shutdown -h +1`          |
| macOS      | ✅      | ✅      | `sudo shutdown -h +1`     |

*Linux GUI 需要安装 tkinter: `sudo apt-get install python3-tk`

## 开发 Development

### 项目结构 Project Structure

```
congenial-parakeet/
├── shutdown_reminder.py          # GUI版本主程序
├── shutdown_reminder_cli.py      # CLI版本主程序
├── daily_shutdown_config.py      # 每日关机配置管理
├── test_shutdown_reminder.py     # 基础功能测试
├── test_daily_functionality.py   # 每日功能测试
├── requirements.txt              # 依赖文件（空，使用标准库）
├── .github/workflows/build.yml   # GitHub Actions 构建配置
├── .gitignore                   # Git忽略文件
└── README.md                    # 项目文档
```

### 配置文件 Configuration File

每日关机配置保存在用户家目录下的 `~/.shutdown_reminder_config.json` 文件中：

```json
{
  "daily_mode_enabled": true,
  "daily_shutdown_hour": 23,
  "daily_shutdown_minute": 30,
  "auto_shutdown": false,
  "last_updated": "2025-01-01T23:30:00.000000"
}
```

### 测试 Testing

```bash
# 测试基础功能
python test_shutdown_reminder.py

# 测试每日功能
python test_daily_functionality.py

# 测试导入
python -c "import datetime, threading, time, subprocess, platform"

# 测试GUI（如果可用）
python -c "import tkinter; print('GUI available')"

# 运行程序测试
python shutdown_reminder_cli.py
```

## 许可证 License

MIT License - 详见 LICENSE 文件

## 贡献 Contributing

欢迎提交 Issue 和 Pull Request！
Issues and Pull Requests are welcome!

## 更新日志 Changelog

### v1.1.0 - 每日定时关机功能 Daily Shutdown Feature
- ✨ 新增每日定时关机功能
- ✨ 新增配置持久化存储
- ✨ 新增后台守护进程模式
- ✨ 新增自动关机模式（无需用户确认）
- ✨ GUI版本支持单次/每日模式切换
- ✨ CLI版本支持丰富的菜单选项
- 🐛 改进错误处理和用户体验

### v1.0.0 - 初始版本 Initial Release
- 初始版本发布
- GUI 和 CLI 双界面支持
- 跨平台关机功能
- GitHub Actions 自动打包
