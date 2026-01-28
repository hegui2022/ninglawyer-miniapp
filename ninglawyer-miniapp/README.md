# 宁律师法律咨询小程序矩阵

## 项目概述

宁律师法律咨询小程序矩阵是一个基于 AI 技术的全方位法律服务平台，采用微信小程序矩阵架构，为企业及个人提供从咨询到维权的全流程法律服务。

### 核心理念
**代码即法律** - 将律师技能嵌入工作流，实现企业管理和风险防控一体化

## 系统架构

### 小程序矩阵
1. **法律教官**（主程序）
   - 导航中心，统一入口
   - 用户账号管理
   - 服务推荐与引导

2. **宁律师家族**（子程序群）
   - 宁律师·民事：民事纠纷、侵权责任、债务纠纷
   - 宁律师·刑事：刑事辩护、取保候审、减刑申请
   - 宁律师·劳动：劳动合同、社保公积金、工伤赔偿
   - 宁律师·公司：公司设立、股权结构、合规管理
   - 宁律师·知识产权：商标、专利、著作权
   - 宁律师·婚姻：离婚、抚养权、财产分割
   - 宁律师·合同：合同起草、审查、修改

3. **码上签约**
   - 合同创建与模板
   - 在线签署
   - 存证管理

4. **理约**
   - 合同履约跟踪
   - 到期提醒
   - 争议预警

5. **怎么判**
   - 案例搜索
   - 智能分析
   - 判决预测

6. **防风险**
   - 风险评估
   - 合规检查
   - 风险预警

## 技术栈

### 后端
- **AI 模型**: doubao-seed (豆包 Agent 优化版)
- **框架**: LangChain, LangGraph
- **语音**: 豆包语音 (ASR/TTS)
- **知识库**: coze-knowledge-base (RAG)
- **数据库**: PostgreSQL (业务数据), Milvus (向量), Redis (缓存), Neo4j (知识图谱), S3 (文件存储)
- **API**: Flask (RESTful)

### 前端
- **框架**: 微信小程序原生框架
- **组件化**: 自定义组件库
- **设计**: 微信/企业微信风格

## 功能特性

### 1. 智能咨询
- 自然语言对话
- 多轮上下文理解
- 语音交互（ASR/TTS）
- 知识库 RAG 检索

### 2. 合同服务
- 智能起草
- 合同审查
- 在线签署
- 履约跟踪

### 3. 风险管理
- 风险评估
- 合规检查
- 预警提示

### 4. 案例分析
- 案例搜索
- 智能分析
- 判决预测

## 目录结构

```
ninglawyer-miniapp/
├── src/                      # 源代码
│   ├── agents/              # AI Agent
│   │   ├── ning_lawyer_template.py    # 基类模板
│   │   ├── lawyer_civil.py            # 民事律师
│   │   ├── lawyer_criminal.py         # 刑事律师
│   │   ├── lawyer_contract.py         # 合同律师
│   │   ├── lawyer_labor.py            # 劳动律师
│   │   ├── lawyer_company.py          # 公司律师
│   │   ├── lawyer_ip.py               # 知识产权律师
│   │   ├── lawyer_marriage.py         # 婚姻律师
│   │   ├── lawyer_factory.py          # 工厂类
│   │   └── master_agent.py            # 主控 Agent
│   ├── tools/               # 工具
│   │   ├── legal_search.py            # 法律检索
│   │   ├── contract_analysis.py       # 合同分析
│   │   ├── risk_assessment.py         # 风险评估
│   │   └── case_search.py             # 案例搜索
│   ├── skills/              # 技能
│   │   ├── consultation.py            # 咨询技能
│   │   ├── drafting.py                # 起草技能
│   │   └── review.py                  # 审查技能
│   ├── api/                 # API 接口
│   │   ├── consultation.py            # 咨询接口
│   │   ├── contract.py                # 合同接口
│   │   └── routes.py                  # 路由注册
│   ├── storage/             # 存储
│   │   ├── db.py                      # 数据库
│   │   ├── vector_store.py            # 向量存储
│   │   └── cache.py                   # 缓存
│   └── config/              # 配置
│       └── models.py                  # 数据模型
├── config/                  # 配置文件
│   └── agent_llm_config.json          # LLM 配置
├── components/              # 公共组件
│   ├── nav-bar/                      # 导航栏
│   ├── service-card/                 # 服务卡片
│   ├── lawyer-avatar/                # 律师头像
│   ├── message-item/                 # 消息项
│   ├── loading/                      # 加载中
│   └── empty/                        # 空状态
├── legal-instructor/         # 法律教官小程序
│   └── pages/
│       ├── index/                    # 首页
│       └── lawyer-family/            # 宁律师家族
├── code-signing/             # 码上签约小程序
│   └── pages/
│       ├── index/                    # 首页
│       ├── create/                   # 创建合同
│       └── sign/                     # 签署
├── manage-contract/          # 理约小程序
│   └── pages/
│       ├── list/                     # 合同列表
│       └── performance/              # 履约跟踪
├── how-to-judge/             # 怎么判小程序
│   └── pages/
│       ├── search/                   # 案例搜索
│       └── analyze/                  # 智能分析
├── prevent-risk/             # 防风险小程序
│   └── pages/
│       └── index/                    # 首页
├── scripts/                 # 脚本
│   ├── deploy.sh                     # 部署
│   ├── start.sh                      # 启动
│   └── stop.sh                       # 停止
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 快速开始

### 环境要求
- Python 3.9+
- Node.js 16+
- Docker & Docker Compose
- 微信开发者工具

### 安装依赖

```bash
# 后端依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py
```

### 启动服务

```bash
# 使用 Docker Compose
docker-compose up -d

# 或使用脚本
./scripts/start.sh
```

### 配置

编辑 `config/agent_llm_config.json` 配置 AI 模型参数：

```json
{
    "config": {
        "model": "doubao-seed-1-6-251015",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_completion_tokens": 10000
    }
}
```

### 小程序开发

1. 使用微信开发者工具打开对应小程序目录
2. 配置 `app.js` 中的 API 地址
3. 编译并预览

## API 文档

### 咨询服务
- `POST /api/consultation/chat` - 咨询对话
- `GET /api/consultation/history` - 咨询历史

### 合同服务
- `POST /api/contract/create` - 创建合同
- `POST /api/contract/draft` - 起草合同
- `POST /api/contract/sign` - 签署合同
- `GET /api/contract/list` - 合同列表
- `GET /api/contract/performance` - 履约跟踪

### 风险服务
- `GET /api/risk/profile` - 风险档案
- `POST /api/risk/analyze` - 风险分析

## 部署

```bash
# 部署到生产环境
./scripts/deploy.sh prod
```

## 测试

```bash
# 运行单元测试
pytest tests/

# 运行集成测试
pytest tests/integration/
```

## 开发规范

### 代码风格
- Python: PEP 8
- JavaScript: ESLint
- 使用类型注解
- 编写单元测试

### Git 提交
```
feat: 新功能
fix: 修复
docs: 文档
style: 格式
refactor: 重构
test: 测试
chore: 构建
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 许可证

Copyright © 2024 宁律师团队. All rights reserved.

## 联系方式

- 官网: https://ninglawyer.com
- 邮箱: contact@ninglawyer.com
- 微信: ninglawyer_bot
