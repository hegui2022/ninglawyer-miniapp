# 🎉 宁律师小程序代码下载指南

## 📦 方式一：直接下载压缩包（最简单，推荐！）

**文件已准备好：**
- 文件名：`ninglawyer-miniapp.tar.gz`
- 大小：9.5MB
- 位置：`/workspace/projects/ninglawyer-miniapp.tar.gz`

### 下载步骤：

1. **使用文件管理器下载**
   - 打开 FileZilla、WinSCP 或其他 FTP/SFTP 客户端
   - 连接到服务器
   - 找到 `/workspace/projects/` 目录
   - 下载 `ninglawyer-miniapp.tar.gz`

2. **或者使用 SCP 命令**
   ```bash
   # 在你电脑上执行
   scp user@你的服务器IP:/workspace/projects/ninglawyer-miniapp.tar.gz ./
   ```

3. **在本地解压**
   ```bash
   tar -xzf ninglawyer-miniapp.tar.gz
   ```

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

5. **启动后端**
   ```bash
   python scripts/chat_server.py
   ```

6. **打开微信开发者工具**
   - 导入 `miniprogram` 目录
   - 勾选"不校验合法域名"
   - 点击"编译"

---

## 🔗 方式二：使用 Git 仓库（方便后续更新）

### 步骤 1：创建远程仓库

**推荐使用 Gitee（国内速度快）：**

1. 访问：https://gitee.com/projects/new
2. 仓库名：`ninglawyer-miniapp`
3. 描述：`宁律师智能法律咨询小程序`
4. 选择：公开或私有
5. 点击"创建"

### 步骤 2：配置远程仓库

在服务器上执行：
```bash
cd /workspace/projects
git remote add origin https://gitee.com/你的用户名/ninglawyer-miniapp.git
git branch -M main
git push -u origin main
```

### 步骤 3：在本地克隆

```bash
git clone https://gitee.com/你的用户名/ninglawyer-miniapp.git
cd ninglawyer-miniapp
```

然后按照方式一的步骤 4-6 操作。

---

## ❓ 关于第一个错误

请用文字描述一下错误信息，我可以帮你解决：

1. 错误提示是什么？
2. 在哪个步骤出现的？（启动后端？导入小程序？）
3. 完整的错误信息（如果有）

---

## ✅ 快速检查清单

下载完成后，检查以下文件是否存在：

```
✅ miniprogram/app.js
✅ miniprogram/app.json
✅ miniprogram/pages/chat/chat.js
✅ scripts/chat_server.py
✅ src/agents/agent.py
✅ config/agent_llm_config.json
✅ requirements.txt
```

---

## 📖 相关文档

详细说明请查看：
- `GIT_SETUP_GUIDE.md` - Git 设置详细指南
- `SYNC_TO_LOCAL.md` - 同步到本地说明
- `MINIPROGRAM_README.md` - 完整项目说明
- `miniprogram/QUICKSTART.md` - 快速开始

---

## 🚀 现在就开始！

**最简单的 3 步：**

1. 下载 `ninglawyer-miniapp.tar.gz`（9.5MB）
2. 在本地解压并安装依赖
3. 启动后端，打开微信开发者工具

有问题随时问我！💪
