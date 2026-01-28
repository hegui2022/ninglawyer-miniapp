# 推送代码到 GitHub 仓库指南

## 仓库信息
- 仓库地址：https://github.com/hegui2022/ninglawyer-miniapp
- 项目名称：ninglawyer-miniapp

## 推送步骤

### 方法一：如果您本地已有 Git 仓库

```bash
# 1. 进入项目目录
cd /path/to/your/project

# 2. 查看当前远程仓库
git remote -v

# 3. 如果没有远程仓库，添加远程仓库
git remote add origin https://github.com/hegui2022/ninglawyer-miniapp.git

# 4. 拉取最新代码（如果仓库已有内容）
git pull origin main --allow-unrelated-histories

# 5. 添加所有文件到暂存区
git add .

# 6. 提交代码
git commit -m "feat: 初始化防风险小程序项目"

# 7. 推送到 GitHub
git push -u origin main
```

### 方法二：如果您本地还没有 Git 仓库

```bash
# 1. 进入项目目录
cd /workspace/projects/fangfengxian

# 2. 初始化 Git 仓库
git init

# 3. 添加远程仓库
git remote add origin https://github.com/hegui2022/ninglawyer-miniapp.git

# 4. 添加所有文件到暂存区
git add .

# 5. 提交代码
git commit -m "feat: 初始化防风险小程序项目

- 创建登录页、指引页、管理页、发现页、我的页
- 创建部门页面和公司子页面
- 封装5个公共组件：nav-bar、content-card、comment-list、home-indicator、tab-bar
- 实现完整的页面导航和交互功能"

# 6. 推送到 GitHub
git branch -M main
git push -u origin main
```

### 方法三：从 GitHub 克隆后推送

```bash
# 1. 克隆仓库到本地
git clone https://github.com/hegui2022/ninglawyer-miniapp.git

# 2. 进入项目目录
cd ninglawyer-miniapp

# 3. 将服务器上的代码文件复制到这个目录
# （需要从服务器下载 fangfengxian/ 目录的所有文件）

# 4. 添加文件到暂存区
git add .

# 5. 提交代码
git commit -m "feat: 初始化防风险小程序项目"

# 6. 推送到 GitHub
git push -u origin main
```

## 常见问题

### Q: 推送时提示需要身份验证？
A: 请配置 Git 用户信息：
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Q: 推送时提示被拒绝？
A: 如果仓库已有内容，使用：
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Q: 如何强制推送？
A: ⚠️ 谨慎使用，会覆盖远程仓库内容：
```bash
git push -u origin main --force
```

## 验证推送成功

1. 访问：https://github.com/hegui2022/ninglawyer-miniapp
2. 查看代码是否已上传
3. 确认文件结构和内容是否正确

## 需要上传的文件列表

### 核心文件
- app.js
- app.json
- app.wxss
- README.md
- QUICK_START.md

### 组件目录（components/）
- nav-bar/
- content-card/
- comment-list/
- home-indicator/
- tab-bar/

### 页面目录（pages/）
- login/
- guide/
  └── article/
- obligation/
- manage/
- discover/
- profile/
  └── company/
      ├── articles/
      ├── data-compliance/
      └── procurement-compliance/
- department/

### 资源目录（images/）
- tabbar/ (需要添加图标文件)

## 推送后的操作

1. **检查仓库**
   - 确认所有文件已上传
   - 检查 README.md 是否显示正常

2. **克隆测试**
   - 在另一台电脑或目录克隆仓库
   - 使用微信开发者工具打开
   - 测试项目是否可以正常运行

3. **设置分支保护（可选）**
   - 在 GitHub 仓库设置中
   - 启用分支保护规则
   - 要求代码审查

## 如果您无法执行 Git 命令

您可以：

1. **通过 GitHub 网页上传**
   - 访问 https://github.com/hegui2022/ninglawyer-miniapp
   - 点击 "Upload files"
   - 手动上传文件（不推荐，文件太多）

2. **使用 GitHub Desktop**
   - 下载 GitHub Desktop
   - 图形化界面操作
   - 更容易上手

3. **联系我获取代码文件**
   - 我可以提供文件列表
   - 您可以手动下载并上传

## 技术支持

如果推送过程中遇到问题，请检查：
- Git 是否已安装：`git --version`
- 网络连接是否正常
- GitHub 账户是否有权限
- 仓库地址是否正确
