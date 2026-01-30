# 智能法律服务后端系统

## 项目概述

基于 Python + Flask + LangChain + LangGraph 的智能法律服务后端系统，采用扣子官方的 SKILL 框架构建，提供智能体、知识库、工作流、技能的统一封装与集成。

## 技术栈

- **后端框架**: Python 3.10+ + Flask
- **AI框架**: LangChain + LangGraph
- **扣子框架**: SKILL 框架（Skill Registry + Bot Registry）
- **工具库**: LLMClient, 语音, 检索
- **编码规范**: PEP 8 (Python)

## 目录结构

```
backend/
├── src/
│   ├── services/                    # 服务层
│   │   ├── base_service.py         # 第三方API基类
│   │   ├── coze_agent_service.py   # 扣子智能体服务
│   │   ├── coze_knowledge_service.py # 扣子知识库服务
│   │   ├── coze_workflow_service.py # 扣子工作流服务
│   │   └── coze_skill_service.py   # 扣子技能服务
│   ├── adapters/                    # 数据适配器层
│   │   ├── base_adapter.py         # 数据适配器基类
│   │   └── legal_knowledge_adapter.py # 法律知识库适配器
│   ├── skills/                      # 技能层
│   │   └── ...                     # 具体技能实现
│   ├── tools/                       # 工具层
│   │   └── ...                     # 具体工具实现
│   └── main.py                      # 应用入口
├── tests/                           # 单元测试
│   ├── test_coze_agent_service.py
│   ├── test_coze_knowledge_service.py
│   └── test_data_adapter.py
├── examples/                        # 示例代码
│   ├── coze_agent_example.py
│   ├── coze_knowledge_example.py
│   └── data_adapter_example.py
├── docs/                            # 文档
│   ├── coze_agent_service.md
│   ├── coze_knowledge_service.md
│   ├── coze_workflow_service.md
│   ├── coze_skill_service.md
│   └── data_adapter.md
├── requirements.txt                 # 依赖列表
├── .env.example                     # 环境变量示例
└── README.md                        # 本文档
```

## 核心功能

### 1. 扣子服务集成

- **智能体服务** (`CozeAgentService`): 管理扣子智能体的创建、调用和管理
- **知识库服务** (`CozeKnowledgeService`): 管理扣子知识库的导入、检索和管理
- **工作流服务** (`CozeWorkflowService`): 管理扣子工作流的执行和管理
- **技能服务** (`CozeSkillService`): 管理扣子技能的注册和调用

### 2. 数据适配层

- **数据适配器基类** (`DataAdapterBase`): 提供三阶段数据处理架构（清洗、转换、增强）
- **法律知识库适配器** (`LegalKnowledgeAdapter`): 专门用于法律数据的格式转换
- **正则表达式 + LLM增强**: 优先使用正则表达式提取结构化信息，按需使用LLM生成摘要

### 3. 第三方API统一封装

- **BaseThirdPartyAPIService基类**: 统一的错误处理、请求管理和数据适配
- 支持扣子、微信、支付宝等第三方API
- 统一的错误码处理（401/404/400/429等）

## 快速开始

### 环境准备

```bash
# 1. 克隆项目
git clone <repository_url>
cd backend

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入必要的配置
```

### 基础用法

#### 1. 使用扣子智能体服务

```python
from backend.src.services import get_coze_agent_service

agent_service = get_coze_agent_service(access_token="YOUR_ACCESS_TOKEN")

# 调用智能体
result = agent_service.chat(
    bot_id="YOUR_BOT_ID",
    message="你好"
)
```

#### 2. 使用扣子知识库服务

```python
from backend.src.services import get_coze_knowledge_service
from backend.src.adapters import get_legal_knowledge_adapter

kb_service = get_coze_knowledge_service(
    access_token="YOUR_ACCESS_TOKEN",
    dataset_id="YOUR_DATASET_ID"
)

# 检索知识库
raw_result = kb_service.search(
    query="刑法第二百六十四条",
    top_k=3
)

# 使用数据适配器转换格式
adapter = get_legal_knowledge_adapter(enable_llm_enhance=False)
adapted_result = adapter.adapt(raw_result)
```

