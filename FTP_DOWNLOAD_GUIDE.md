# 📥 使用文件管理器下载文件详细教程

## 🎯 准备工作

### 你需要知道的信息：

在开始之前，你需要向服务器管理员获取以下信息：

- ✅ **服务器 IP 地址**（如：192.168.1.100）
- ✅ **用户名**（如：root）
- ✅ **密码**（你的登录密码）
- ✅ **端口**（通常是 22，SSH/SFTP 端口）

**如果不知道这些信息，请询问服务器管理员。**

---

## 📦 文件信息

- **文件名**：`ninglawyer-miniapp.tar.gz`
- **文件位置**：`/workspace/projects/ninglawyer-miniapp.tar.gz`
- **文件大小**：9.5MB

---

## 🛠️ 方式一：使用 FileZilla（推荐）

### 第一步：下载 FileZilla

1. 访问官网：https://filezilla-project.org/download.php
2. 下载 FileZilla Client
3. 安装到你的电脑（Windows/Mac/Linux）

### 第二步：连接到服务器

1. 打开 FileZilla

2. 在顶部输入框填写信息：

```
主机: 你的服务器IP地址
用户名: 你的用户名（如 root）
密码: 你的密码
端口: 22
```

3. 点击"快速连接"按钮

### 第三步：浏览文件

1. 连接成功后，右侧是"远程站点"（服务器文件）
2. 找到 `/workspace/projects/` 目录
3. 找到 `ninglawyer-miniapp.tar.gz` 文件

### 第四步：下载文件

**方法 A：右键下载**
1. 右键点击 `ninglawer-miniapp.tar.gz`
2. 选择"下载"
3. 文件会下载到你的本地电脑（默认在"我的文档"）

**方法 B：拖拽下载**
1. 找到左侧"本地站点"（你的电脑）
2. 选择你要保存的文件夹
3. 从右侧拖拽 `ninglawer-miniapp.tar.gz` 到左侧

### 第五步：等待下载完成

- 9.5MB 的文件，下载很快（通常几秒到几分钟）
- 底部会显示下载进度

---

## 🛠️ 方式二：使用 WinSCP（Windows 用户推荐）

### 第一步：下载 WinSCP

1. 访问官网：https://winscp.net/eng/download.php
2. 下载 WinSCP（免费）
3. 安装到你的电脑

### 第二步：新建站点

1. 打开 WinSCP
2. 点击"新建站点"

3. 填写信息：
```
文件协议: SFTP
主机名: 你的服务器IP
端口: 22
用户名: 你的用户名（如 root）
密码: 你的密码
```

4. 点击"保存"
5. 点击"登录"

### 第三步：浏览文件

1. 登录成功后，右侧是远程服务器文件
2. 导航到 `/workspace/projects/`
3. 找到 `ninglawer-miniapp.tar.gz`

### 第四步：下载文件

**方法 A：右键下载**
1. 右键点击文件
2. 选择"下载"
3. 选择保存位置
4. 点击"确定"

**方法 B：拖拽下载**
1. 从右侧拖拽文件到左侧（本地文件夹）

### 第五步：等待下载完成

- 底部显示下载进度
- 下载完成后会有提示

---

## 🛠️ 方式三：使用 MobaXterm（功能强大）

### 下载 MobaXterm

1. 访问：https://mobaxterm.mobatek.net/download.html
2. 下载免费版（Home Edition）
3. 安装到电脑

### 连接和下载

1. 打开 MobaXterm
2. 点击"Session" → "SFTP"
3. 填写服务器信息
4. 连接后，直接在文件浏览器中右键下载

---

## 🔍 如果不知道 FTP 访问信息

### 检查是否有 SSH 访问权限

如果你可以 SSH 登录服务器，就可以使用 SFTP 下载：

**测试 SSH 连接：**
```bash
ssh 用户名@服务器IP
```

如果可以登录，说明有 SFTP 访问权限。

---

## 📋 连接信息示例

假设你的服务器信息如下：

```
服务器 IP: 123.45.67.89
用户名: root
密码: your_password_here
端口: 22
文件路径: /workspace/projects/ninglawyer-miniapp.tar.gz
```

在 FileZilla 中填写：

```
主机: 123.45.67.89
用户名: root
密码: your_password_here
端口: 22
```

---

## ❓ 常见问题

### Q1: 连接失败，提示"连接被拒绝"

