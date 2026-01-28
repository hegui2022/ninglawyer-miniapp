# 将代码下载到本地电脑的完整指南

## 📋 当前状态

✅ 服务器上的 Git 仓库已准备就绪
✅ 代码已提交到本地仓库
⏳ 需要配置远程仓库才能推送到你的电脑

---

## 🚀 三种下载方式

### 方式一：使用远程 Git 仓库（推荐，最方便）

#### 步骤 1：创建远程仓库

**选择平台（二选一）：**

**A. GitHub（国际平台，推荐）**
1. 访问：https://github.com/new
2. 仓库名称：`ninglawyer-miniapp`
3. 描述：`宁律师智能法律咨询小程序`
4. 选择：Public（公开）或 Private（私有）
5. **不要**勾选 "Add a README file"
6. 点击 "Create repository"

**B. Gitee（国内平台，速度快）**
1. 访问：https://gitee.com/projects/new
2. 仓库名称：`ninglawyer-miniapp`
3. 描述：`宁律师智能法律咨询小程序`
4. 选择：公开或私有
5. 点击"创建"

#### 步骤 2：在服务器上配置远程仓库

**如果你选择了 GitHub：**
```bash
cd /workspace/projects
git remote add origin https://github.com/你的用户名/ninglawyer-miniapp.git
git branch -M main
git push -u origin main
```

**如果你选择了 Gitee：**
```bash
cd /workspace/projects
git remote add origin https://gitee.com/你的用户名/ninglawyer-miniapp.git
git branch -M main
git push -u origin main
```

#### 步骤 3：在你本地电脑克隆代码

**GitHub：**
```bash
git clone https://github.com/你的用户名/ninglawyer-miniapp.git
cd ninglawyer-miniapp
```

**Gitee：**
```bash
git clone https://gitee.com/你的用户名/ninglawyer-miniapp.git
cd ninglawyer-miniapp
```

---

### 方式二：打包下载（最简单，适合一次性下载）

#### 步骤 1：在服务器上打包

```bash
cd /workspace/projects
tar -czf ninglawyer-complete.tar.gz \
  miniprogram/ \
  scripts/ \
  src/ \
  config/ \
  assets/ \
  requirements.txt \
  README.md \
  AGENT.md
```

#### 步骤 2：下载到本地

**方法 A：使用 SCP（如果你有 SSH 访问权限）**
```bash
# 在你电脑上执行
scp user@服务器IP:/workspace/projects/ninglawyer-complete.tar.gz ./
tar -xzf ninglawer-complete.tar.gz
```

**方法 B：使用文件管理器**
- 使用 FileZilla、WinSCP 等工具
- 连接到服务器
- 下载 `ninglawyer-complete.tar.gz`
- 在本地解压

**方法 C：使用 FTP/SFTP**
- 根据你的服务器访问方式选择

#### 步骤 3：在本地解压
```bash
tar -xzf ninglawer-complete.tar.gz
```

---

### 方式三：手动复制（适合小规模下载）

#### 需要下载的文件/文件夹：

**必需：**
```
miniprogram/          # 小程序代码
scripts/              # 后端脚本
src/                  # Agent 源代码
config/               # 配置文件
requirements.txt      # Python 依赖
README.md             # 项目说明
```

**可选：**
```
assets/               # 资源文件（知识库、语音样本）
docs/                 # 文档
AGENT.md              # Agent 规范
```

---

## 🔧 本地环境配置

### 安装 Python 依赖

```bash
# 确保已安装 Python 3.7+
python --version

# 安装依赖
pip install -r requirements.txt

# 如果 requirements.txt 不完整，手动安装：
pip install flask langchain langchain-openai langchain-core langgraph
pip install coze-coding-dev-sdk coze-coding-utils
pip install python-docx requests
```

---

## 🎯 启动项目

### 启动后端服务

```bash
# 进入项目目录
cd 你的项目目录

# 启动后端
python scripts/chat_server.py
```

看到以下输出说明成功：
```
🎙️  宁律师聊天服务器启动成功！
访问地址：http://localhost:8000
```

