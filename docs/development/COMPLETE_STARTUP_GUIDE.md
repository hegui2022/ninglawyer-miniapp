# 🚀 完整的小程序启动测试指南

## 📋 前置条件

### 必需
- ✅ Python 3.9+ 已安装
- ✅ Anaconda 已安装
- ✅ 微信开发者工具已安装
- ✅ 项目文件完整

### 可选
- Git（用于版本控制）

---

## 第一步：环境准备

### 1.1 打开 Anaconda Prompt

**Windows**:
1. 按 `Win` 键
2. 搜索 "Anaconda Prompt"
3. 打开 Anaconda Prompt

### 1.2 创建并激活虚拟环境

```bash
# 创建虚拟环境
conda create -n ninglawyer python=3.9 -y

# 激活虚拟环境
conda activate ninglawyer
```

### 1.3 进入项目目录

```bash
# 替换为您的实际路径
cd C:\ninglawyer-miniapp
```

### 1.4 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 如果安装缓慢，使用镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 1.5 验证依赖安装

```bash
python -c "import flask; print('Flask:', flask.__version__)"
python -c "import langchain; print('LangChain:', langchain.__version__)"
python -c "import sqlalchemy; print('SQLAlchemy:', sqlalchemy.__version__)"
```

---

## 第二步：配置和初始化

### 2.1 检查 .env 文件

确保项目目录中有 `.env` 文件，包含以下内容：

```env
DATABASE_URL=sqlite:///ninglawyer.db
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=False
JWT_SECRET_KEY=ninglawyer-secret-key-2024
JWT_ACCESS_TOKEN_EXPIRES=3600
WECHAT_APP_ID=your-wechat-app-id
WECHAT_APP_SECRET=your-wechat-app-secret
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
FLASK_ENV=development
```

### 2.2 创建日志目录

```bash
mkdir logs
```

### 2.3 初始化数据库

```bash
python scripts/migrate_subscription.py
```

成功后会看到：
```
✅ 数据库迁移完成！
```

### 2.4 验证数据库

```bash
# Windows
dir *.db

# Mac/Linux
ls -la *.db
```

应该看到 `ninglawyer.db` 文件

---

## 第三步：启动后端服务

### 3.1 启动 Flask 服务

```bash
python src/main.py
```

**成功启动后会看到**：

```
========================================
宁律师法律咨询小程序矩阵
========================================
服务地址: http://0.0.0.0:5000
健康检查: http://0.0.0.0:5000/health
API 文档: http://0.0.0.0:5000/api
========================================

* Running on http://127.0.0.1:5000
* Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

### 3.2 测试后端服务

**打开新的 Anaconda Prompt 窗口**，激活虚拟环境：

```bash
conda activate ninglawyer
cd C:\ninglawyer-miniapp
```

**测试健康检查**：

```bash
# Windows PowerShell
Invoke-WebRequest -Uri http://localhost:5000/health | Select-Object -ExpandProperty Content

# Windows CMD
curl http://localhost:5000/health
```

**预期输出**：

```json
{
  "status": "ok",
  "service": "ninglawyer-miniapp",
  "version": "1.0.0-alpha"
}
```

**测试套餐接口**：

```bash
curl http://localhost:5000/api/subscription/plans
```

**预期输出**：

```json
{
  "success": true,
  "data": [...]
}
```

---

## 第四步：配置微信开发者工具

### 4.1 打开微信开发者工具

1. 启动微信开发者工具
2. 扫码登录

### 4.2 导入项目

1. 点击 "+" 按钮
2. 填写项目信息：
   - **项目名称**: 宁律师法律咨询
   - **目录**: 选择 `ninglawyer-miniapp/miniprogram` 文件夹
   - **AppID**: 选择"测试号"
   - **开发模式**: 小程序
   - **后端服务**: 不使用云服务
3. 点击"导入"

### 4.3 配置开发环境

在微信开发者工具中：
1. 点击右上角"详情"
2. 选择"本地设置"
3. **必须勾选**:
   - ✅ 不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书
   - ✅ 启用调试
4. 建议勾选:
   - ✅ 启用 ES6 转 ES5
   - ✅ 启用增强编译

### 4.4 编译运行

点击"编译"按钮

**成功编译后，模拟器中会显示**：
- 首页（显示问候语和快捷入口）
- 底部有5个导航标签

---

## 第五步：功能测试

### 5.1 测试底部导航

点击底部导航栏的5个标签，确保都能正常切换：

1. **首页** - 显示问候语、快捷入口、热门问题
2. **咨询** - 显示咨询输入界面
3. **合同** - 显示合同功能入口
4. **记录** - 显示历史记录列表
5. **我的** - 显示个人信息和设置

### 5.2 测试套餐功能

**步骤**：
1. 点击底部"我的"
2. 点击"套餐管理"
3. 查看当前套餐信息
4. 点击"专业版"或"企业版"
5. 点击"升级套餐"
6. 查看升级成功提示

**验证后端**：
打开浏览器，访问：
```
http://localhost:5000/api/subscription/user?user_id=1
```

查看套餐是否已更新。

### 5.3 测试咨询功能

**步骤**：
1. 点击底部"咨询"
2. 输入问题，例如："借钱给朋友不还怎么办？"
3. 点击"发送"按钮
4. 等待AI回复

**查看日志**：
回到运行 Flask 的终端，查看处理日志。

### 5.4 测试合同功能

**步骤**：
1. 点击底部"合同"
2. 选择合同类型（例如：借款合同）
3. 填写合同信息
4. 点击"生成合同"
5. 等待合同生成
6. 查看生成的合同内容

---

## 第六步：完整测试

### 6.1 运行后端测试

**打开新终端**，激活虚拟环境：

```bash
conda activate ninglawyer
cd C:\ninglawyer-miniapp
```

**运行集成测试**：

```bash
python scripts/test_integration.py
```

**预期输出**：

```
============================================================
                      宁律师小程序 - 前后端集成测试                      
