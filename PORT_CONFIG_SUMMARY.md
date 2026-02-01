# 端口配置变更总结

## ✅ 已完成修改

### 1. 配置文件修改
- ✅ `legal-instructor-pc/vite.config.js`
  - 端口从 `3000` 改为 `8080`

### 2. 文档更新
- ✅ `QUICK_START.md` - 更新所有端口引用
- ✅ `LEGAL_INSTRUCTOR_README.md` - 更新所有端口引用
- ✅ `PORT_CHANGE.md` - 新增端口变更说明
- ✅ `legal-instructor-pc/PORT_CONFIG.md` - 新增端口配置说明

### 3. 启动脚本增强
- ✅ `legal-instructor-pc/package.json`
  - `dev`: 默认使用 8080
  - `dev:3001`: 使用 3001 端口
  - `dev:5173`: 使用 5173 端口

## 🚀 使用方式

### 方式1：默认启动（8080端口）
```bash
cd legal-instructor-pc
npm run dev
```
访问：http://localhost:8080

### 方式2：使用其他端口
```bash
# 使用3001端口
npm run dev:3001

# 使用5173端口（Vite默认）
npm run dev:5173

# 或直接指定任意端口
npm run dev -- --port 8888
```

### 方式3：修改配置文件
编辑 `vite.config.js`，修改 `server.port` 的值

## 📝 端口配置说明

| 端口 | 用途 | 命令 |
|------|------|------|
| 5000 | 后端服务 | `python src/app.py` |
| 8080 | PC端前端（默认） | `npm run dev` |
| 3001 | PC端前端（备选） | `npm run dev:3001` |
| 5173 | PC端前端（备选） | `npm run dev:5173` |

## ⚠️ 注意事项

1. 确保8080端口未被占用
2. 如端口冲突，使用其他可用端口
3. 修改端口后，访问地址需相应更新
4. 后端服务必须在5000端口运行

## 📋 快速启动流程

```bash
# 终端1：启动后端
cd backend
python src/app.py

# 终端2：启动PC端
cd legal-instructor-pc
npm install  # 首次需要
npm run dev
```

然后访问：**http://localhost:8080**
