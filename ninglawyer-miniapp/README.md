# 宁律师法律咨询小程序矩阵

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**一个基于AI的法律咨询小程序，提供证据脱敏、法律咨询、合同起草等服务**

</div>

---

## 📖 项目简介

宁律师法律咨询小程序矩阵是一个智能法律服务平台，通过整合多个AI Bot，为用户提供便捷的法律服务。

### 核心功能

- 🔒 **证据脱敏**：自动识别并脱敏证据中的敏感信息（姓名、身份证、手机号、地址等）
- ⚖️ **法律咨询**：提供民事、婚姻、劳动等多个领域的法律咨询服务
- 📄 **合同起草**：支持起草借款合同、租赁合同、劳动合同等多种合同
- 🔍 **合同审查**：智能识别合同中的风险点，提供修改建议

### 技术架构

```
微信小程序 ←→ Flask API ←→ 主脑调度器 ←→ 扣子Bot矩阵
                                    ↓
                         脱敏Bot | 咨询Bot | 合同Bot
```

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Flask 2.0+
- 扣子平台账号

### 5分钟快速部署

#### 1. 克隆项目

```bash
git clone <项目地址>
cd ninglawyer-miniapp
```

#### 2. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入扣子Bot Token
nano .env
```

需要配置的Token：

```env
COZE_DESENSITIZE_API_TOKEN=pat_xxxx  # 脱敏Bot
COZE_MASTER_API_TOKEN=pat_xxxx       # 主脑Bot
COZE_CIVIL_CONSULT_API_TOKEN=pat_xxxx # 民事咨询Bot
COZE_CONTRACT_DRAFT_API_TOKEN=pat_xxxx # 合同起草Bot
```

#### 4. 启动服务

```bash
python src/main.py
```

服务将在 `http://localhost:5000` 启动。

#### 5. 验证服务

```bash
curl http://localhost:5000/health
```

返回：

```json
{
  "status": "ok",
  "service": "ninglawyer-miniapp",
  "version": "1.0.0-alpha"
}
```

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [部署文档](docs/DEPLOYMENT.md) | 详细的部署步骤和配置说明 |
| [API文档](docs/API.md) | 所有API接口的详细说明 |
| [主脑Prompt](docs/MASTER_BOT_PROMPT.md) | 主脑智能体的Prompt设计 |
| [民事咨询Prompt](docs/CIVIL_CONSULT_BOT_PROMPT.md) | 民事咨询Bot的Prompt设计 |
| [合同起草Prompt](docs/CONTRACT_DRAFT_BOT_PROMPT.md) | 合同起草Bot的Prompt设计 |
| [脱敏助手Prompt](docs/DESENSITIZE_BOT_PROMPT.md) | 脱敏助手Bot的Prompt设计 |
| [进度报告](docs/PROGRESS.md) | 项目开发进度 |

---

## 🎯 API接口示例

### 1. 脱敏接口

```bash
curl -X POST http://localhost:5000/api/master/desensitize \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "id_card": "123456789012345678",
    "phone": "13812345678"
  }'
```

**响应**：

```json
{
  "success": true,
  "data": {
    "name": "*三",
    "id_card": "123***********678",
    "phone": "138****5678"
  }
}
```

### 2. 法律咨询接口

```bash
curl -X POST http://localhost:5000/api/master/consult \
  -H "Content-Type: application/json" \
  -d '{
    "question": "朋友借钱不还怎么办",
    "domain": "民事"
  }'
```

**响应**：

```json
{
  "success": true,
  "data": {
    "answer": "根据《民法典》相关规定...",
    "domain": "民事",
    "suggestions": ["收集证据", "友好协商", "法律途径"]
  }
}
```

### 3. 合同起草接口

```bash
curl -X POST http://localhost:5000/api/master/draft-contract \
  -H "Content-Type: application/json" \
  -d '{
    "contract_type": "借款合同",
    "details": "借款方：张三，出借方：李四，金额：10000元"
  }'
```

**响应**：

```json
{
  "success": true,
  "data": {
    "contract": "借款合同\n\n甲方：李四\n乙方：张三\n...",
    "contract_type": "借款合同"
  }
}
```

