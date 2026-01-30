# 宁律师法律服务项目

基于 Monorepo 架构的智能法律服务生态系统，包含多个微信小程序和统一的后端服务。

## 项目架构

```
ninglawyer-legal-services/
├── packages/                      # npm 包
│   └── @ninglawyer/shared/       #    共享组件和工具
├── miniprograms/                 # 小程序集合
│   ├── ninglawyer-main/          #    主小程序（宁律师法律咨询）
│   ├── fangfengxian/             #    防风险评估小程序
│   ├── legal-instructor/         #    法律教官小程序
│   ├── lyue/                     #    乐约小程序
│   ├── zenme-pan/                #    怎么判小程序
│   └── code-signing/             #    码上签约小程序
├── backend/                      # 后端服务
│   ├── src/                      #    源代码
│   ├── config/                   #    配置文件
│   ├── tests/                    #    测试代码
│   └── scripts/                  #    脚本
├── docs/                         # 文档
├── scripts/                      # 全局脚本
└── infrastructure/               # 基础设施
```

## 核心功能

### 后端服务
- 智能法律咨询（基于豆包大语言模型）
- 合同起草助手（支持 6 种合同类型）
- 合同审查（风险识别和建议）
- 合同管理系统（保存、查询、更新）
- MCP 服务（知识库、语音、向量检索）
- API 接口（RESTful）

### 小程序
- **宁律师法律咨询**：法律咨询、合同管理、AI 对话
- **防风险**：合同风险识别和预警
- **法律教官**：律师工具和统计
- **理约**：合同提醒和管理
- **怎么判**：案例查询和法律咨询
- **码上签约**：电子签名和合同管理

## 技术栈

### 后端
- **框架**: Python + Flask
- **AI**: 豆包大语言模型（LangChain + LangGraph）
- **语音**: 豆包语音（TTS/ASR）
- **数据库**: PostgreSQL
- **存储**: S3 对象存储

### 小程序
- **框架**: 微信小程序原生
- **共享包**: @ninglawyer/shared（npm）
- **UI**: 豆包风格

## 快速开始

### 前置要求
- Node.js >= 14
- Python >= 3.8
- 微信开发者工具

### 1. 克隆项目
```bash
git clone https://github.com/ninglawyer/ninglawyer-legal-services.git
cd ninglawyer-legal-services
```

### 2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 3. 启动后端服务
```bash
cd backend
python3 main.py
```

### 4. 开发小程序
```bash
# 安装共享包
cd packages/@ninglawyer/shared
npm install

# 进入小程序目录
cd ../../miniprograms/ninglawyer-main

# 安装依赖
npm install

# 使用微信开发者工具打开该目录
```

## 共享包使用

### 安装共享包
```bash
cd miniprograms/ninglawyer-main
npm install
```

### 构建 npm
在微信开发者工具中：工具 -> 构建 npm

### 使用示例
```javascript
// 导入工具
import { request, auth } from '@ninglawyer/shared'

// API 请求
const data = await request('/user/info')

// 认证
auth.setToken('your_token')
```

## 文档

- [架构文档](docs/architecture/)
- [API 文档](docs/api/)
- [部署文档](docs/deployment/)
- [共享包文档](packages/@ninglawyer/shared/README.md)
- [使用指南](docs/development/)

## 开发指南

### 添加新小程序
1. 在 `miniprograms/` 下创建新目录
2. 复制 `miniprograms/ninglawyer-main/package.json`
3. 安装依赖：`npm install`
4. 使用微信开发者工具打开

### 修改共享代码
1. 修改 `packages/@ninglawyer/shared/` 下的代码
2. 更新版本：`npm version patch`
3. 在小程序中重新构建 npm

### 部署
```bash
# 部署后端
cd backend
./scripts/deploy.sh

# 部署小程序
# 使用微信开发者工具上传
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

- 邮箱: support@ninglawyer.com
- 官网: https://www.ninglawyer.com

## 更新日志

### v1.0.0 (2025-01-30)
- 初始版本发布
- 实现 Monorepo 架构
- 创建共享包 @ninglawyer/shared
- 整合所有小程序
- 完成后端服务迁移