============================================================

测试1: 健康检查
✅ 健康检查通过

测试2: 获取套餐列表
✅ 获取套餐列表成功: 3 个套餐

测试3: 获取用户套餐
✅ 获取用户套餐成功

测试4: 获取可用模块
✅ 获取可用模块成功: 2 个模块

测试5: 升级套餐
✅ 升级套餐成功

总计: 5/5 通过
✅ 所有测试通过！前后端联动成功！
```

### 6.2 运行项目验证

```bash
python verify_startup.py
```

**预期输出**：

```
============================================================
  宁律师法律咨询小程序 - 启动验证
============================================================

✅ 所有检查通过！可以启动项目

启动命令:
  python3 src/main.py
```

### 6.3 运行小程序语法检查

```bash
python miniprogram/check_miniprogram_syntax.py
```

**预期输出**：

```
✅ 所有文件语法正确！
```

---

## 第七步：常见问题解决

### 问题1: 端口 5000 被占用

**Windows**:
```bash
netstat -ano | findstr :5000
taskkill /PID <进程ID> /F
```

### 问题2: 依赖安装失败

```bash
# 清理缓存
pip cache purge

# 使用镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 逐个安装核心依赖
pip install flask sqlalchemy langchain langchain-openai flask-cors python-dotenv loguru
```

### 问题3: 数据库初始化失败

```bash
# 删除现有数据库
del ninglawyer.db

# 重新初始化
python scripts/migrate_subscription.py
```

### 问题4: 小程序无法连接后端

1. 确认 Flask 服务正在运行
2. 检查 `miniprogram/app.js` 中的 `apiBase` 配置：
   ```javascript
   const apiBase = 'http://localhost:5000'
   ```
3. 确保"不校验合法域名"已勾选

### 问题5: 页面空白

1. 点击"编译"重新编译
2. 清除缓存：工具 → 清除缓存 → 全部清除
3. 重新编译

### 问题6: 网络请求失败

1. 确认后端服务运行
2. 检查 API 地址配置
3. 确保勾选"不校验合法域名"
4. 查看控制台错误信息

---

## 第八步：快速启动（后续使用）

以后启动项目只需要：

```bash
# 1. 打开 Anaconda Prompt

# 2. 激活虚拟环境
conda activate ninglawyer

# 3. 进入项目目录
cd C:\ninglawyer-miniapp

# 4. 启动后端
python src/main.py

# 5. 打开微信开发者工具
# 6. 点击"编译"按钮
```

---

## 📝 完整命令清单

### 首次启动
```bash
# 1. 创建虚拟环境
conda create -n ninglawyer python=3.9 -y

# 2. 激活虚拟环境
conda activate ninglawyer

# 3. 进入项目目录
cd C:\ninglawyer-miniapp

# 4. 安装依赖
pip install -r requirements.txt

# 5. 创建日志目录
mkdir logs

# 6. 初始化数据库
python scripts/migrate_subscription.py

# 7. 启动服务
python src/main.py

# 8. 打开微信开发者工具，导入 miniprogram 目录
# 9. 点击"编译"
```

### 后续启动
```bash
# 1. 激活虚拟环境
conda activate ninglawyer

# 2. 进入项目目录
cd C:\ninglawyer-miniapp

# 3. 启动服务
python src/main.py

# 4. 打开微信开发者工具
# 5. 点击"编译"
```

### 测试命令
```bash
# 测试后端
curl http://localhost:5000/health

# 运行集成测试
python scripts/test_integration.py

# 运行项目验证
python verify_startup.py

# 检查小程序语法
python miniprogram/check_miniprogram_syntax.py
```

---

## ✅ 启动检查清单

启动前请确认：

- [ ] Anaconda 已安装
- [ ] 虚拟环境已创建并激活
- [ ] Python 依赖已安装
- [ ] .env 文件已配置
- [ ] 数据库已初始化
- [ ] 后端服务可以启动
- [ ] 微信开发者工具已安装
- [ ] 小程序项目已导入
- [ ] 开发环境已配置（不校验域名）
- [ ] API 地址配置正确

---

## 🎯 成功标志

当您完成所有步骤后，您应该能够：

1. ✅ 在 Anaconda 虚拟环境中运行 Flask 服务
2. ✅ 通过浏览器访问 API 接口
3. ✅ 在微信开发者工具中看到小程序界面
4. ✅ 点击底部导航正常切换页面
5. ✅ 测试套餐升级功能
6. ✅ 测试法律咨询功能
7. ✅ 测试合同起草功能
8. ✅ 查看后端和前端的交互日志

---

**祝您体验愉快！** 🎉

如有任何问题，请参考"常见问题解决"部分。
