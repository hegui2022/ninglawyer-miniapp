# 宁律师智能法律咨询 Agent

基于豆包大语言模型、LangChain 和 LangGraph 框架构建的智能法律咨询 Agent，集成语音交互与知识库 RAG 能力，支持文本+语音同步输出。

## 核心功能

### 1. 法律咨询
- 支持多轮对话的自然语言法律咨询
- 基于知识库的精准回答（RAG）
- 语音输入与语音输出（豆包语音）

### 2. 合同起草助手 V4.0
采用多智能体架构，支持以下合同类型的智能起草：

- **标准劳动合同**：适用于全日制用工的正式劳动合同
- **非全日制用工合同**：适用于兼职、小时工等非全日制用工
- **实习协议**：适用于在校学生实习场景
- **退休返聘协议**：适用于退休人员返聘工作场景
- **项目制合同**：适用于项目承包、工程承揽等场景
- **劳务派遣合同**：适用于劳务派遣三方合作场景

### 合同导出功能
- 支持 Word 格式导出（.docx）
- 支持 PDF 格式导出（.pdf）

## 技术栈

- **模型**：doubao-seed-1-8-251228 (豆包 Agent 优化版)
- **框架**：LangChain, LangGraph
- **语音**：豆包语音 (TTS/ASR)
- **知识库**：coze-coding-dev-sdk Knowledge
- **存储**：S3 对象存储
- **测试服务**：Flask (用于模拟对话界面)
- **移动端**：微信小程序原生框架

## 多智能体架构

合同起草助手采用三层架构：

### 1. Master Agent (主控代理)
- 意图识别：判断用户是否需要起草合同
- 场景分类：识别合同类型
- 代理分发：将任务分发给对应的场景代理

### 2. Scenario Agents (场景代理)
- `StandardLaborContractAgent`：标准劳动合同代理
- `PartTimeContractAgent`：非全日制用工合同代理
- `InternAgreementAgent`：实习协议代理
- `RetiredReemploymentAgent`：退休返聘协议代理
- `ProjectContractAgent`：项目制合同代理
- `DispatchContractAgent`：劳务派遣合同代理

### 3. Skill Agents (技能代理)
- 每个场景代理包含多个技能代理
- 负责处理合同的各个条款（基本信息、合同期限、工作内容、劳动报酬等）

## 使用方法

### 本地运行

#### 运行工作流
```bash
bash scripts/local_run.sh -m flow
```

#### 运行单个节点
```bash
bash scripts/local_run.sh -m node -n node_name
```

#### 启动 HTTP 服务
```bash
bash scripts/http_run.sh -m http -p 5000
```

### 合同起草示例

**对话 1：开始起草**
```
用户：我要起草一份劳动合同
Agent：请选择合同类型：
1. 标准劳动合同
2. 非全日制用工合同
3. 实习协议
4. 退休返聘协议
5. 项目制合同
6. 劳务派遣合同

用户：1
Agent：好的，我们开始起草标准劳动合同。请填写以下信息：
[显示第一步信息收集表单]
```

**对话 2：填写信息**
```
用户：用人单位：XX公司，地址：北京市朝阳区...
Agent：已记录基本信息。接下来请填写合同期限：
[显示第二步信息收集表单]
```

**对话 3：生成合同**
```
用户：（填写完所有信息后）
Agent：合同已生成！是否需要导出？
1. 导出为 Word
2. 导出为 PDF

用户：2
Agent：合同已导出为 PDF，文件路径：...
```

## 文件结构

```
.
├── config                       # 配置目录
│   └── agent_llm_config.json    # 模型配置
├── docs                         # 文档
├── scripts                      # 脚本
│   ├── local_run.sh            # 本地运行脚本
│   └── http_run.sh             # HTTP 服务启动脚本
├── assets                       # 资源目录
│   └── contracts               # 合同模板
├── tests                        # 单元测试
├── src                          # 源码
│   ├── agents                  # Agent 代码
│   │   └── agent.py            # 主 Agent 实现
│   ├── tools                   # 工具定义
│   │   ├── contract_drafter_master.py    # 主控代理
│   │   ├── contract_scenarios.py         # 场景代理
│   │   ├── contract_skills               # 技能库
│   │   │   ├── __init__.py
│   │   │   ├── basic_skills.py           # 基础技能
│   │   │   ├── intern_skills.py          # 实习协议技能
│   │   │   ├── retired_skills.py         # 退休返聘技能
│   │   │   ├── project_skills.py         # 项目制技能
│   │   │   └── dispatch_skills.py        # 劳务派遣技能
│   │   ├── contract_drafting_tool.py     # 合同起草工具
│   │   └── contract_exporter.py          # 合同导出工具
│   ├── storage                  # 存储
│   │   └── memory
│   │       └── memory_saver.py  # 短期记忆
│   └── main.py                  # 主入口
├── AGENT.md                     # 模型规范
├── README.md                    # 项目说明
├── requirements.txt             # 依赖
└── .coze                        # 配置
```

## 开发规范

- 遵循 LangChain 工程规范
- 使用 LangGraph 1.0 版本
- 严格遵循工程规范（详见 AGENT.md）

## 更新日志

### V4.0 (2025-01-XX)
- 新增实习协议支持
- 新增退休返聘协议支持
- 新增项目制合同支持
- 新增劳务派遣合同支持
- 新增 PDF 导出功能
- 优化场景分类器权重
- 修复技能类继承问题

### V3.0
- 新增非全日制用工合同支持
- 新增 Word 导出功能
- 优化智能输入解析器

### V2.0
- 新增合同起草助手功能
- 支持标准劳动合同起草
- 新增多智能体架构

### V1.0
- 基础法律咨询功能
- 知识库 RAG 支持
- 语音交互功能
- 微信小程序端支持