---

## 📁 项目结构

```
ninglawyer-miniapp/
├── src/                        # 后端源代码
│   ├── agents/                 # Agent实现
│   │   └── master_agent.py    # 主脑调度器
│   ├── api/                    # API接口
│   │   ├── master.py          # 主脑API
│   │   ├── consultation.py    # 咨询API
│   │   ├── contract.py        # 合同API
│   │   └── routes.py          # 路由注册
│   ├── storage/                # 数据存储
│   │   ├── db.py              # 数据库初始化
│   │   └── memory/            # 记忆存储
│   ├── utils/                  # 工具函数
│   │   ├── bot_registry.py    # Bot注册表
│   │   ├── logger.py          # 日志工具
│   │   └── coze_client.py     # 扣子客户端
│   └── main.py                 # 主入口
├── miniprogram/               # 小程序代码
│   ├── pages/                 # 页面
│   │   ├── index/            # 首页
│   │   ├── desensitize/      # 脱敏页面
│   │   ├── consult/          # 咨询页面
│   │   └── contract/         # 合同页面
│   └── utils/                # 工具
├── config/                    # 配置文件
│   └── coze_bots.json        # Bot配置
├── docs/                     # 文档
│   ├── DEPLOYMENT.md         # 部署文档
│   ├── API.md                # API文档
│   ├── MASTER_BOT_PROMPT.md  # 主脑Prompt
│   └── ...
├── tests/                    # 测试
│   └── integration_test.py   # 集成测试
├── requirements.txt          # Python依赖
├── .env.example             # 环境变量示例
├── .coze                    # 扣子配置
└── README.md                # 本文件
```

---

## 🔧 配置说明

### 扣子Bot配置

项目需要配置4个Bot：

| Bot名称 | Bot ID | 说明 | 配置文件 |
|--------|--------|------|---------|
| 宁律师脱敏助手 | 7368002369864167438 | 脱敏功能 | `docs/DESENSITIZE_BOT_PROMPT.md` |
| 宁律师主脑 | 待创建 | 任务路由 | `docs/MASTER_BOT_PROMPT.md` |
| 民事咨询Bot | 待创建 | 法律咨询 | `docs/CIVIL_CONSULT_BOT_PROMPT.md` |
| 合同起草Bot | 待创建 | 合同起草 | `docs/CONTRACT_DRAFT_BOT_PROMPT.md` |

**如何获取Token**：

1. 登录 [扣子平台](https://www.coze.cn)
2. 创建Bot或使用现有Bot
3. 点击"发布"
4. 复制API Token
5. 填入 `.env` 文件

详细步骤请参考 [部署文档](docs/DEPLOYMENT.md)

---

## 🧪 测试

### 运行集成测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试
python tests/integration_test.py
```

测试会自动验证所有API接口的功能。

### 手动测试

```bash
# 健康检查
curl http://localhost:5000/health

# 脱敏测试
curl -X POST http://localhost:5000/api/master/desensitize \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "id_card": "123456789012345678"}'

# 咨询测试
curl -X POST http://localhost:5000/api/master/consult \
  -H "Content-Type: application/json" \
  -d '{"question": "朋友借钱不还怎么办", "domain": "民事"}'
```

---

## 📦 生产部署

### 使用systemd管理服务

创建服务文件：

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

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start ninglawyer
sudo systemctl enable ninglawyer
```

### 使用Nginx反向代理

```bash
sudo nano /etc/nginx/sites-available/ninglawyer
```

内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

配置HTTPS：

```bash
sudo certbot --nginx -d your-domain.com
```

详细部署步骤请参考 [部署文档](docs/DEPLOYMENT.md)

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

---

## 📄 开源协议

本项目采用 MIT 协议开源。

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件：support@example.com

---

## 🙏 致谢

感谢以下项目和服务：

- [扣子](https://www.coze.cn) - AI Bot开发平台
- [Flask](https://flask.palletsprojects.com/) - Python Web框架
- [微信小程序](https://developers.weixin.qq.com/miniprogram/dev/framework/) - 小程序开发平台

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by NingLawyer Team

</div>
