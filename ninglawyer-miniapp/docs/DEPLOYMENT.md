# 宁律师小程序 - 完整部署文档

## 📋 目录

1. [项目概述](#项目概述)
2. [环境要求](#环境要求)
3. [快速开始](#快速开始)
4. [详细配置](#详细配置)
5. [部署步骤](#部署步骤)
6. [扣子平台配置](#扣子平台配置)
7. [测试验证](#测试验证)
8. [常见问题](#常见问题)

---

## 项目概述

**项目名称**：宁律师法律咨询小程序矩阵
**项目版本**：1.0.0-alpha
**技术栈**：Python + Flask + 微信小程序 + 扣子Bot

**核心功能**：
- 证据脱敏（自动识别并脱敏敏感信息）
- 法律咨询（民事、婚姻、劳动等领域）
- 合同起草（借款合同、租赁合同等）
- 合同审查（风险识别与建议）

**架构设计**：
```
微信小程序 ←→ Flask API ←→ 主脑调度器 ←→ 扣子Bot
```

---

## 环境要求

### 服务器环境

| 组件 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Linux (Ubuntu 20.04+) | Linux (Ubuntu 22.04+) |
| Python | 3.9+ | 3.10+ |
| 内存 | 2GB | 4GB |
| 磁盘 | 10GB | 20GB |
| CPU | 2核 | 4核 |

### 开发环境（本地）

- Python 3.9+
- Node.js 16+（开发小程序）
- 微信开发者工具
- Git

### 网络要求

- 服务器需要公网IP（或通过内网穿透暴露）
- 支持HTTPS（微信小程序要求）
- 开放端口：5000（API端口）

---

## 快速开始

### 方式一：快速部署（推荐新手）

#### 1. 克隆项目

```bash
git clone <项目地址>
cd ninglawyer-miniapp
```

#### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装Python依赖
pip install -r requirements.txt
```

#### 3. 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填写扣子Bot Token：

```env
# 扣子Bot API Token（必填）
COZE_DESENSITIZE_API_TOKEN=pat_xxxx  # 脱敏Bot的Token
COZE_MASTER_API_TOKEN=pat_xxxx       # 主脑Bot的Token
COZE_CIVIL_CONSULT_API_TOKEN=pat_xxxx # 民事咨询Bot的Token
COZE_CONTRACT_DRAFT_API_TOKEN=pat_xxxx # 合同起草Bot的Token

# API配置
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=False

# 微信小程序配置（可选）
WECHAT_APP_ID=your_appid
WECHAT_APP_SECRET=your_appsecret
```

#### 4. 创建Bot配置文件

```bash
mkdir -p config
```

编辑 `config/coze_bots.json`：

```json
{
  "bots": [
    {
      "bot_type": "desensitize",
      "bot_id": "7368002369864167438",
      "api_token_env": "COZE_DESENSITIZE_API_TOKEN",
      "name": "宁律师脱敏助手",
      "description": "自动识别并脱敏证据中的敏感信息"
    },
    {
      "bot_type": "master",
      "bot_id": "7368000000000000000",  # 替换为实际Bot ID
      "api_token_env": "COZE_MASTER_API_TOKEN",
      "name": "宁律师主脑",
      "description": "主脑调度器，负责任务路由"
    },
    {
      "bot_type": "civil_consult",
      "bot_id": "7368000000000000000",  # 替换为实际Bot ID
      "api_token_env": "COZE_CIVIL_CONSULT_API_TOKEN",
      "name": "民事咨询",
      "description": "提供民事法律咨询服务"
    },
    {
      "bot_type": "contract_draft",
      "bot_id": "7368000000000000000",  # 替换为实际Bot ID
      "api_token_env": "COZE_CONTRACT_DRAFT_API_TOKEN",
      "name": "合同起草",
      "description": "起草各类合同"
    }
  ]
}
```

#### 5. 启动服务

```bash
# 启动API服务
python src/main.py
```

#### 6. 验证服务

访问：http://localhost:5000/health

应该返回：

```json
{
  "status": "ok",
  "service": "ninglawyer-miniapp",
  "version": "1.0.0-alpha"
}
```

---

## 详细配置

### 配置文件说明

#### 1. `.env` 环境变量文件

| 变量名 | 说明 | 必填 | 示例 |
|-------|------|------|------|
| COZE_DESENSITIZE_API_TOKEN | 脱敏Bot的Token | 是 | pat_xxxx |
| COZE_MASTER_API_TOKEN | 主脑Bot的Token | 是 | pat_xxxx |
| COZE_CIVIL_CONSULT_API_TOKEN | 民事咨询Bot的Token | 是 | pat_xxxx |
| COZE_CONTRACT_DRAFT_API_TOKEN | 合同起草Bot的Token | 是 | pat_xxxx |
| API_HOST | API服务地址 | 否 | 0.0.0.0 |
| API_PORT | API服务端口 | 否 | 5000 |
| DEBUG | 调试模式 | 否 | False |

#### 2. `config/coze_bots.json` Bot配置文件

配置每个Bot的详细信息：

```json
{
  "bots": [
    {
      "bot_type": "Bot类型标识",
      "bot_id": "Bot的ID（从扣子平台获取）",
      "api_token_env": "环境变量名",
      "name": "Bot名称",
      "description": "Bot描述"
    }
  ]
}
```

### 如何获取扣子Bot Token

#### 步骤1：登录扣子平台

访问：https://www.coze.cn

#### 步骤2：创建Bot

按照以下Bot Prompt文档创建Bot：

1. 宁律师脱敏助手 - 参考 `docs/DESENSITIZE_BOT_PROMPT.md`
2. 宁律师主脑 - 参考 `docs/MASTER_BOT_PROMPT.md`
3. 民事咨询 - 参考 `docs/CIVIL_CONSULT_BOT_PROMPT.md`
4. 合同起草 - 参考 `docs/CONTRACT_DRAFT_BOT_PROMPT.md`

#### 步骤3：获取Bot ID和Token

1. 进入Bot编辑页面
2. 点击右上角"发布"按钮
3. 在发布页面找到"API"部分
4. 复制Bot ID和API Token

#### 步骤4：更新配置

将Bot ID填入 `config/coze_bots.json`
将API Token填入 `.env` 文件

---

## 部署步骤

### 方式一：本地部署

#### 1. 准备环境

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python 3.10
sudo apt install python3.10 python3.10-venv python3-pip -y

# 安装其他依赖
sudo apt install git nginx certbot python3-certbot-nginx -y
```

#### 2. 部署代码

```bash
# 克隆项目
cd /opt
git clone <项目地址> ninglawyer-miniapp
cd ninglawyer-miniapp

# 创建虚拟环境
python3.10 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置环境

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置
nano .env
```

填写所有Token。

#### 4. 创建服务文件

```bash
sudo nano /etc/systemd/system/ninglawyer.service
```

内容：

```ini
[Unit]
Description=Ning Lawyer API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ninglawyer-miniapp
Environment="PATH=/opt/ninglawyer-miniapp/venv/bin"
ExecStart=/opt/ninglawyer-miniapp/venv/bin/python /opt/ninglawyer-miniapp/src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 5. 启动服务

```bash
# 重载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ninglawyer

# 开机自启
sudo systemctl enable ninglawyer

# 查看状态
sudo systemctl status ninglawyer
```

#### 6. 配置Nginx

```bash
sudo nano /etc/nginx/sites-available/ninglawyer
```

内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/ninglawyer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 7. 配置HTTPS（微信小程序必须）

```bash
# 使用Let's Encrypt免费证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 方式二：Docker部署

#### 1. 创建Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "src/main.py"]
```

#### 2. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    restart: always
```

#### 3. 启动服务

```bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

---

## 扣子平台配置

### 1. 创建宁律师主脑

#### Bot ID：`7368000000000000000`（需要替换）

**Prompt设计**：参考 `docs/MASTER_BOT_PROMPT.md`

**工作流**：

1. 添加"开始"节点
2. 添加"意图识别"节点
3. 添加"路由判断"节点（分支：脱敏、民事咨询、合同起草、合同审查）
4. 添加"调用子Bot"节点
5. 添加"整合结果"节点
6. 添加"结束"节点

#### 发布配置：

- 版本号：1.0.0
- 环境ID：7368xxxx（记录下来）
- API Token：复制到 `.env`

### 2. 创建民事咨询Bot

#### Bot ID：`7368000000000000000`（需要替换）

**Prompt设计**：参考 `docs/CIVIL_CONSULT_BOT_PROMPT.md`

**插件**：
- 添加法律知识库插件（如果有）
- 添加联网搜索插件

#### 发布配置：

- 版本号：1.0.0
- 环境ID：7368xxxx
- API Token：复制到 `.env`

### 3. 创建合同起草Bot

#### Bot ID：`7368000000000000000`（需要替换）

**Prompt设计**：参考 `docs/CONTRACT_DRAFT_BOT_PROMPT.md`

**插件**：
- 添加法律知识库插件

#### 发布配置：

- 版本号：1.0.0
- 环境ID：7368xxxx
- API Token：复制到 `.env`

### 4. 宁律师脱敏助手（已完成）

#### Bot ID：`7368002369864167438`

**API Token**：已在 `.env.example` 中提供

---

## 测试验证

### 1. 健康检查

```bash
curl http://localhost:5000/health
```

预期输出：

```json
{
  "status": "ok",
  "service": "ninglawyer-miniapp",
  "version": "1.0.0-alpha"
}
```

### 2. 测试脱敏接口

```bash
curl -X POST http://localhost:5000/api/master/desensitize \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "id_card": "123456789012345678",
    "phone": "13812345678",
    "address": "北京市朝阳区xxx"
  }'
```

### 3. 测试法律咨询接口

```bash
curl -X POST http://localhost:5000/api/master/consult \
  -H "Content-Type: application/json" \
  -d '{
    "question": "朋友借钱不还怎么办",
    "domain": "民事"
  }'
```

### 4. 测试合同起草接口

```bash
curl -X POST http://localhost:5000/api/master/draft-contract \
  -H "Content-Type: application/json" \
  -d '{
    "contract_type": "借款合同",
    "details": "借款方：张三，出借方：李四，金额：10000元"
  }'
```

### 5. 运行集成测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试
python tests/integration_test.py
```

---

## 常见问题

### Q1：API返回500错误

**原因**：
1. 扣子Bot Token未正确配置
2. 扣子Bot未发布或发布失败
3. 网络连接问题

**解决方案**：
1. 检查 `.env` 文件中的Token是否正确
2. 登录扣子平台检查Bot是否发布成功
3. 检查服务器网络是否能访问coze.cn

### Q2：小程序无法连接到服务器

**原因**：
1. 服务器未开放端口
2. 防火墙拦截
3. 域名未解析

**解决方案**：
1. 检查防火墙规则：`sudo ufw allow 5000`
2. 确保域名正确解析到服务器IP
3. 微信小程序必须使用HTTPS

### Q3：Bot调用失败

**原因**：
1. Bot ID配置错误
2. Bot未发布
3. Token过期

**解决方案**：
1. 检查 `config/coze_bots.json` 中的Bot ID
2. 重新发布Bot
3. 重新获取API Token

### Q4：日志如何查看

**查看服务日志**：

```bash
# systemd服务日志
sudo journalctl -u ninglawyer -f

# 应用日志
tail -f /app/work/logs/bypass/app.log
```

### Q5：如何更新代码

```bash
cd /opt/ninglawyer-miniapp
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart ninglawyer
```

### Q6：如何备份数据

```bash
# 备份配置文件
tar -czf ninglawyer-backup-$(date +%Y%m%d).tar.gz \
  config/ .env

# 备份数据库（如果有）
pg_dump -U username dbname > backup.sql
```

---

## 联系支持

如有问题，请联系：
- 技术支持：support@example.com
- 项目文档：`docs/` 目录

---

## 附录

### A. API接口文档

详细API文档请参考：`docs/API.md`

### B. Bot Prompt文档

所有Bot的Prompt设计文档在 `docs/` 目录：
- `MASTER_BOT_PROMPT.md` - 主脑智能体
- `CIVIL_CONSULT_BOT_PROMPT.md` - 民事咨询
- `CONTRACT_DRAFT_BOT_PROMPT.md` - 合同起草
- `DESENSITIZE_BOT_PROMPT.md` - 脱敏助手

### C. 项目结构

```
ninglawyer-miniapp/
├── src/
│   ├── agents/          # Agent实现
│   ├── api/            # API接口
│   ├── storage/        # 数据存储
│   ├── tools/          # 工具
│   └── utils/          # 工具函数
├── config/             # 配置文件
├── miniprogram/        # 小程序代码
├── docs/              # 文档
├── tests/             # 测试
└── requirements.txt   # 依赖
```

---

**文档版本**：1.0.0
**更新日期**：2025-01-21
