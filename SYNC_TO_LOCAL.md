# 将代码同步到本地电脑的步骤

## 方式一：使用 Git（推荐）

### 1. 在服务器上提交代码

```bash
cd /workspace/projects
git add .
git commit -m "feat: 完成宁律师小程序开发"
```

### 2. 推送到远程仓库（需要先创建远程仓库）

```bash
# 在 GitHub/Gitee 上创建一个新仓库
# 然后执行以下命令：

git remote add origin <你的仓库地址>
git branch -M main
git push -u origin main
```

### 3. 在本地电脑克隆代码

```bash
# 在你电脑上执行
git clone <你的仓库地址>
cd 项目目录
```

### 4. 本地启动后端

```bash
# 确保已安装 Python 3.7+
pip install -r requirements.txt

# 启动后端服务
python scripts/chat_server.py
```

### 5. 打开微信开发者工具

```
1. 打开微信开发者工具
2. 选择"导入项目"
3. 项目目录选择本地的 miniprogram 文件夹
4. 点击"导入"
5. 勾选"不校验合法域名"
6. 点击"编译"
```

---

## 方式二：手动下载（快速方式）

### 1. 打包小程序代码

```bash
# 在服务器上执行
cd /workspace/projects
tar -czf miniprogram.tar.gz miniprogram/
```

### 2. 下载到本地

**如果你有 SSH 访问权限：**
```bash
# 在你电脑上执行
scp user@server:/workspace/projects/miniprogram.tar.gz ./
tar -xzf miniprogram.tar.gz
```

**或者：**
- 通过文件管理器（如 FileZilla）下载 `miniprogram.tar.gz`
- 在本地解压

### 3. 下载后端代码

同样方式下载：
- `src/` 目录
- `scripts/` 目录
- `config/` 目录
- `assets/` 目录（可选）
- `requirements.txt`

### 4. 本地启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端
python scripts/chat_server.py

# 打开微信开发者工具导入 miniprogram 目录
```

---

## 方式三：使用 VS Code Remote SSH

### 1. 安装 VS Code Remote SSH 扩展

在 VS Code 中安装 "Remote - SSH" 扩展

### 2. 配置 SSH 连接

编辑 `~/.ssh/config`：
```
Host your-server
    HostName 你的服务器IP
    User 用户名
    Port 22
```

### 3. 连接到服务器

```
1. 按 F1，输入 "Remote-SSH: Connect to Host"
2. 选择你的服务器
3. 编辑代码
4. 使用本地终端启动后端
```

---

## 本地环境配置

### 安装 Python 依赖

```bash
pip install flask langchain langchain-openai langchain-core langgraph langgraph-checkpoint-memory
pip install coze-coding-dev-sdk coze-coding-utils
pip install python-docx requests
```

### 配置环境变量（可选）

创建 `.env` 文件：
```env
FLASK_APP=scripts/chat_server.py
FLASK_ENV=development
```

---

## 测试流程

### 1. 启动后端

```bash
python scripts/chat_server.py
```

看到以下输出说明成功：
```
🎙️  宁律师聊天服务器启动成功！
访问地址：http://localhost:8000
```

### 2. 打开微信开发者工具

```
1. 导入 miniprogram 目录
2. 勾选"不校验合法域名"
3. 点击"编译"
```

### 3. 测试功能

- ✅ 输入文本："你好，宁律师"
- ✅ 点击发送
- ✅ 查看回复
- ✅ 点击快捷标签
- ✅ 查看历史记录

---

## 常见问题

### Q1: 下载代码时出错？

A: 确保服务器有足够的权限，或者联系管理员获取访问权限

### Q2: 本地启动后端失败？

A: 检查 Python 版本和依赖是否安装正确：
```bash
python --version  # 需要 3.7+
pip list  # 查看已安装的包
```

### Q3: 小程序无法连接后端？

A: 检查以下几点：
1. 后端服务是否启动
2. `miniprogram/app.js` 中的 `baseUrl` 是否正确
3. 是否勾选了"不校验合法域名"

### Q4: 想同时用服务器和本地？

A: 可以：
- 服务器上运行后端
- 本地运行小程序
- 修改 `miniprogram/app.js` 的 `baseUrl` 为服务器地址

---

## 推荐开发流程

### 日常开发

```
1. 在本地编辑代码
2. 启动后端：python scripts/chat_server.py
3. 打开微信开发者工具测试
4. 提交代码：git add . && git commit -m "描述"
5. 推送到远程：git push
```

### 团队协作

```
1. 每个人从远程仓库克隆
2. 创建分支：git checkout -b feature/xxx
3. 开发完成后提交
4. 发起 Pull Request
5. 合并到主分支
```

---

## 快速开始总结

**最简单的方式（3步）：**

1. **下载代码**
   ```bash
   # 方式 A: Git 克隆
   git clone <仓库地址>

   # 方式 B: 手动下载 miniprogram 目录
   ```

2. **启动后端**
   ```bash
   pip install -r requirements.txt
   python scripts/chat_server.py
   ```

3. **打开微信开发者工具**
   - 导入 miniprogram 目录
   - 勾选"不校验合法域名"
   - 点击"编译"

完成！🎉
