# 宁律师小程序矩阵 - 部署文档

## 📚 部署指南

本文档提供宁律师小程序矩阵的完整部署指南，包括小程序发布和后端服务部署。

---

## 🏗️ 项目架构

```
ninglawyer-miniapp/
├── 法律教官/          # AI 法律咨询小程序
├── 码上签约/          # 合同起草与审查小程序
├── 理约/             # 合同履约管理小程序
├── 怎么判/           # 法律维权小程序
├── 防风险/           # 法律风险检测小程序
├── common/           # 公共代码和工具
├── components/       # 通用组件
├── server/          # 后端服务
├── docs/            # 文档
├── scripts/         # 脚本
└── tools/           # 开发工具
```

---

## 🚀 快速开始

### 前置要求

1. **微信开发者工具**
   - 下载：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
   - 版本：1.06.2307260 或更高

2. **Node.js 环境**
   - 版本：16.x 或更高
   - 安装：https://nodejs.org/

3. **Python 环境**
   - 版本：3.8 或更高
   - 安装：https://www.python.org/

4. **数据库**
   - PostgreSQL 13 或更高
   - Redis 6 或更高

5. **微信小程序账号**
   - 已注册的小程序 AppID
   - 小程序密钥（AppSecret）

---

## 📦 小程序部署

### 1. 法律教官小程序部署

#### 1.1 配置小程序

1. **配置 AppID**
   ```javascript
   // legal-mentor/app.js
   App({
     onLaunch() {
       // 配置小程序 AppID
       const appId = 'your_appid_here';
       wx.setStorageSync('appId', appId);
       
       // 配置后端 API 地址
       const apiBaseUrl = 'https://your-server.com/api';
       wx.setStorageSync('apiBaseUrl', apiBaseUrl);
     }
   });
   ```

2. **配置服务器域名**
   - 登录微信公众平台：https://mp.weixin.qq.com/
   - 进入"开发" > "开发管理" > "开发设置"
   - 配置"服务器域名"：
     ```
     request合法域名: https://your-server.com
     uploadFile合法域名: https://your-server.com
     downloadFile合法域名: https://your-server.com
     ```

3. **配置跳转小程序**
   - 进入"设置" > "第三方设置" > "关联小程序"
   - 关联其他小程序（码上签约、理约、怎么判、防风险）

#### 1.2 上传代码

1. 打开微信开发者工具
2. 导入项目：`legal-mentor/`
3. 点击"上传"按钮
4. 填写版本号和项目备注
5. 点击"确定"上传

#### 1.3 提交审核

1. 登录微信公众平台
2. 进入"版本管理"
3. 选择刚才上传的版本
4. 点击"提交审核"
5. 填写审核信息：
   - 功能描述：AI 智能法律咨询，提供专业的法律建议
   - 测试账号：（可选）
6. 等待审核通过

#### 1.4 发布上线

1. 审核通过后，点击"发布"
2. 确认发布信息
3. 小程序正式上线

---

### 2. 码上签约小程序部署

部署流程与法律教官相同，重复上述步骤：

1. 配置 AppID
2. 配置服务器域名
3. 配置跳转小程序
4. 上传代码
5. 提交审核
6. 发布上线

---

### 3. 理约小程序部署

部署流程与法律教官相同，重复上述步骤：

1. 配置 AppID
2. 配置服务器域名
3. 配置跳转小程序
4. 上传代码
5. 提交审核
6. 发布上线

---

### 4. 怎么判小程序部署

部署流程与法律教官相同，重复上述步骤：

1. 配置 AppID
2. 配置服务器域名
3. 配置跳转小程序
4. 上传代码
5. 提交审核
6. 发布上线

---

### 5. 防风险小程序部署

部署流程与法律教官相同，重复上述步骤：

1. 配置 AppID
2. 配置服务器域名
3. 配置跳转小程序
4. 上传代码
5. 提交审核
6. 发布上线

---

## 🖥️ 后端服务部署

### 1. 环境准备

#### 1.1 安装依赖

