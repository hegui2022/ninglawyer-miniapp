# 法律教官系统 - 使用指南

## 系统架构

```
┌─────────────┐
│   PC端前端   │  (Vue 3 + Element Plus)
│  案例录入    │  - 录入法律案例
└──────┬──────┘  - 提交到后端
       │
       ↓ HTTP
┌─────────────┐
│   后端API    │  (Flask + SQLAlchemy)
│  数据存储    │  - 接收案例数据
└──────┬──────┘  - 存储到数据库
       │
       ↓ HTTP
┌─────────────┐
│  小程序端    │  (微信小程序)
│  怎么判展示  │  - 检索案例
│             │  - 展示案例详情
└─────────────┘
```

## 快速开始

### 1. 数据库初始化

```bash
cd backend
# 创建数据库表
psql -U postgres -d legal_assistant -f database/case_schema.sql
```

### 2. 启动后端服务

```bash
cd backend
# 安装依赖（首次）
pip install -r requirements.txt

# 启动服务
python src/app.py
```

后端服务将在 `http://localhost:5000` 启动

### 3. 启动PC端前端

```bash
cd legal-instructor-pc
# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev
```

PC端将在 `http://localhost:3000` 启动

### 4. 启动小程序端

```bash
# 使用微信开发者工具打开 frontend 目录
# 确保勾选"不校验合法域名"
```

## 业务流程测试

### 步骤1：PC端录入案例

1. 打开浏览器访问 `http://localhost:3000`
2. 填写案例信息：
   - **标题**：测试案例：张某盗窃案
   - **副标题**：盗窃罪数额认定标准
   - **关键词**：选择"判决"、"盗窃"，补充"数额认定"
   - **基本案情**：输入案件描述
   - **裁判要旨**：输入裁判规则
   - **裁判结果**：输入判决结果
   - **关联索引**：添加法条和历审程序
   - **争议焦点**：输入争议焦点
3. 点击"提交案例"

### 步骤2：验证数据存储

```bash
# 运行后端测试
cd backend
python tests/test_legal_instructor_api.py
```

### 步骤3：小程序端检索案例

1. 打开微信开发者工具
2. 进入"怎么判"页面
3. 切换到"判例检索"Tab
4. 输入关键词"盗窃"
5. 点击搜索
6. 查看检索结果

## API接口文档

### 创建案例（PC端调用）

**接口**：`POST /api/v1/legal_instructor/cases`

**请求体**：
```json
{
  "title": "测试案例",
  "subtitle": "案例副标题",
  "keywords": [
    {"type": "裁判类型", "value": "判决"},
    {"type": "案由", "value": "盗窃"}
  ],
  "basic_facts": "<p>基本案情HTML</p>",
  "judgment_essence": "<p>裁判要旨HTML</p>",
  "judgment_result": "<p>裁判结果HTML</p>",
  "dispute_foci": ["焦点1", "焦点2"],
  "related_index": {
    "laws": [
      {"law_name": "刑法", "article_numbers": "第1条"}
    ],
    "proceedings": [
      {
        "procedure_type": "一审",
        "court": "北京市朝阳区人民法院",
        "case_number": "...",
        "judgment_type": "判决",
        "judgment_date": "2024-01-01"
      }
    ]
  },
  "status": "published"
}
```

**响应**：
```json
{
  "success": true,
  "message": "案例创建成功",
  "data": {
    "id": 1,
    "title": "测试案例",
    ...
  }
}
```

### 搜索案例（小程序调用）

**接口**：`POST /api/v1/legal_instructor/cases/search`

**请求体**：
```json
{
  "keywords": "盗窃",
  "filters": {
    "case_type": "盗窃"
  }
}
```

**响应**：
```json
{
  "success": true,
  "data": {
    "cases": [
      {
        "case_id": 1,
        "case_title": "测试案例：张某盗窃案",
        "case_number": "(2023)京0105刑初123号",
        "court": "北京市朝阳区人民法院",
        "judgment_type": "判决",
        "cause_of_action": "盗窃",
        "result": "判决结果摘要...",
        "judgment_essence": "裁判要旨..."
      }
    ],
    "total": 1
  }
}
```

## 技术栈

### PC端前端
- Vue 3
- Element Plus
- Axios
- Vite

### 后端
- Flask
- SQLAlchemy
- PostgreSQL

### 小程序
- 微信小程序原生开发
- wx.request API

## 注意事项

1. **开发环境配置**：
   - 小程序开发需要勾选"不校验合法域名"
   - 确保后端服务先启动

2. **生产环境配置**：
   - PC端和小程序需要配置真实的后端域名
   - 小程序需要在微信公众平台配置request合法域名

3. **数据库连接**：
   - 确保PostgreSQL已安装并运行
   - 检查 `.env` 文件中的数据库配置

## 故障排查

### 问题1：PC端无法连接后端
- 检查后端服务是否启动：`http://localhost:5000/health`
- 检查 `legal-instructor-pc/vite.config.js` 中的代理配置

### 问题2：小程序无法获取数据
- 确保勾选"不校验合法域名"
- 检查 `frontend/pages/how_to_judge/how_to_judge.js` 中的API地址

### 问题3：数据库连接失败
- 检查 PostgreSQL 是否运行
- 检查 `.env` 文件中的数据库配置
- 执行数据库初始化脚本

## 后续优化

- [ ] 添加案例编辑功能
- [ ] 添加草稿自动保存
- [ ] 添加案例导出功能（Word/PDF）
- [ ] 添加图片上传功能
- [ ] 添加批量导入功能
- [ ] 添加数据统计和可视化
