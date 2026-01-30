# 🚀 宁律师法律咨询小程序 - 快速启动指南

## 📋 前置要求

### 必需
- **Python**: 3.9 或更高版本
- **pip**: Python 包管理器
- **微信开发者工具**: [下载地址](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

### 可选
- **PostgreSQL**: 生产环境数据库
- **Redis**: 缓存服务（可选）
- **Git**: 版本控制（可选）

---

## 🔧 安装步骤

### 1. 克隆或下载项目

```bash
# 如果使用 Git
git clone <repository-url>
cd ninglawyer-miniapp

# 或者直接解压项目文件
cd ninglawyer-miniapp
```

### 2. 安装 Python 依赖

#### 方法一：使用启动脚本（推荐）

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

#### 方法二：手动安装

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

项目已经包含了 `.env` 文件，默认配置适合开发环境。如需修改，请编辑 `.env` 文件：

```env
# 数据库配置（默认使用 SQLite）
DATABASE_URL=sqlite:///ninglawyer.db

# API 服务配置
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=False

# JWT 配置
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
```

### 4. 初始化数据库

```bash
python3 scripts/migrate_subscription.py
```

这将创建数据库表并初始化测试数据。

---

## 🚀 启动服务

### 后端服务

```bash
# 方法一：使用启动脚本
./start.sh          # Linux/Mac
start.bat            # Windows

# 方法二：手动启动
python3 src/main.py
```

**成功启动后，您将看到：**
```
========================================
宁律师法律咨询小程序矩阵
========================================
服务地址: http://0.0.0.0:5000
健康检查: http://0.0.0.0:5000/health
API 文档: http://0.0.0.0:5000/api
========================================

* Running on http://127.0.0.1:5000
```

### 前端服务（微信小程序）

1. **打开微信开发者工具**
2. **导入项目**
   - 点击 "+" 按钮
   - 选择项目目录：`ninglawyer-miniapp/miniprogram`
   - 输入 AppID（测试可以使用"测试号"）
   - 点击"导入"

3. **配置 API 地址**
   
   编辑 `miniprogram/app.js`，修改 API 基础地址：
   ```javascript
   // 开发环境
   const apiBase = 'http://localhost:5000'
   
   // 生产环境
   // const apiBase = 'https://your-domain.com'
   ```

4. **运行小程序**
   - 点击"编译"按钮
   - 小程序将在模拟器中运行

---

## 🧪 测试服务

### 测试后端服务

```bash
# 测试健康检查
curl http://localhost:5000/health

# 运行集成测试
cd ninglawyer-miniapp
python3 scripts/test_integration.py
```

**预期输出：**
```
总计: 5/5 通过
✅ 所有测试通过！前后端联动成功！
```

### 测试前端服务

在微信开发者工具中：
1. 检查模拟器是否正常显示
2. 测试各个页面切换
3. 测试 API 调用（查看网络请求）

---

## 📊 数据库管理

### 查看数据库

```bash
# SQLite（开发环境）
sqlite3 ninglawyer.db

# 常用命令
.tables              # 查看所有表
.schema users        # 查看表结构
SELECT * FROM users; # 查询用户数据
.quit               # 退出
```

### 重置数据库

```bash
# 删除数据库文件
rm ninglawyer.db

# 重新初始化
python3 scripts/migrate_subscription.py
```

---

## 🔍 故障排查

### 问题 1: 后端启动失败

**症状**: 启动时报错 "Address already in use"

**解决方案**:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### 问题 2: 依赖安装失败

**症状**: pip install 报错

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装
pip install -r requirements.txt --no-cache-dir
```

### 问题 3: 数据库连接失败

**症状**: 提示数据库连接失败

**解决方案**:
```bash
# 检查数据库文件权限
ls -la ninglawyer.db

# 重新初始化数据库
python3 scripts/migrate_subscription.py
```

### 问题 4: 前端无法连接后端

**症状**: 小程序提示网络错误

**解决方案**:
1. 检查后端服务是否启动
2. 检查 API 地址配置是否正确
3. 检查微信开发者工具的"不校验合法域名"是否勾选

---

## 📁 项目结构

```
ninglawyer-miniapp/
├── src/                      # 后端源代码
│   ├── agents/               # 智能体模块
│   ├── api/                  # API 接口
│   ├── config/               # 配置文件
│   ├── middleware/           # 中间件
│   ├── models/               # 数据模型
│   ├── skills/               # 技能模块
│   ├── storage/              # 存储模块
│   ├── tools/                # 工具函数
│   └── utils/                # 工具类
├── miniprogram/              # 小程序前端
│   ├── pages/                # 页面
│   ├── static/               # 静态资源
│   ├── app.js                # 小程序入口
│   ├── app.json              # 小程序配置
│   └── app.wxss              # 全局样式
├── scripts/                  # 脚本工具
├── tests/                    # 测试文件
├── docs/                     # 文档
├── requirements.txt          # Python 依赖
├── .env                      # 环境配置
├── start.sh                  # Linux/Mac 启动脚本
└── start.bat                 # Windows 启动脚本
```

---

## 🎯 常用命令

### 后端相关
```bash
# 启动服务
python3 src/main.py

# 初始化数据库
python3 scripts/migrate_subscription.py

# 运行测试
python3 scripts/test_integration.py

# 检查日志
tail -f logs/app.log
```

### 前端相关
```bash
# 无需命令，使用微信开发者工具操作
```

---

## 📚 更多文档

- [完整实施报告](COMPLETION_SUMMARY.md)
- [前后端集成测试报告](FRONTEND_BACKEND_INTEGRATION_SUCCESS_REPORT.md)
- [单元测试报告](TEST_REPORT.md)
- [套餐系统说明](SUBSCRIPTION_COMPLETION_REPORT.md)

---

## 💡 开发建议

### 开发环境
- 使用 SQLite 作为数据库（默认）
- 启用 DEBUG 模式
- 使用虚拟环境隔离依赖

### 生产环境
- 使用 PostgreSQL 作为数据库
- 禁用 DEBUG 模式
- 配置 HTTPS
- 使用 Nginx 反向代理
- 配置 Redis 缓存
- 配置日志收集

---

## 🆘 获取帮助

如果遇到问题，请：
1. 查看本文档的"故障排查"部分
2. 查看项目文档目录
3. 检查日志文件 `logs/app.log`
4. 运行测试脚本验证配置

---

## ✅ 启动检查清单

启动前请确认：

- [ ] Python 3.9+ 已安装
- [ ] 依赖已安装 (`pip install -r requirements.txt`)
- [ ] .env 文件已配置
- [ ] 数据库已初始化 (`python3 scripts/migrate_subscription.py`)
- [ ] 后端服务已启动 (`python3 src/main.py`)
- [ ] 微信开发者工具已安装
- [ ] 小程序项目已导入
- [ ] API 地址配置正确

---

**祝您使用愉快！** 🎉