```bash
# 进入后端目录
cd ninglawyer-miniapp/server

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装 Python 依赖
pip install -r requirements.txt
```

#### 1.2 配置数据库

```bash
# 创建 PostgreSQL 数据库
createdb ninglawyer

# 运行数据库迁移
python manage.py migrate
```

#### 1.3 配置环境变量

创建 `.env` 文件：

```env
# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False

# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ninglawyer
DB_USER=ninglawyer
DB_PASSWORD=your_password

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# 微信小程序配置
WECHAT_APP_ID=your_appid
WECHAT_APP_SECRET=your_secret

# 大模型配置
LLM_API_KEY=your_llm_api_key
LLM_API_BASE=https://api.llm.com
LLM_MODEL=doubao-seed-1-6-251015

# 文件存储配置
OSS_ACCESS_KEY=your_access_key
OSS_SECRET_KEY=your_secret_key
OSS_BUCKET=your_bucket
OSS_ENDPOINT=your_endpoint

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=/var/log/ninglawyer
```

---

### 2. 启动服务

#### 2.1 启动主服务

```bash
# 开发模式
python manage.py runserver

# 生产模式
gunicorn -w 4 -b 0.0.0.0:8000 manage:app
```

#### 2.2 启动 Celery Worker

```bash
celery -A tasks worker --loglevel=info
```

#### 2.3 启动 Celery Beat

```bash
celery -A tasks beat --loglevel=info
```

---

### 3. 使用 Systemd 管理服务

创建服务文件：

#### 3.1 主服务

```ini
# /etc/systemd/system/ninglawyer.service
[Unit]
Description=NingLawyer Server
After=network.target

[Service]
Type=notify
User=ninglawyer
Group=ninglawyer
WorkingDirectory=/var/www/ninglawyer
Environment="PATH=/var/www/ninglawyer/venv/bin"
ExecStart=/var/www/ninglawyer/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 manage:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 3.2 Celery Worker

```ini
# /etc/systemd/system/ninglawyer-worker.service
[Unit]
Description=NingLawyer Celery Worker
After=network.target

[Service]
Type=forking
User=ninglawyer
Group=ninglawyer
WorkingDirectory=/var/www/ninglawyer
Environment="PATH=/var/www/ninglawyer/venv/bin"
ExecStart=/var/www/ninglawyer/venv/bin/celery -A tasks worker --loglevel=info --pidfile=/var/run/ninglawyer-worker.pid
ExecStop=/bin/kill -TERM $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 3.3 Celery Beat

```ini
# /etc/systemd/system/ninglawyer-beat.service
[Unit]
Description=NingLawyer Celery Beat
After=network.target

[Service]
Type=forking
User=ninglawyer
Group=ninglawyer
WorkingDirectory=/var/www/ninglawyer
Environment="PATH=/var/www/ninglawyer/venv/bin"
ExecStart=/var/www/ninglawyer/venv/bin/celery -A tasks beat --loglevel=info --pidfile=/var/run/ninglawyer-beat.pid
ExecStop=/bin/kill -TERM $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
# 重载配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ninglawyer
sudo systemctl start ninglawyer-worker
sudo systemctl start ninglawyer-beat

# 设置开机自启
sudo systemctl enable ninglawyer
sudo systemctl enable ninglawyer-worker
sudo systemctl enable ninglawyer-beat
```

---

### 4. 使用 Nginx 反向代理

#### 4.1 配置 Nginx

```nginx
# /etc/nginx/sites-available/ninglawyer
server {
    listen 80;
    server_name your-server.com;

    # SSL 配置
    # listen 443 ssl;
    # ssl_certificate /path/to/cert.pem;
    # ssl_certificate_key /path/to/key.pem;

    # 客户端上传文件大小限制
    client_max_body_size 100M;

    # 代理到后端服务
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket 支持
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 静态文件
    location /static {
        alias /var/www/ninglawyer/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 日志
    access_log /var/log/nginx/ninglawyer_access.log;
    error_log /var/log/nginx/ninglawyer_error.log;
}
```

#### 4.2 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/ninglawyer /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

---

## 🔒 安全配置