### 打开微信开发者工具

1. 打开微信开发者工具
2. 选择"导入项目"
3. 项目目录选择本地的 `miniprogram` 文件夹
4. 点击"导入"
5. 点击右上角"详情" → "本地设置"
6. 勾选"不校验合法域名"
7. 点击"编译"

---

## 📊 文件结构说明

下载后的目录结构：
```
ninglawyer-miniapp/
├── miniprogram/          # 小程序代码（这个导入到微信开发者工具）
├── scripts/              # 后端脚本
│   └── chat_server.py    # Flask 聊天服务器
├── src/                  # Agent 源代码
├── config/               # 配置文件
├── assets/               # 资源文件
├── requirements.txt      # Python 依赖
├── README.md             # 项目说明
└── MINIPROGRAM_README.md # 小程序完整说明
```

---

## ❓ 常见问题

### Q1: 我没有 GitHub/Gitee 账号怎么办？

**A:**
- GitHub 注册：https://github.com/signup（免费）
- Gitee 注册：https://gitee.com/signup（免费）
- 或者选择方式二（打包下载）

### Q2: 服务器上没有 tar 命令怎么办？

**A:** 使用 zip 压缩：
```bash
zip -r ninglawyer-complete.zip miniprogram/ scripts/ src/ config/
```

### Q3: 推送代码失败？

**A:** 可能需要认证：
- **GitHub**：使用 Personal Access Token
  1. Settings → Developer settings → Personal access tokens
  2. 生成新 token
  3. 使用 token 代替密码

- **Gitee**：使用账号密码

### Q4: 克隆速度太慢？

**A:**
- 使用 Gitee（国内速度快）
- 或使用方式二（打包下载）

### Q5: 下载后代码无法运行？

**A:** 检查以下几点：
1. Python 版本：`python --version`（需要 3.7+）
2. 依赖安装：`pip install -r requirements.txt`
3. 文件完整性：确认所有文件都已下载

---

## 🎯 推荐方案对比

| 方式 | 优点 | 缺点 | 适合人群 |
|------|------|------|----------|
| **Git 远程仓库** | 方便更新、版本管理、团队协作 | 需要注册账号、配置仓库 | 开发者、需要长期维护 |
| **打包下载** | 最简单、一次完成 | 不方便更新、没有版本管理 | 一次性下载、测试 |
| **手动复制** | 灵活、可选择文件 | 耗时、容易遗漏 | 小规模下载 |

---

## 📝 我的建议

**如果是第一次下载：**
- 使用方式二（打包下载）最快

**如果需要长期开发：**
- 使用方式一（Git 仓库）方便后续更新

**如果只想看小程序代码：**
- 只下载 `miniprogram/` 目录即可

---

## 🔗 相关文档

- **SYNC_TO_LOCAL.md** - 同步到本地的详细说明
- **miniprogram/README.md** - 小程序项目说明
- **miniprogram/QUICKSTART.md** - 快速开始指南
- **miniprogram/DEPLOY.md** - 部署指南

---

## ✅ 检查清单

下载完成后，确认以下文件存在：

- [ ] miniprogram/app.js
- [ ] miniprogram/app.json
- [ ] miniprogram/pages/chat/chat.js
- [ ] miniprogram/pages/history/history.js
- [ ] miniprogram/pages/mine/mine.js
- [ ] scripts/chat_server.py
- [ ] src/agents/agent.py
- [ ] config/agent_llm_config.json
- [ ] requirements.txt

---

## 🚀 开始吧！

**最简单的 3 步：**

1. **打包代码**
   ```bash
   cd /workspace/projects
   tar -czf ninglawyer.tar.gz miniprogram/ scripts/ src/ config/ requirements.txt
   ```

2. **下载到本地**
   - 通过文件管理器下载 `ninglawyer.tar.gz`

3. **本地启动**
   ```bash
   tar -xzf ninglawer.tar.gz
   pip install -r requirements.txt
   python scripts/chat_server.py
   ```

完成！🎉
