# 自动化工具配置与使用指南

## 🚀 快速开始

### 第一步：配置路径

**首次使用时，必须先配置路径！**

双击运行 `config-wizard.bat`，按照提示配置：

1. **项目路径** - ninglawyer-miniapp 项目所在目录
2. **微信开发者工具路径** - 微信开发者工具 cli.bat 所在路径
3. **监控间隔** - 实时监控的检查间隔（秒）

### 第二步：启动自动化工具

双击运行 `start.bat`，选择您需要的功能：

```
[1] 启动实时监控（每 30 秒检查一次）
[2] 立即同步最新代码
[3] 查看最近提交记录
[4] 打开微信开发者工具
[5] 快速提交代码
[6] 配置路径
[0] 退出
```

---

## 📚 功能详解

### 1. 实时监控

**用途**：自动监控代码更新，发现新代码后自动拉取并刷新微信开发者工具。

**使用方法**：
- 运行 `start.bat`，选择 [1]
- 或直接运行 `monitor.bat` / `monitor.py`

**工作原理**：
- 每 30 秒检查一次远程仓库
- 发现新提交后自动拉取
- 自动刷新所有小程序项目（legal-instructor, code-signing, lyue, zenme-pan）

**停止监控**：按 `Ctrl+C`

**配置**：在 `sync-config.ini` 中修改 `MONITOR_INTERVAL` 调整监控间隔。

---

### 2. 立即同步

**用途**：立即拉取最新代码并刷新微信开发者工具。

**使用方法**：
- 运行 `start.bat`，选择 [2]
- 或直接运行 `sync.bat`
- 或直接运行 `auto-sync.bat`

**工作流程**：
1. 检查远程仓库是否有新提交
2. 如果有新提交，显示提交信息
3. 拉取最新代码
4. 刷新微信开发者工具

---

### 3. 快速提交

**用途**：快速提交代码到远程仓库。

**使用方法**：
- 运行 `start.bat`，选择 [5]
- 或直接运行 `quick-commit.bat`

**工作流程**：
1. 自动添加所有更改
2. 显示更改的文件列表
3. 提示输入提交信息
4. 提交代码
5. 推送到远程仓库

---

### 4. 查看提交记录

**用途**：查看最近 5 次提交记录。

**使用方法**：
- 运行 `start.bat`，选择 [3]

---

### 5. 打开微信开发者工具

**用途**：快速打开法律教官小程序。

**使用方法**：
- 运行 `start.bat`，选择 [4]

---

### 6. 配置路径

**用途**：重新配置项目路径和微信开发者工具路径。

**使用方法**：
- 运行 `start.bat`，选择 [6]
- 或直接运行 `config-wizard.bat`

---

## ⚙️ 配置文件详解

配置文件：`sync-config.ini`

```ini
[General]
# 项目路径（必须修改）
PROJECT_PATH=C:\Users\YourName\ninglawyer-miniapp

# 监控间隔（秒），默认 30 秒
MONITOR_INTERVAL=30

[Git]
# Git 仓库地址
REPO_URL=https://github.com/hegui2022/ninglawyer-miniapp.git

# 分支名称
BRANCH=main

[WeChatDevTools]
# 微信开发者工具路径（必须修改）
# Windows 默认路径
WIN_PATH=C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat

# macOS 默认路径
MAC_PATH=/Applications/wechatwebdevtools.app/Contents/MacOS/cli

[Notifications]
# 是否启用通知（true/false）
ENABLE_NOTIFICATION=true

# 通知方式：console/terminal-notifier/osascript
NOTIFICATION_METHOD=console

[Projects]
# 需要刷新的小程序项目（逗号分隔）
PROJECTS=legal-instructor,code-signing,lyue,zenme-pan
```

### 配置项说明

| 配置项 | 说明 | 是否必须 |
|--------|------|---------|
| `PROJECT_PATH` | 项目根目录路径 | ✅ 必须 |
| `MONITOR_INTERVAL` | 监控间隔（秒） | ❌ 可选 |
| `REPO_URL` | Git 仓库地址 | ❌ 可选 |
| `BRANCH` | 分支名称 | ❌ 可选 |
| `WIN_PATH` | 微信开发者工具 cli.bat 路径 | ✅ 必须 |
| `MAC_PATH` | macOS 微信开发者工具路径 | ❌ 可选 |
| `ENABLE_NOTIFICATION` | 是否启用通知 | ❌ 可选 |
| `NOTIFICATION_METHOD` | 通知方式 | ❌ 可选 |
| `PROJECTS` | 需要刷新的小程序列表 | ❌ 可选 |