### 1. SSL 证书

使用 Let's Encrypt 免费证书：

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-server.com

# 自动续期
sudo certbot renew --dry-run
```

### 2. 防火墙配置

```bash
# 配置 UFW 防火墙
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### 3. 数据库安全

```sql
-- 创建只读用户
CREATE USER ninglawyer_read WITH PASSWORD 'read_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ninglawyer_read;

-- 创建备份用户
CREATE USER ninglawyer_backup WITH PASSWORD 'backup_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ninglawyer_backup;
```

---

## 📊 监控与日志

### 1. 应用监控

使用 Prometheus + Grafana：

```python
# 安装依赖
pip install prometheus_client

# 添加监控端点
from prometheus_client import Counter, Histogram

# 定义指标
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

# 使用指标
@app.route('/api/...')
def api_handler():
    request_count.inc()
    with request_duration.time():
        # 处理请求
        pass
```

### 2. 日志管理

使用 Logrotate：

```bash
# /etc/logrotate.d/ninglawyer
/var/log/ninglawyer/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 ninglawyer ninglawyer
    sharedscripts
    postrotate
        systemctl reload ninglawyer > /dev/null 2>&1 || true
    endscript
}
```

---

## 🔄 更新部署

### 1. 小程序更新

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 打开微信开发者工具
# 3. 导入项目
# 4. 上传代码
# 5. 提交审核
# 6. 发布上线
```

### 2. 后端服务更新

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行数据库迁移
python manage.py migrate

# 4. 重启服务
sudo systemctl restart ninglawyer
sudo systemctl restart ninglawyer-worker
sudo systemctl restart ninglawyer-beat
```

---

## 🧪 部署验证

### 1. 小程序验证

- [ ] 所有小程序可以正常打开
- [ ] AI 聊天功能正常
- [ ] 小程序跳转功能正常
- [ ] 数据交互功能正常

### 2. 后端服务验证

```bash
# 检查服务状态
sudo systemctl status ninglawyer
sudo systemctl status ninglawyer-worker
sudo systemctl status ninglawyer-beat

# 检查服务日志
sudo journalctl -u ninglawyer -f
sudo journalctl -u ninglawyer-worker -f
sudo journalctl -u ninglawyer-beat -f

# 测试 API
curl https://your-server.com/api/health
```

---

## 📞 故障排查

### 1. 小程序无法访问后端

**检查项**：
- [ ] 服务器域名是否正确配置
- [ ] SSL 证书是否有效
- [ ] 防火墙是否开放
- [ ] 后端服务是否正常运行

**解决方案**：
```bash
# 检查服务状态
sudo systemctl status ninglawyer

# 查看服务日志
sudo journalctl -u ninglawyer -n 100

# 检查端口监听
sudo netstat -tlnp | grep 8000
```

### 2. 数据库连接失败

**检查项**：
- [ ] 数据库是否正常运行
- [ ] 数据库配置是否正确
- [ ] 网络是否可达

**解决方案**：
```bash
# 检查数据库状态
sudo systemctl status postgresql

# 测试数据库连接
psql -h localhost -U ninglawyer -d ninglawyer

# 查看数据库日志
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### 3. Redis 连接失败

**检查项**：
- [ ] Redis 是否正常运行
- [ ] Redis 配置是否正确
- [ ] 网络是否可达

**解决方案**：
```bash
# 检查 Redis 状态
sudo systemctl status redis

# 测试 Redis 连接
redis-cli ping

# 查看 Redis 日志
sudo tail -f /var/log/redis/redis-server.log
```

---

## 📚 相关文档

- [开发文档](./DEVELOPMENT.md)
- [API 文档](./API.md)
- [测试用例](./TEST_CASES.md)
- [用户手册](./USER_MANUAL.md)

---

## 🤝 技术支持

如有问题，请联系：

- 邮箱：support@ninglawyer.com
- 微信：ninglawyer_support
- GitHub Issues：https://github.com/ninglawyer/miniapp-matrix/issues

---

**部署文档版本**：v1.0.0
**最后更新**：2024年
