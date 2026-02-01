# 端口变更说明

## ✅ 已修改配置

PC端前端端口已从 **3000** 修改为 **8080**

## 📝 修改内容

1. **配置文件**: `legal-instructor-pc/vite.config.js`
   - 修改 `server.port` 从 `3000` 改为 `8080`

2. **文档更新**:
   - `QUICK_START.md`
   - `LEGAL_INSTRUCTOR_README.md`

3. **新增文档**:
   - `legal-instructor-pc/PORT_CONFIG.md` (端口配置说明)

## 🚀 启动方式

### 启动后端
```bash
cd backend
python src/app.py
```

### 启动PC端
```bash
cd legal-instructor-pc
npm install  # 首次
npm run dev
```

访问地址：**http://localhost:8080**

## ⚠️ 如果8080也被占用

请参考 `legal-instructor-pc/PORT_CONFIG.md` 文档修改端口。

### 快速修改方法

编辑 `vite.config.js`，将 `port: 8080` 改为其他端口号：
```javascript
server: {
  port: 8081,  // 或 3001、5173 等
  ...
}
```

或者通过命令行指定：
```bash
npm run dev -- --port 8081
```

## 📋 端口占用检查

### Linux/Mac
```bash
lsof -i :8080
```

### Windows
```bash
netstat -ano | findstr :8080
```

如果端口被占用，会显示占用该端口的进程信息。
