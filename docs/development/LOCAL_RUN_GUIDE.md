# 宁律师小程序矩阵 - 本地运行指南

## 📖 目录

- [环境要求](#环境要求)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [后端服务运行](#后端服务运行)
- [小程序开发](#小程序开发)
- [测试运行](#测试运行)
- [常见问题](#常见问题)

---

## 环境要求

### 必须安装

1. **Python** 3.8 或更高
   ```bash
   python --version
   ```

2. **Node.js** 16.x 或更高（用于微信开发者工具）
   ```bash
   node --version
   ```

3. **PostgreSQL** 13 或更高
   ```bash
   psql --version
   ```

4. **Redis** 6 或更高
   ```bash
   redis-server --version
   ```

5. **微信开发者工具**
   - 下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
   - 版本：1.06.2307260 或更高

### 可选安装

- **Docker**（用于快速启动数据库）
- **Git**（用于克隆项目）

---

## 项目结构

```
ninglawyer-miniapp/
├── src/                      # 后端源码
│   ├── agents/              # Agent 类
│   ├── api/                 # API 接口
│   ├── config/              # 配置文件
│   ├── skills/              # 技能定义
│   ├── storage/             # 存储管理
│   ├── tools/               # 工具函数
│   ├── utils/               # 工具类
│   └── main.py              # 主入口
├── components/              # 通用组件
│   ├── message-list/        # 消息列表
│   ├── chat-input/          # 聊天输入
│   ├── loading/             # 加载组件
│   ├── lawyer-selector/     # 律师选择
│   └── contract-editor/     # 合同编辑器
├── miniprogram/            # 小程序代码
│   ├── legal-instructor/   # 法律教官
│   ├── ma-shang-qian-yue/  # 码上签约
│   ├── li-yue/             # 理约
│   ├── zen-pan/            # 怎么判
│   └── fang-feng-xian/     # 防风险
├── tests/                   # 测试代码
├── docs/                    # 文档
├── scripts/                 # 脚本工具
├── requirements.txt         # Python 依赖
├── .env.example            # 环境配置示例
└── README.md               # 项目说明
```

---

## 快速开始

### 1. 克隆项目

```bash
# 克隆项目到本地
git clone https://github.com/hegui2022/ninglawyer-miniapp.git
cd ninglawyer-miniapp
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 3. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境配置示例
cp .env.example .env

# 编辑 .env 文件，配置必要的参数
# 使用你喜欢的编辑器打开 .env 文件
# nano .env
# 或
# vim .env
```

**必需配置项**：

```env
# API 配置
API_HOST=0.0.0.0
API_PORT=8080
API_DEBUG=True

# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ninglawyer
DB_USER=postgres
DB_PASSWORD=your_password

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# 模型配置
MODEL_NAME=doubao-seed-1-6-251015
MODEL_API_KEY=your_api_key
MODEL_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
```

### 5. 初始化数据库

```bash
# 使用 Docker 快速启动 PostgreSQL 和 Redis
docker-compose up -d

# 或手动创建数据库
createdb ninglawyer
```

### 6. 启动后端服务

```bash
# 启动服务
python src/main.py

# 服务将运行在 http://localhost:8080
```

---

## 后端服务运行

### 方式一：直接运行

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动服务
python src/main.py
```

### 方式二：使用 Gunicorn（生产环境）

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:8080 src.main:app
```

### 方式三：使用 Docker

```bash
# 构建镜像
docker build -t ninglawyer-backend .

# 运行容器
docker run -p 8080:8080 --env-file .env ninglawyer-backend
```

### 使用 Docker Compose（推荐）

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: ninglawyer
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - postgres
      - redis
    env_file:
      - .env
    volumes:
      - ./src:/app/src

volumes:
  postgres_data:
  redis_data:
```

启动所有服务：

```bash
docker-compose up -d
```

---

## 小程序开发

### 1. 安装微信开发者工具

下载并安装微信开发者工具：
https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html

### 2. 导入小程序项目

1. 打开微信开发者工具
2. 点击"导入项目"
3. 选择小程序目录，例如：
   - `miniprogram/legal-instructor` （法律教官）
   - `miniprogram/ma-shang-qian-yue` （码上签约）
   - `miniprogram/li-yue` （理约）
   - `miniprogram/zen-pan` （怎么判）
   - `miniprogram/fang-feng-xian` （防风险）
4. 填写项目信息：
   - AppID：填写你的小程序 AppID（测试可使用测试号）
   - 项目名称：例如"法律教官"
5. 点击"导入"

### 3. 配置小程序

在小程序的 `app.js` 中配置后端 API 地址：

```javascript
// miniprogram/legal-instructor/app.js
App({
  onLaunch() {
    // 配置后端 API 地址
    const apiBaseUrl = 'http://localhost:8080';
    wx.setStorageSync('apiBaseUrl', apiBaseUrl);

    // 配置小程序 AppID
    const appId = 'your_appid';
    wx.setStorageSync('appId', appId);
  }
});
```

### 4. 运行小程序

1. 在微信开发者工具中，点击"编译"
2. 小程序将在模拟器中运行
3. 可以实时查看效果和调试

### 5. 开发技巧

#### 使用组件

在页面中引用通用组件：

```javascript
// 页面的 .json 配置
{
  "usingComponents": {
    "message-list": "/components/message-list/message-list",
    "chat-input": "/components/chat-input/chat-input"
  }
}
```

在页面中使用：

```html
<!-- 页面的 .wxml -->
<message-list messages="{{messages}}" />
<chat-input bind:send="onSendMessage" />
```

#### 调试技巧

- 使用 `console.log()` 输出调试信息
- 使用微信开发者工具的"调试器"查看日志
- 使用"网络"面板查看 API 请求
- 使用"存储"面板查看本地数据

---

## 测试运行

### 1. 运行单元测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_basic.py -v

# 查看测试覆盖率
pytest tests/ --cov=src --cov-report=html
```

### 2. 运行集成测试

```bash
# 运行简化测试（不需要数据库和 API）
python -m pytest tests/test_simple.py -v

# 运行完整测试（需要数据库和 API）
python -m pytest tests/test_integration.py -v
```

### 3. 测试后端 API

```bash
# 测试健康检查
curl http://localhost:8080/api/health

# 测试咨询 API
curl -X POST http://localhost:8080/api/consult \
  -H "Content-Type: application/json" \
  -d '{"message": "合同违约怎么办？"}'
```

### 4. 测试小程序

在微信开发者工具中：
1. 点击"编译"运行小程序
2. 在模拟器中测试各项功能
3. 查看控制台输出和错误信息

---

## 常见问题

### Q1: Python 依赖安装失败

**解决方案**：
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 数据库连接失败

**解决方案**：
1. 检查 PostgreSQL 是否运行：
   ```bash
   # Linux/Mac
   sudo systemctl status postgresql

   # 或使用 Docker
   docker ps | grep postgres
   ```

2. 检查 `.env` 文件中的数据库配置

3. 测试数据库连接：
   ```bash
   psql -h localhost -U postgres -d ninglawyer
   ```

### Q3: Redis 连接失败

**解决方案**：
1. 检查 Redis 是否运行：
   ```bash
   redis-cli ping
   ```

2. 检查 `.env` 文件中的 Redis 配置

### Q4: API 端口被占用

**解决方案**：
```bash
# 查找占用端口的进程
lsof -i :8080

# 或
netstat -tlnp | grep 8080

# 更换端口，修改 .env 文件
API_PORT=8000
```

### Q5: 小程序无法连接后端

**解决方案**：
1. 检查后端服务是否运行：
   ```bash
   curl http://localhost:8080/api/health
   ```

2. 检查小程序中的 API 地址配置

3. 检查微信开发者工具中的网络设置

### Q6: 模型 API 调用失败

**解决方案**：
1. 检查 `.env` 文件中的 API 密钥配置

2. 确认 API 密钥有效且有足够的额度

3. 测试 API 连接：
   ```bash
   curl -X POST https://ark.cn-beijing.volces.com/api/v3/chat/completions \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "doubao-seed-1-6-251015", "messages": [{"role": "user", "content": "你好"}]}'
   ```

### Q7: 组件找不到

**解决方案**：
1. 检查组件路径是否正确

2. 检查页面的 `.json` 配置：
   ```json
   {
     "usingComponents": {
       "message-list": "/components/message-list/message-list"
     }
   }
   ```

3. 确保组件文件存在：
   ```
   components/
   └── message-list/
       ├── message-list.js
       ├── message-list.json
       ├── message-list.wxml
       └── message-list.wxss
   ```

---

## 开发工作流

### 1. 启动开发环境

```bash
# 终端 1: 启动后端服务
source venv/bin/activate
python src/main.py

# 终端 2: 启动 PostgreSQL 和 Redis
docker-compose up -d

# 终端 3: 运行测试（可选）
pytest tests/ -v
```

### 2. 开发小程序

1. 在微信开发者工具中打开小程序项目
2. 修改代码
3. 点击"编译"查看效果
4. 重复上述步骤

### 3. 调试后端

```bash
# 查看日志
tail -f /app/work/logs/bypass/app.log

# 或使用调试器
python -m pdb src/main.py
```

### 4. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_basic.py -v

# 查看覆盖率
pytest tests/ --cov=src --cov-report=html
```

---

## 部署到生产环境

详见 [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 获取帮助

- 📖 文档：[https://docs.ninglawyer.com](https://docs.ninglawyer.com)
- 💬 社区：[GitHub Issues](https://github.com/hegui2022/ninglawyer-miniapp/issues)
- 📧 邮箱：support@ninglawyer.com

---

**本地运行指南版本**：v1.0.0
**最后更新**：2025年1月29日
