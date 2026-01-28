# 宁律师法律咨询小程序矩阵

## 项目简介

宁律师是一个基于 AI 技术的法律咨询服务平台，采用微信小程序矩阵架构，提供全方位的法律服务。

### 产品矩阵

- **法律教官** - 主小程序，导航中枢
- **宁律师家族** - 7x24小时法律咨询（7个专业领域）
- **码上签约** - 扫码签约，智能指导
- **理约** - 合同全生命周期管理
- **怎么判** - 诉讼维权，专业指导
- **防风险** - 企业合规风险防控

### 全流程服务

```
咨询 → 起草 → 签署 → 履约 → 违约 → 维权
```

## 技术栈

### 前端
- 微信小程序原生框架
- 组件化开发
- 微信UI设计风格

### 后端
- **框架**: LangChain + LangGraph
- **模型**: doubao-seed + doubao-voice
- **存储**: PostgreSQL + Milvus + Neo4j + Redis + S3
- **API**: Flask + RESTful

## 项目结构

```
ninglawyer-miniapp/
├── legal-instructor/          # 主小程序：法律教官
├── ning-lawyer/              # 宁律师家族
│   ├── civil/               # 宁律师·民事
│   ├── criminal/            # 宁律师·刑事
│   ├── contract/            # 宁律师·合同
│   ├── labor/               # 宁律师·劳动
│   ├── company/             # 宁律师·公司
│   ├── ip/                  # 宁律师·知识产权
│   └── marriage/            # 宁律师·婚姻
├── mashangqianyue/          # 码上签约
├── liyue/                   # 理约
├── zenmepan/                # 怎么判
├── fangfengxian/            # 防风险（已开发）
├── src/                     # 后端代码
│   ├── agents/             # AGENT 代码
│   ├── skills/             # SKILL 包
│   ├── tools/              # 工具
│   ├── api/                # API 接口
│   ├── storage/            # 存储层
│   ├── config/             # 配置
│   └── utils/              # 工具函数
├── components/             # 公共组件
├── tests/                  # 测试
├── docs/                   # 文档
└── assets/                 # 资源文件
```

## 快速开始

### 环境要求

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Neo4j 5+
- Milvus 2.3+

### 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入真实配置
```

### 启动服务

```bash
# 启动后端服务
python src/main.py

# 访问 API 文档
open http://localhost:8080/docs
```

### 小程序开发

1. 使用微信开发者工具打开对应的小程序目录
2. 配置 AppID
3. 点击编译查看效果

## 开发指南

### 组件开发

所有组件位于 `components/` 目录，遵循以下规范：

```javascript
// components/example-component/example-component.js
Component({
  properties: {
    // 组件属性
    title: {
      type: String,
      value: ''
    }
  },

  data: {
    // 组件内部数据
  },

  methods: {
    // 组件方法
    handleTap() {
      this.triggerEvent('tap');
    }
  }
});
```

### AGENT 开发

所有 AGENT 继承自 `BaseAgent`：

```python
from src.agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        # 初始化配置
    
    def execute(self, input_data):
        # 执行逻辑
        return result
```

### SKILL 开发

所有 SKILL 使用 `@skill` 装饰器：

```python
from src.skills.base_skill import BaseSkill
from src.utils.skill_decorator import skill

@skill(name="我的技能")
class MySkill(BaseSkill):
    def execute(self, *args, **kwargs):
        # 执行逻辑
        return result
```

## 测试

```bash
# 运行所有测试
pytest tests/

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 生成覆盖率报告
pytest --cov=src tests/
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t ninglawyer-api .

# 运行容器
docker run -p 8080:8080 ninglawyer-api
```

### Kubernetes 部署

```bash
kubectl apply -f k8s/
```

## 文档

详细文档请查看 `docs/` 目录：

- [开发指南](docs/DEVELOPMENT.md)
- [API 文档](docs/API.md)
- [部署指南](docs/DEPLOYMENT.md)
- [常见问题](docs/FAQ.md)

## 贡献指南

欢迎提交 Pull Request！

## 许可证

MIT License

## 联系方式

- 作者: HeGui
- 邮箱: hegui@example.com