**A:** 检查以下几点：
1. 服务器 IP 地址是否正确
2. 端口是否正确（通常是 22）
3. 服务器是否允许外部连接
4. 防火墙是否阻止了连接

### Q2: 登录失败，提示"认证失败"

**A:** 检查以下几点：
1. 用户名和密码是否正确
2. 是否需要使用 SSH 密钥而非密码
3. 是否需要使用特殊端口

### Q3: 找不到文件

**A:** 检查以下几点：
1. 文件路径是否正确：`/workspace/projects/`
2. 文件名是否正确：`ninglawer-miniapp.tar.gz`
3. 文件是否已被删除

### Q4: 下载速度慢

**A:** 可能的原因：
1. 网络带宽限制
2. 服务器带宽限制
3. 使用国内镜像（如果服务器在国外）

### Q5: 没有 FTP/SFTP 访问权限

**A:** 替代方案：
1. 使用 SCP 命令下载
2. 请求管理员发送文件
3. 使用其他方式传输（如网盘）

---

## 🔄 替代方案：使用 SCP 命令

如果你有 SSH 访问权限，可以使用命令行下载：

### Windows（PowerShell/CMD）

```bash
scp root@你的服务器IP:/workspace/projects/ninglawyer-miniapp.tar.gz ./
```

### Mac/Linux

```bash
scp root@你的服务器IP:/workspace/projects/ninglawer-miniapp.tar.gz ./
```

### 示例

```bash
scp root@123.45.67.89:/workspace/projects/ninglawer-miniapp.tar.gz ./
```

下载后会提示输入密码。

---

## 📱 替代方案：使用 VS Code Remote SSH

### 安装扩展

1. 打开 VS Code
2. 安装 "Remote - SSH" 扩展
3. 连接到服务器
4. 在左侧资源管理器中找到文件
5. 右键 → "Download"

---

## 📦 下载后的操作

### 1. 解压文件

```bash
# Windows (使用 7-Zip 或 WinRAR)
# 右键 → "解压到 ninglawyer-miniapp"

# Mac/Linux
tar -xzf ninglawer-miniapp.tar.gz
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动后端

```bash
python scripts/chat_server.py
```

### 4. 打开微信开发者工具

1. 导入 `miniprogram` 目录
2. 勾选"不校验合法域名"
3. 点击"编译"

---

## 🎯 推荐工具对比

| 工具 | 平台 | 优点 | 缺点 | 推荐度 |
|------|------|------|------|--------|
| **FileZilla** | 全平台 | 免费、简单、功能全 | 界面老旧 | ⭐⭐⭐⭐⭐ |
| **WinSCP** | Windows | 简洁、支持编辑 | 仅 Windows | ⭐⭐⭐⭐⭐ |
| **MobaXterm** | Windows | 功能强大、集成度高 | 较复杂 | ⭐⭐⭐⭐ |
| **SCP 命令** | 全平台 | 快速、无需安装 | 需要命令行 | ⭐⭐⭐⭐ |

---

## ✅ 下载检查清单

下载完成后，检查：

- [ ] 文件大小约为 9.5MB
- [ ] 文件可以正常解压
- [ ] 解压后有 miniprogram/ 文件夹
- [ ] 解压后有 scripts/ 文件夹
- [ ] 解压后有 src/ 文件夹
- [ ] 解压后有 config/ 文件夹

---

## 🆘 如果还是无法下载

### 请提供以下信息：

1. **你使用的是哪个操作系统？**（Windows/Mac/Linux）
2. **你尝试过什么方式？**（FileZilla/WinSCP/其他）
3. **遇到了什么错误？**（完整的错误提示）
4. **你知道服务器访问信息吗？**（IP、用户名、密码）

### 或者尝试其他方式：

1. **使用 SCP 命令**（如果有 SSH 访问权限）
2. **请求管理员发送文件**（通过网盘、邮件等）
3. **使用 Git 克隆**（如果有远程仓库）

---

## 📞 需要帮助？

如果遇到问题，请告诉我：
1. 你使用的是什么工具？
2. 具体的错误提示是什么？
3. 你尝试了什么操作？

我会帮你解决！

---

## 🚀 开始下载吧！

**推荐使用 FileZilla 或 WinSCP：**

1. 下载工具（FileZilla：https://filezilla-project.org/）
2. 填写服务器信息
3. 找到文件
4. 下载到本地

祝你下载顺利！💪
