# 宁律师小程序部署指南

## 本地运行（开发阶段）

### 前置条件
- Python 3.7+
- 微信开发者工具
- 后端服务已启动

### 步骤

1. **启动后端服务**
```bash
cd /workspace/projects
python scripts/chat_server.py
```

2. **配置小程序**
打开 `miniprogram/app.js`，确保 `baseUrl` 是开发环境地址：
```javascript
globalData: {
  baseUrl: 'http://localhost:8000',
}
```

3. **配置微信开发者工具**
- 打开微信开发者工具
- 导入 `miniprogram` 项目
- 在"详情" -> "本地设置"中勾选"不校验合法域名"

4. **运行**
点击"编译"按钮即可在模拟器中查看效果

---

## 生产部署

### 方案一：使用云服务器（推荐）

#### 1. 准备云服务器

推荐使用：
- 腾讯云
- 阿里云
- 华为云

配置要求：
- CPU: 2核
- 内存: 4GB
- 带宽: 5Mbps
- 操作系统: Ubuntu 20.04 LTS / CentOS 7+

#### 2. 配置服务器

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和依赖
sudo apt install python3 python3-pip git nginx -y

# 克隆项目（或上传代码）
git clone <your-repo-url> /opt/ninglawyer
cd /opt/ninglawyer

# 安装 Python 依赖
pip3 install -r requirements.txt

# 安装依赖（如果需要）
pip3 install flask langchain langchain-openai
```

#### 3. 配置 Nginx

创建 Nginx 配置文件：
```bash
sudo nano /etc/nginx/sites-available/ninglawyer
```

添加以下内容：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/ninglawyer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. 使用 systemd 管理服务

创建服务文件：
```bash
sudo nano /etc/systemd/system/ninglawyer.service
```

添加以下内容：
```ini
[Unit]
Description=Ning Lawyer Chat Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ninglawyer
ExecStart=/usr/bin/python3 /opt/ninglawyer/scripts/chat_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable ninglawyer
sudo systemctl start ninglawyer
```

#### 5. 配置 HTTPS（必需）

使用 Let's Encrypt 免费证书：
```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

#### 6. 配置小程序

修改 `miniprogram/app.js`：
```javascript
globalData: {
  baseUrl: 'https://your-domain.com',
}
```

#### 7. 配置微信小程序后台

1. 登录微信公众平台：https://mp.weixin.qq.com/
2. 进入"开发" -> "开发管理" -> "开发设置"
3. 配置服务器域名：
   - request: `https://your-domain.com`
   - uploadFile: `https://your-domain.com`
   - downloadFile: `https://your-domain.com`

#### 8. 发布小程序

1. 在微信开发者工具中上传代码
2. 登录微信公众平台
3. 进入"版本管理"
4. 提交审核
5. 审核通过后发布

---

### 方案二：使用云函数（Serverless）

#### 1. 腾讯云函数

1. 登录腾讯云控制台
2. 创建云函数
3. 上传代码（修改为云函数入口格式）
4. 配置触发器（API 网关）
5. 获取 API 网关地址

#### 2. 阿里云函数计算

步骤类似腾讯云函数。

---

### 方案三：使用云开发

#### 1. 微信云开发

1. 开通微信云开发
2. 创建云函数
3. 部署后端代码
4. 配置环境变量

优点：
- 与小程序无缝集成
- 免费额度
- 自动 HTTPS

---

## 环境变量配置

### 后端服务需要的环境变量

```bash
# Flask 配置
FLASK_APP=scripts/chat_server.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# 对象存储配置（如果需要）
COZE_BUCKET_ENDPOINT_URL=https://your-endpoint.com
COZE_BUCKET_NAME=your-bucket-name

# 模型配置（如果需要）
COZE_WORKLOAD_IDENTITY_API_KEY=your-api-key
COZE_INTEGRATION_MODEL_BASE_URL=https://your-model-endpoint.com
COZE_WORKSPACE_PATH=/opt/ninglawyer
```

---

## 性能优化

### 1. 后端优化

- 使用 Gunicorn + Gevent 提高并发
- 启用 Redis 缓存
- 使用 CDN 加速静态资源

### 2. 小程序优化

- 压缩代码和图片
- 开启分包加载
- 使用懒加载

---

## 监控和日志

### 1. 服务器监控

使用工具：
- htop
- iotop
- netstat
- nginx -t

### 2. 日志管理

```bash
# 查看日志
sudo journalctl -u ninglawyer -f

# 查看错误日志
tail -f /var/log/nginx/error.log
```

---

## 备份和恢复

### 1. 数据备份

```bash
# 备份代码
tar -czf ninglawyer-backup-$(date +%Y%m%d).tar.gz /opt/ninglawyer

# 备份数据库（如果使用数据库）
mysqldump -u root -p ninglawyer > backup.sql
```

### 2. 自动备份

创建 cron 任务：
```bash
sudo crontab -e
```

添加：
```bash
# 每天凌晨 3 点备份
0 3 * * * /opt/scripts/backup.sh
```

---

## 安全建议

1. **定期更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **配置防火墙**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

3. **修改默认端口**
   - SSH 端口改为非 22
   - 限制 SSH 登录

4. **定期备份**

5. **监控异常访问**

---

## 成本估算

### 云服务器方案

| 资源 | 配置 | 月费用 |
|------|------|--------|
| 服务器 | 2核4G | ¥50-100 |
| 带宽 | 5Mbps | ¥20-50 |
| 对象存储 | 10GB | 免费-¥10 |
| **合计** | | **¥70-160/月** |

### 云函数方案

按实际使用计费，通常更便宜。

---

## 常见问题

### Q1: 部署后小程序无法连接？

A: 检查以下几点：
1. 服务器是否正常运行
2. Nginx 配置是否正确
3. 域名 DNS 解析是否生效
4. 微信小程序后台是否配置了域名

### Q2: HTTPS 证书到期怎么办？

A: Let's Encrypt 证书会自动续期，如果没有：
```bash
sudo certbot renew
sudo systemctl reload nginx
```

### Q3: 如何扩容？

A: 
- 垂直扩容：升级服务器配置
- 水平扩容：使用负载均衡 + 多台服务器
- 使用云函数自动扩容

---

## 联系支持

- 部署问题：support@ninglawyer.com
- 技术文档：https://docs.ninglawyer.com