---

## 🔧 常见问题

### 1. 运行脚本时提示"项目路径不存在"

**原因**：配置文件中的 `PROJECT_PATH` 路径不正确。

**解决方法**：
1. 运行 `config-wizard.bat`
2. 输入正确的项目路径
3. 例如：`C:\Users\YourName\Documents\ninglawyer-miniapp`

---

### 2. 运行脚本时提示"微信开发者工具路径不存在"

**原因**：配置文件中的 `WIN_PATH` 路径不正确。

**解决方法**：
1. 找到微信开发者工具的安装位置
2. 通常在以下位置：
   - `C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat`
   - `C:\Program Files\Tencent\微信web开发者工具\cli.bat`
   - `D:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat`
3. 运行 `config-wizard.bat`，输入正确的路径

---

### 3. 微信开发者工具没有自动刷新

**原因**：
1. 微信开发者工具路径配置错误
2. 微信开发者工具未安装命令行工具

**解决方法**：
1. 确认微信开发者工具路径正确
2. 确保微信开发者工具已安装命令行工具（通常默认安装）
3. 如果仍不工作，手动在微信开发者工具中按 `Ctrl+S` 刷新

---

### 4. 实时监控无法启动

**原因**：缺少 Python 或 monitor.py 文件

**解决方法**：
1. 确保已安装 Python 3.x
2. 确保项目根目录下有 `monitor.py` 文件
3. 如果没有 monitor.py，可以使用 `monitor.bat` 作为替代

---

### 5. 提交代码时提示"没有需要提交的更改"

**原因**：当前没有文件更改

**解决方法**：
1. 检查是否有文件修改
2. 运行 `git status` 查看状态

---

## 💡 高级用法

### 自定义监控间隔

编辑 `sync-config.ini`：

```ini
[General]
# 每 60 秒检查一次
MONITOR_INTERVAL=60
```

### 只刷新特定小程序

编辑 `sync-config.ini`：

```ini
[Projects]
# 只刷新 legal-instructor
PROJECTS=legal-instructor
```

### 手动刷新特定小程序

```bash
"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat" open --project C:\path\to\legal-instructor
```

---

## 📋 脚本列表

| 脚本 | 用途 |
|------|------|
| `config-wizard.bat` | 配置向导 |
| `start.bat` | 一键启动菜单 |
| `auto-sync.bat` | 自动同步代码 |
| `sync.bat` | 同步代码 |
| `quick-commit.bat` | 快速提交 |
| `monitor.bat` | 实时监控（批处理版） |
| `monitor.py` | 实时监控（Python 版） |

---

## 🎯 使用场景

### 场景 1：日常开发

1. 启动实时监控（`start.bat` → [1]）
2. 修改代码
3. 自动同步到其他设备
4. 微信开发者工具自动刷新

### 场景 2：多人协作

1. 团队成员提交代码到 GitHub
2. 您的电脑自动检测到新代码
3. 自动拉取并刷新微信开发者工具
4. 立即看到最新的更改

### 场景 3：快速提交

1. 修改代码
2. 运行 `quick-commit.bat`
3. 输入提交信息
4. 自动提交并推送

---

## 📞 技术支持

如果遇到问题：

1. 检查配置文件 `sync-config.ini` 是否正确
2. 运行 `config-wizard.bat` 重新配置
3. 查看 GitHub Issues
4. 联系开发团队

---

## ✅ 最佳实践

1. **首次使用**：先运行 `config-wizard.bat` 配置路径
2. **日常开发**：保持实时监控开启
3. **提交代码**：使用 `quick-commit.bat` 快速提交
4. **查看日志**：定期查看提交记录，了解项目进展
5. **多设备同步**：在每台设备上配置自动化工具

---

**享受高效的开发体验！** 🚀