#### 3. 使用数据适配器

```python
from backend.src.adapters import get_legal_knowledge_adapter

# 获取适配器实例
adapter = get_legal_knowledge_adapter(enable_llm_enhance=True)

# 适配数据
result = adapter.adapt(raw_data)

# 使用适配后的数据
for item in result["data"]:
    print(f"法条编号: {item['article_number']}")
    print(f"罪名: {item['crime_name']}")
    print(f"摘要: {item['summary']}")
    print(f"关键点: {item['key_points']}")
```

## 架构设计

### SKILL 框架

```
┌─────────────────────────────────────────┐
│         前端（微信小程序/H5）            │
└────────────────┬────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────┐
│         Master Brain（主脑）             │
│         路由决策引擎                      │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    ↓            ↓            ↓
┌─────────┐ ┌──────────┐ ┌──────────┐
│ Skill 1 │ │ Skill 2  │ │ Skill 3  │
│ (技能)  │ │ (技能)   │ │ (技能)   │
└────┬────┘ └────┬─────┘ └────┬─────┘
     │           │            │
     ↓           ↓            ↓
┌──────────────────────────────────────┐
│            Tool（工具层）              │
│  - LLMClient                         │
│  - 语音处理                          │
│  - 检索服务                          │
└──────────────────────────────────────┘
```

### 数据流转

```
前端请求 → Master Brain → Skill → Tool → 第三方API → 数据适配 → 返回前端
```

## 文档

- [扣子智能体服务文档](./docs/coze_agent_service.md)
- [扣子知识库服务文档](./docs/coze_knowledge_service.md)
- [扣子工作流服务文档](./docs/coze_workflow_service.md)
- [扣子技能服务文档](./docs/coze_skill_service.md)
- [数据适配器文档](./docs/data_adapter.md)

## 开发指南

### 编码规范

- Python: 遵循 PEP 8 规范
- 使用 `black` 格式化代码
- 使用 `flake8` 检查代码质量
- 使用 `mypy` 进行类型检查

### 测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行单个测试文件
python -m pytest tests/test_coze_agent_service.py -v

# 运行特定测试
python -m pytest tests/test_coze_agent_service.py::TestCozeAgentService::test_create_bot -v
```

### 运行示例

```bash
# 运行智能体示例
python examples/coze_agent_example.py

# 运行知识库示例
python examples/coze_knowledge_example.py

# 运行数据适配器示例
python examples/data_adapter_example.py
```

## 环境变量

参考 `.env.example` 文件配置以下环境变量：

```env
# 扣子配置
COZE_ACCESS_TOKEN=your_access_token
COZE_API_BASE_URL=https://api.coze.cn

# LLM配置
COZE_LLM_MODEL=doubao-seed-1-8-251228
COZE_LLM_API_KEY=your_llm_api_key
COZE_LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 应用配置
APP_ENV=development
APP_PORT=5000
APP_DEBUG=True
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t legal-service-backend .

# 运行容器
docker run -d -p 5000:5000 \
  --env-file .env \
  --name legal-service-backend \
  legal-service-backend
```

### 传统部署

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python src/main.py
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目主页: [GitHub Repository](https://github.com/your-username/legal-service-backend)
- 问题反馈: [GitHub Issues](https://github.com/your-username/legal-service-backend/issues)

## 更新日志

### v1.0.0 (2025-01-15)

- ✅ 实现扣子智能体服务
- ✅ 实现扣子知识库服务
- ✅ 实现扣子工作流服务
- ✅ 实现扣子技能服务
- ✅ 实现数据适配层（基类 + 法律知识库适配器）
- ✅ 实现第三方API统一封装
- ✅ 完整的单元测试和示例代码
- ✅ 完善的文档

---

**注意**: 本项目遵循扣子官方 SKILL 框架规范，拒绝在 Agent 中硬编码数据或引入不符合框架的知识库逻辑。所有数据获取必须通过 Skill 调用 LLM 或工具实现。
