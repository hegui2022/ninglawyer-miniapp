# 宁律师法律咨询小程序矩阵

基于 AI 技术的全方位法律服务平台，实现从咨询、起草、签约到履约、违约、维权的全流程法律服务。

## 项目架构

```
ninglawyer-miniapp/
├── src/                        # 后端源码
│   ├── agents/                 # AGENT 核心代码
│   │   ├── master_agent.py     # 主脑 - 意图识别和路由
│   │   ├── lawyer_factory.py   # 宁律师工厂
│   │   ├── ning_lawyer_template.py  # 宁律师模板
│   │   ├── lawyer_civil.py     # 宁律师·民事
│   │   ├── lawyer_criminal.py  # 宁律师·刑事
│   │   ├── lawyer_labor.py     # 宁律师·劳动
│   │   ├── lawyer_company.py   # 宁律师·公司
│   │   ├── lawyer_ip.py        # 宁律师·知识产权
│   │   ├── lawyer_marriage.py  # 宁律师·婚姻
│   │   └── lawyer_contract.py  # 宁律师·合同
│   ├── api/                    # API 接口
│   │   ├── consultation.py     # 咨询 API
│   │   └── contract.py         # 合同 API
│   ├── config/                 # 配置文件
│   │   └── lawyer_domains.py   # 宁律师领域配置
│   ├── utils/                  # 工具类
│   │   ├── config.py           # 配置工具
│   │   ├── logger.py           # 日志工具
│   │   └── response.py         # 响应工具
│   └── main.py                 # 主程序入口
├── legal-instructor/           # 法律教官主小程序
│   ├── pages/                  # 页面
│   │   ├── index/              # 首页
│   │   └── lawyer-family/      # 宁律师家族
│   └── app.json                # 小程序配置
├── code-signing/               # 码上签约小程序
│   ├── pages/
│   │   ├── index/              # 首页
│   │   ├── create/             # 创建合同
│   │   ├── sign/               # 签署合同
│   │   └── record/             # 签署记录
│   └── app.json
├── manage-contract/            # 理约小程序
│   ├── pages/
│   │   ├── index/              # 首页
│   │   ├── list/               # 合同列表
│   │   ├── reminder/           # 到期提醒
│   │   └── performance/        # 履约跟踪
│   └── app.json
├── how-to-judge/               # 怎么判小程序
│   ├── pages/
│   │   ├── index/              # 首页
│   │   ├── search/             # 案例搜索
│   │   ├── analyze/            # 智能分析
│   │   └── lawyer/             # 律师推荐
│   └── app.json
├── components/                 # 公共组件库
│   ├── nav-bar/                # 导航栏
│   ├── service-card/           # 服务卡片
│   ├── lawyer-avatar/          # 律师头像
│   ├── message-item/           # 消息项
│   ├── loading/                # 加载中
│   └── empty/                  # 空状态
├── tests/                      # 测试代码
│   ├── test_integration.py     # 集成测试
│   └── test_all_lawyers.py     # 宁律师测试
├── scripts/                    # 脚本
│   └── deploy.sh               # 部署脚本
├── requirements.txt            # Python 依赖
└── README.md                   # 项目文档
```

## 技术栈

### 后端
- **框架**: Flask
- **AI框架**: LangChain, LangGraph
- **模型**: doubao-seed (豆包 Agent 优化版)
- **日志**: loguru
- **测试**: pytest

### 前端
- **平台**: 微信小程序
- **框架**: 微信小程序原生框架
- **样式**: 微信/企业微信设计风格
- **组件**: 自定义组件库

## 核心功能

### 1. 宁律师家族（7个专业领域）

| 宁律师 | 领域 | 核心能力 |
|--------|------|----------|
| 宁律师·民事 | 民事法律 | 合同纠纷、侵权责任、婚姻家庭、财产分割 |
| 宁律师·刑事 | 刑事法律 | 刑事辩护、取保候审、减刑假释 |
| 宁律师·劳动 | 劳动法律 | 劳动合同、工资纠纷、工伤赔偿、劳动仲裁 |
| 宁律师·公司 | 公司法律 | 公司设立、公司治理、股权设计、公司并购 |
| 宁律师·知识产权 | 知识产权 | 专利申请、商标注册、版权登记、侵权维权 |
| 宁律师·婚姻 | 婚姻家庭 | 离婚诉讼、抚养权、财产分割、继承纠纷 |
| 宁律师·合同 | 合同法律 | 合同起草、合同审查、风险分析 |

### 2. 小程序矩阵

#### 法律教官（主小程序）
- 导航中枢
- 首页展示
- 宁律师家族页面

#### 码上签约
- 合同创建
- 电子签署
- 签署记录管理

#### 理约
- 合同列表
- 到期提醒
- 履约跟踪

#### 怎么判
- 案例搜索
- 智能分析
- 律师推荐

### 3. 全流程服务

