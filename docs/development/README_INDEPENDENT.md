# 宁律师法律咨询小程序 - 独立架构版本

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0--independent-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Architecture](https://img.shields.io/badge/architecture-Independent-orange.svg)

**基于AI大模型的智能法律服务平台 - 完全独立开发**

</div>

---

## 📖 项目简介

宁律师法律咨询小程序是一个完全独立开发的智能法律服务平台，不依赖任何第三方Bot平台。通过自主开发的**主脑智能体**和**技能模块**，为用户提供便捷的法律服务。

### 核心功能

- 🔒 **证据脱敏**：自动识别并脱敏证据中的敏感信息（姓名、身份证、手机号、地址等）
- ⚖️ **法律咨询**：提供民事、婚姻、劳动等多个领域的法律咨询服务
- 📄 **合同起草**：支持起草借款合同、租赁合同、劳动合同等多种合同
- 🔍 **合同审查**：智能识别合同中的风险点，提供修改建议

### 技术架构

```
微信小程序 ←→ Flask API ←→ 主脑智能体 ←→ 技能模块
                                    ↓
                    脱敏技能 | 民事咨询技能 | 合同起草技能
                                    ↓
                            豆包大语言模型（LLM）
```

---

## 🎯 独立架构优势

### ✅ 完全自主可控
- 不依赖任何第三方Bot平台
- 所有代码自主开发
- 数据完全私有化

### ✅ 技术架构清晰
- 主脑智能体：任务路由和协调
- 技能模块：独立的功能实现
- 服务注册表：统一的技能管理

### ✅ 易于扩展
- 添加新技能只需开发新的技能模块
- 统一的技能注册机制
- 标准化的接口定义

### ✅ 成本可控
- 直接调用大语言模型API
- 无需第三方平台费用
- 灵活的计费方式

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Flask 2.0+
- 豆包大语言模型（通过集成服务）

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

#### 3. 启动服务

```bash
python src/main.py
```

服务将在 `http://localhost:5000` 启动。

#### 4. 验证服务

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

## 🎯 API接口示例

### 1. 主脑路由接口（智能路由）

```bash
curl -X POST http://localhost:5000/api/master/route \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "帮我脱敏一下，我叫张三，手机号13812345678"
  }'
```

**响应**：

```json
{
  "success": true,
  "data": {
    "original": "张三",
    "desensitized": "张*",
    "type": "姓名"
  }
}
```

### 2. 脱敏接口

```bash
curl -X POST http://localhost:5000/api/master/desensitize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "我叫张三，身份证123456789012345678"
  }'
```

### 3. 法律咨询接口

```bash
curl -X POST http://localhost:5000/api/master/consult \
  -H "Content-Type: application/json" \
  -d '{
    "question": "朋友借钱不还怎么办"
  }'
```

### 4. 合同起草接口

```bash
curl -X POST http://localhost:5000/api/master/contract \
  -H "Content-Type: application/json" \
  -d '{
    "text": "帮我起草一个借款合同，借款方：张三，出借方：李四，金额：10000元"
  }'
```

---

## 📁 项目结构

```
ninglawyer-miniapp/
├── src/                        # 后端源代码
│   ├── agents/                 # 智能体
│   │   └── master_brain.py    # 主脑智能体
│   ├── skills/                 # 技能模块
│   │   ├── desensitize_skill.py  # 脱敏技能
│   │   ├── civil_consult_skill.py # 民事咨询技能
│   │   ├── contract_skill.py     # 合同起草技能
│   │   └── __init__.py           # 技能注册
│   ├── utils/                  # 工具函数
│   │   ├── skill_registry.py  # 技能注册表
│   │   ├── logger.py          # 日志工具
│   │   └── coze_client.py     # LLM客户端
│   ├── api/                    # API接口
│   │   ├── master.py          # 主脑API
│   │   ├── consultation.py    # 咨询API
│   │   ├── contract.py        # 合同API
│   │   └── routes.py          # 路由注册
│   ├── storage/                # 数据存储
│   │   ├── db.py              # 数据库初始化
│   │   └── memory/            # 记忆存储
│   └── main.py                 # 主入口
├── miniprogram/               # 小程序代码
│   ├── pages/                 # 页面
│   │   ├── index/            # 首页
│   │   ├── desensitize/      # 脱敏页面
│   │   ├── consult/          # 咨询页面
│   │   └── contract/         # 合同页面
│   └── utils/                # 工具
├── tests/                    # 测试
│   └── integration_test_independent.py  # 集成测试
├── docs/                     # 文档
│   ├── DEPLOYMENT.md         # 部署文档
│   ├── API.md                # API文档
│   └── ...
├── requirements.txt          # Python依赖
├── .env.example             # 环境变量示例
└── README.md                # 本文件
```

---

## 🔧 技术栈

### 后端
- Python 3.9+
- Flask 2.0+
- LangChain（消息处理）
- 豆包大语言模型（集成服务）
- Loguru（日志）

### 前端
- 微信小程序
- 原生小程序框架

### AI服务
- 豆包大语言模型（doubao-seed-1-8-251228）
- 多模态支持（文本、图片、视频）

---

## 🧪 测试

### 运行集成测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试
python tests/integration_test_independent.py
```

### 测试结果

| 功能 | 状态 | 说明 |
|------|------|------|
| 健康检查 | ✅ 通过 | 服务正常运行 |
| 主脑路由 | ✅ 通过 | 正确路由到对应技能 |
| 脱敏技能 | ✅ 通过 | 姓名、身份证、手机号脱敏正常 |
| 民事咨询 | ✅ 通过 | 法律分析、建议、风险提示完整 |
| 合同起草 | ✅ 通过 | 生成完整规范的合同文本 |
| 合同审查 | ✅ 通过 | 风险识别、修改建议准确 |

---

## 📚 文档

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目说明（本文件） |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | 部署文档 |
| [API.md](docs/API.md) | API接口文档 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目完成总结 |

---

## 🎉 项目亮点

### 1. 主脑智能体
- ✅ 智能意图识别
- ✅ 自动任务路由
- ✅ 降级处理机制

### 2. 技能模块化
- ✅ 独立的技能实现
- ✅ 统一的接口规范
- ✅ 灵活可扩展

### 3. 服务注册表
- ✅ 自动技能注册
- ✅ 动态技能管理
- ✅ 分类组织

### 4. 完整的文档
- ✅ 详细的部署文档
- ✅ 完整的API文档
- ✅ 测试覆盖

---

## 🚀 部署

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

详细部署步骤请参考：[部署文档](docs/DEPLOYMENT.md)

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件：support@example.com

---

## 📄 开源协议

本项目采用 MIT 协议开源。

---

<div align="center">

**宁律师小程序 - 让法律服务触手可及**

**版本**：2.0.0-independent
**架构**：完全独立
**完成时间**：2025-01-29
**状态**：✅ 已完成

Made with ❤️ by NingLawyer Team

</div>
