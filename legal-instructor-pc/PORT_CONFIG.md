# 端口配置说明

## 当前配置

PC端前端默认运行在 **http://localhost:8080**

## 修改端口

如果 8080 端口也被占用，可以修改为其他端口：

### 方法1：修改配置文件

编辑 `vite.config.js` 文件：

```javascript
server: {
  port: 8081,  // 修改为你想要的端口号，如 8081、3001 等
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true
    }
  }
}
```

### 方法2：命令行指定

启动时通过命令行参数指定端口：

```bash
npm run dev -- --port 8081
```

## 常用端口建议

- 8080 (当前默认)
- 8081
- 3001
- 5173 (Vite默认端口)

## 注意事项

修改端口后，访问地址需要相应更新，例如：
- 原来：http://localhost:8080
- 改为：http://localhost:8081