```
咨询（宁律师） → 起草（宁律师·合同） → 签署（码上签约） → 履约（理约） → 违约（怎么判） → 维权（怎么判）
```

## 快速开始

### 1. 环境要求

- Python 3.8+
- 微信开发者工具

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```env
# 模型配置
MODEL_NAME=doubao-seed
MODEL_BASE_URL=https://your-model-api.com
MODEL_API_KEY=your-api-key

# 服务配置
API_PORT=5000
DEBUG=True

# 数据库配置（可选）
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ninglawyer
DB_USER=postgres
DB_PASSWORD=password
```

### 4. 运行测试

```bash
# 测试所有宁律师
python tests/test_all_lawyers.py

# 集成测试
python tests/test_integration.py
```

### 5. 启动服务

```bash
# 方式1：直接启动
python src/main.py

# 方式2：使用部署脚本
bash scripts/deploy.sh
```

### 6. 开发小程序

使用微信开发者工具打开对应小程序目录：
- `legal-instructor/` - 法律教官
- `code-signing/` - 码上签约
- `manage-contract/` - 理约
- `how-to-judge/` - 怎么判

## API 文档

### 咨询 API

#### 路由咨询
```
POST /consultation/route
{
  "input": "用户输入",
  "context": {}
}
```

#### 文字咨询
```
POST /consultation/consult
{
  "domain": "civil",
  "question": "咨询问题",
  "chat_history": []
}
```

#### 获取宁律师列表
```
GET /consultation/lawyers
```

#### 获取宁律师信息
```
GET /consultation/lawyer/{domain}
```

### 合同 API

#### 起草合同
```
POST /contract/draft
{
  "contract_type": "采购合同",
  "partyA": "甲方",
  "partyB": "乙方",
  "terms": "主要条款",
  "domain": "contract"
}
```

#### 审查合同
```
POST /contract/review
{
  "contract_text": "合同文本",
  "domain": "contract"
}
```

#### 获取合同模板
```
GET /contract/templates
```

#### 分析纠纷
```
POST /contract/analyze
{
  "dispute_type": "合同纠纷",
  "description": "纠纷描述",
  "amount": 10000,
  "evidence": "相关证据"
}
```

## 组件使用

### nav-bar 导航栏

```html
<nav-bar
  title="页面标题"
  background="#07C160"
  textColor="#ffffff"
  showBack="{{true}}"
  showHome="{{false}}">
</nav-bar>
```

### service-card 服务卡片

```html
<service-card
  title="服务名称"
  description="服务描述"
  icon="/assets/icons/icon.png"
  tag="热门"
  tagType="primary"
  count="1000"
  url="/pages/detail/detail">
</service-card>
```

### lawyer-avatar 律师头像

```html
<lawyer-avatar
  name="宁律师·民事"
  avatar="/assets/images/lawyers/civil.png"
  domain="民事"
  status="online"
  size="default"
  bind:tap="onLawyerTap">
</lawyer-avatar>
```

## 测试结果

### 集成测试

```
✓ Master Agent 测试通过
✓ Lawyer Factory 测试通过
✓ 宁律师·民事 测试通过
✓ 宁律师·合同 测试通过
✓ 全流程测试通过

总计：5/5 通过
```

### 宁律师测试

```
✓ civil 测试通过
✓ criminal 测试通过
✓ labor 测试通过
✓ company 测试通过
✓ ip 测试通过
✓ marriage 测试通过
✓ contract 测试通过
✓ LawyerFactory 测试通过

总计：8/8 通过
```

## 开发规范

### 代码规范

1. 使用 Python 3.8+ 语法
2. 遵循 PEP 8 编码规范
3. 使用类型注解
4. 编写单元测试
5. 添加必要的注释

### 组件规范

1. 组件命名采用 kebab-case
2. 使用组件时传入必要属性
3. 通过 triggerEvent 传递事件
4. 组件样式独立管理

### API 规范

1. 使用 RESTful 风格
2. 统一返回格式
3. 添加错误处理
4. 记录日志

## 设计规范

### 微信/企业微信风格

- 主色：#07C160
- 成功色：#07C160
- 警告色：#FF9500
- 错误色：#FA5151
- 圆角：8rpx / 12rpx / 16rpx
- 间距：8rpx / 16rpx / 24rpx / 32rpx

## 项目特点

1. **组件化开发**：前后端分离，代码高可读性、维护性、扩展性
2. **微信/企业微信风格**：UI 设计完全采用微信和企业微信设计规范
3. **矩阵架构**：主程序导航，子程序业务，职责清晰
4. **可复制模板**：宁律师采用工厂模式，易于扩展新领域
5. **全流程服务**：咨询→起草→签约→履约→违约→维权，闭环服务

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。

## 联系我们

- 项目主页：[宁律师官网]
- 技术支持：support@ninglawyer.com
- 商务合作：business@ninglawyer.com

---

© 2024 宁律师. All rights reserved.
