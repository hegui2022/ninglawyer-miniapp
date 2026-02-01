# 法律教官系统 - 快速启动指南

## 🚀 一键启动测试

### 1. 启动后端服务

```bash
cd backend
python src/app.py
```

后端将在 `http://localhost:5000` 启动

### 2. 启动PC端前端

```bash
cd legal-instructor-pc
npm install  # 首次运行需要安装依赖
npm run dev
```

PC端将在 `http://localhost:5173` 启动

### 3. 打开小程序

使用微信开发者工具打开 `frontend` 目录，确保勾选"不校验合法域名"

## 📊 业务流程测试

### 步骤1：PC端录入案例

1. 浏览器访问 `http://localhost:5173`
2. 填写案例信息（所有字段都有默认值和提示）
3. 点击"提交案例"

### 步骤2：小程序检索案例

1. 打开微信开发者工具
2. 进入"怎么判" → "判例检索"
3. 输入关键词搜索
4. 查看PC端录入的案例

## ✅ 测试结果

所有API测试通过：
- ✓ 创建案例成功
- ✓ 获取案例列表成功
- ✓ 搜索案例成功

## 📁 项目结构

```
.
├── backend/                           # 后端服务
│   ├── src/
│   │   ├── api/
│   │   │   └── v1_legal_instructor.py # 法律教官API
│   │   ├── models/
│   │   │   └── case_model.py          # 案例数据模型
│   │   └── app.py                     # 主应用（已注册法律教官蓝图）
│   ├── database/
│   │   └── case_schema.sql            # 数据库表结构
│   └── tests/
│       └── test_legal_instructor_api.py # API测试脚本
├── legal-instructor-pc/              # PC端前端
│   ├── src/
│   │   ├── views/
│   │   │   └── CaseInput.vue          # 案例录入页面
│   │   ├── components/
│   │   │   └── RichTextEditor.vue     # 富文本编辑器
│   │   ├── api/
│   │   │   └── case.js                # API调用
│   │   ├── router/
│   │   │   └── index.js               # 路由配置
│   │   └── main.js                    # 入口文件
│   ├── package.json
│   └── vite.config.js
└── frontend/                          # 小程序端
    └── pages/
        └── how_to_judge/
            └── how_to_judge.js         # 已修改为调用法律教官API
```

## 🔧 API接口

### 创建案例
- **URL**: `POST /api/v1/legal_instructor/cases`
- **调用方**: PC端前端

### 搜索案例
- **URL**: `POST /api/v1/legal_instructor/cases/search`
- **调用方**: 小程序怎么判

### 获取案例列表
- **URL**: `GET /api/v1/legal_instructor/cases`
- **调用方**: 小程序

### 获取案例详情
- **URL**: `GET /api/v1/legal_instructor/cases/{id}`
- **调用方**: 小程序

## ⚠️ 注意事项

1. **数据库**: 当前使用 SQLite（自动创建），无需额外配置
2. **跨域**: 后端已配置 CORS，支持前端跨域调用
3. **开发环境**: 小程序需要勾选"不校验合法域名"
4. **依赖安装**: PC端首次运行需要 `npm install`

## 🎯 下一步优化

- [ ] 添加案例编辑功能
- [ ] 添加草稿自动保存
- [ ] 添加图片上传功能
- [ ] 添加数据统计和可视化
- [ ] 优化富文本编辑器功能
