# 🚀 使用 GitHub 同步代码 - 完整步骤

## 🎉 太好了！你有 GitHub 账号

这意味着我们可以通过 GitHub 传输代码，完全不需要服务器访问信息！

---

## 📋 操作步骤（5 步搞定）

### 第一步：在 GitHub 创建空仓库（你操作）

#### 1.1 登录 GitHub

访问：https://github.com

#### 1.2 创建新仓库

1. 点击右上角 **"+"** 按钮
2. 选择 **"New repository"**

#### 1.3 填写仓库信息

```
Repository name: ninglawyer-miniapp
Description: 宁律师智能法律咨询小程序
```

#### 1.4 设置仓库属性

- **Public**：公开（推荐）
- **Private**：私有（如果你不想公开）

#### 1.5 创建仓库

**重要**：❌ 不要勾选以下选项
- [ ] Add a README file
- [ ] Add .gitignore
- [ ] Choose a license

保持全空，直接点击 **"Create repository"**

#### 1.6 复制仓库地址

创建后会看到这样的页面，复制你的仓库地址：

```
HTTPS: https://github.com/你的用户名/ninglawyer-miniapp.git
```

---

### 第二步：告诉我你的仓库地址（现在就做）

**请回复我你的 GitHub 仓库地址，例如：**

```
https://github.com/zhangsan/ninglawyer-miniapp.git
```

我会立即在服务器上配置并推送代码！

---

### 第三步：等待服务器推送（我操作）

收到你的仓库地址后，我会：

1. 在服务器上添加远程仓库
2. 推送代码到 GitHub
3. 告诉你推送成功

---

### 第四步：在本地克隆仓库（你操作）

推送成功后，在你的 Windows 电脑上操作：

#### 4.1 安装 Git（如果没有）

下载地址：https://git-scm.com/downloads
- 选择 Windows 版本
- 下载并安装
- 安装时全部默认选项，一路"下一步"

#### 4.2 克隆仓库

打开 **命令提示符（CMD）** 或 **PowerShell**，执行：

```bash
git clone https://github.com/你的用户名/ninglawyer-miniapp.git
```

#### 4.3 进入项目目录

```bash
cd ninglawyer-miniapp
```

#### 4.4 查看文件

```bash
dir
```

你应该能看到：
- miniprogram/
- scripts/
- src/
- config/
- assets/
- requirements.txt
- 等等...

---

### 第五步：安装依赖并启动（你操作）

#### 5.1 安装 Python 依赖

```bash
pip install -r requirements.txt
```

#### 5.2 启动后端服务

```bash
python scripts/chat_server.py
```

#### 5.3 打开微信开发者工具

1. 导入 `miniprogram` 目录
2. 勾选"不校验合法域名"
3. 点击"编译"

**完成！** 🎉

---

## 📝 完整示例

### 假设你的 GitHub 用户名是 `zhangsan`

#### 在 GitHub 创建仓库

1. 访问：https://github.com
2. 点击 "+" → "New repository"
3. 填写：
   ```
   Repository name: ninglawyer-miniapp
   Description: 宁律师智能法律咨询小程序
   ```
4. 选择：Public
5. 不勾选任何选项，直接创建
6. 复制地址：
   ```
   https://github.com/zhangsan/ninglawyer-miniapp.git
   ```

#### 在本地克隆

```bash
# 克隆仓库
git clone https://github.com/zhangsan/ninglawyer-miniapp.git

# 进入目录
cd ninglawyer-miniapp

# 安装依赖
pip install -r requirements.txt

# 启动后端
python scripts/chat_server.py
```

#### 用微信开发者工具打开

导入 `ninglawyer-miniapp/miniprogram` 目录

---

## 🔑 GitHub 认证方式

### 方式一：使用 Personal Access Token（推荐）

#### 1. 创建 Token

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 填写：
   ```
   Note: ninglawyer-miniapp
   Expiration: 90 days
   ```
4. 勾选权限：
   - [x] repo（完整仓库访问权限）
5. 点击 **"Generate token"**
6. 复制生成的 token（类似：`ghp_xxxxxxxxxxxxxxxxxxxx`）

#### 2. 在本地使用 Token

**Windows CMD：**

```bash
git clone https://你的token@github.com/你的用户名/ninglawyer-miniapp.git
```

**示例：**

```bash
git clone https://ghp_abc123xyz@github.com/zhangsan/ninglawyer-miniapp.git
```

---

### 方式二：使用 GitHub CLI（更简单）

#### 1. 安装 GitHub CLI

下载：https://cli.github.com/
- 选择 Windows 版本
- 安装到电脑

#### 2. 登录 GitHub

```bash
gh auth login
```

按照提示选择：
- What account do you want to log into? → GitHub.com
- What is your preferred protocol for Git operations? → HTTPS
- Authenticate with a GitHub.com device code → 按提示操作

#### 3. 克隆仓库

```bash
gh repo clone 你的用户名/ninglawyer-miniapp
```

---

## ✅ 检查清单

在开始之前，请确认：

- [ ] 你有 GitHub 账号 ✅
- [ ] 你已登录 GitHub
- [ ] 你知道如何创建仓库
- [ ] 你准备好告诉我仓库地址

---

## ⏱️ 预计时间

| 步骤 | 需要时间 |
|------|---------|
| 创建 GitHub 仓库 | 2 分钟 |
| 等待我配置并推送 | 2-5 分钟 |
| 在本地克隆 | 1-2 分钟 |
| 安装依赖 | 3-5 分钟 |
| **总计** | **10-15 分钟** |

---

## 🆘 常见问题

### Q1: 创建仓库时出错

**A:** 检查：
- 仓库名是否合法（只能包含字母、数字、连字符、下划线）
- 仓库名是否重复（GitHub 上唯一）

### Q2: 克隆失败

**A:** 检查：
- 仓库地址是否正确
- 是否有访问权限（如果是私有仓库）
- 是否需要使用 Token 认证

### Q3: pip install 失败

**A:** 解决方案：
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q4: 微信开发者工具导入失败

**A:** 检查：
- 导入的是 `miniprogram` 目录，不是根目录
- `miniprogram` 目录下是否有 `app.js` 文件
- 是否勾选了"不校验合法域名"

### Q5: 不知道怎么安装 Git

**A:** 详细步骤：
1. 访问：https://git-scm.com/downloads
2. 下载 Windows 版本
3. 双击安装程序
4. 全部默认选项，一路"下一步"
5. 安装完成后，打开 CMD，输入：
   ```bash
   git --version
   ```
   如果显示版本号，说明安装成功！

---

## 🎯 下一步操作

### 现在你需要做的：

1. ✅ **登录 GitHub**（如果还没登录）
2. ✅ **创建新仓库**：
   - 名字：`ninglawyer-miniapp`
   - 描述：`宁律师智能法律咨询小程序`
   - 不勾选任何选项，直接创建
3. ✅ **复制仓库地址**
4. ✅ **回复我仓库地址**，例如：
   ```
   https://github.com/你的用户名/ninglawyer-miniapp.git
   ```

### 收到你的仓库地址后，我会：

1. 在服务器上配置远程仓库
2. 推送代码到 GitHub
3. 告诉你推送成功
4. 你就可以在本地克隆了！

---

## 🚀 现在就去创建仓库吧！

1. 访问：https://github.com
2. 点击 "+" → "New repository"
3. 创建仓库
4. 复制地址
5. 告诉我！

**预计 10-15 分钟后，你就可以在本地开发宁律师小程序了！** 🎉
