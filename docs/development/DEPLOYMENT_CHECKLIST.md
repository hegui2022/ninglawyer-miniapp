# 宁律师法律咨询小程序 - 部署检查清单

## 📋 部署前检查

### ✅ 服务器准备
- [ ] 服务器已购买（推荐：4核8G，40G SSD）
- [ ] 操作系统已安装（Ubuntu 22.04 LTS 或 CentOS 7+）
- [ ] Docker 已安装
- [ ] Docker Compose 已安装
- [ ] 防火墙已配置（开放 22, 80, 443 端口）

### ✅ 域名和 SSL
- [ ] 域名已购买（如：api.ninglawyer.com）
- [ ] DNS 已解析到服务器 IP
- [ ] SSL 证书已获取（Let's Encrypt 或已有证书）

### ✅ 代码和配置
- [ ] 代码已克隆到服务器
- [ ] `.env` 文件已创建并配置
- [ ] SSL 证书已放到 `nginx/ssl` 目录
- [ ] Nginx 配置文件已修改（替换域名）

### ✅ 第三方服务
- [ ] 豆包大模型 API Key 已获取并配置
- [ ] S3 对象存储已配置（可选）
- [ ] 微信小程序 AppID 和 Secret 已配置

---

## 🚀 部署步骤

### 第一步：准备服务器
```bash
# 安装 Docker
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 第二步：克隆代码
```bash
git clone https://github.com/hegui2022/ninglawyer-miniapp.git
cd ninglawyer-miniapp
```

### 第三步：配置环境
```bash
# 创建环境配置文件
cp .env.production.example .env

# 编辑配置文件
vi .env

# 必须配置的项：
# - DB_PASSWORD: 数据库密码
# - JWT_SECRET_KEY: JWT 密钥
# - DOUBAO_API_KEY: 豆包大模型 API Key（必须）
```

### 第四步：配置 SSL 证书
```bash
# 创建 SSL 证书目录
mkdir -p nginx/ssl

# 方式一：使用 Let's Encrypt（免费）
sudo apt-get install certbot
sudo certbot certonly --standalone -d api.ninglawyer.com
sudo cp /etc/letsencrypt/live/api.ninglawyer.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/api.ninglawyer.com/privkey.pem nginx/ssl/key.pem

# 方式二：使用已有证书
# 将证书文件放到 nginx/ssl 目录
# cert.pem (证书文件)
# key.pem (私钥文件)
```

### 第五步：配置 Nginx
```bash
# 编辑 Nginx 配置文件
vi nginx/nginx.conf

# 修改以下配置：
# server_name: 替换为你的域名
# ssl_certificate: 证书路径
# ssl_certificate_key: 私钥路径
```

### 第六步：部署服务
```bash
# 赋予执行权限
chmod +x scripts/deploy-prod.sh

# 执行部署脚本
./scripts/deploy-prod.sh

# 或手动部署
docker-compose up -d
```

---

## 🔍 部署后验证

### ✅ 服务状态检查
```bash
# 检查所有服务状态
docker-compose ps

# 应该看到以下服务都运行正常：
# - postgres
# - redis
# - milvus-standalone
# - backend
# - nginx
```

### ✅ 健康检查
```bash
# 检查后端 API
curl http://localhost:5000/health

# 预期返回：
# {"status":"ok","service":"ninglawyer-miniapp","version":"1.0.0-alpha"}

# 检查数据库
docker-compose exec postgres pg_isready -U postgres

# 预期返回：
# postgres: ready

# 检查 Redis
docker-compose exec redis redis-cli ping

# 预期返回：
# PONG
```

### ✅ 网络检查
```bash
# 检查端口监听
sudo netstat -tulpn | grep -E ':(80|443|5000)'

# 应该看到：
# tcp  0.0.0.0:80   LISTEN  ...
# tcp  0.0.0.0:443  LISTEN  ...
# tcp  127.0.0.1:5000  LISTEN  ...
```

### ✅ 外网访问检查
```bash
# 检查 HTTPS 访问
curl -I https://api.ninglawyer.com

# 应该看到：
# HTTP/1.1 200 OK 或 HTTP/1.1 301 Moved Permanently
```

---

## 📱 前端配置

### ✅ 修改前端配置
```javascript
// legal-instructor/utils/config.js
const CONFIG = {
  production: {
    apiUrl: 'https://api.ninglawyer.com/api',  // 替换为你的域名
    baseUrl: 'https://api.ninglawyer.com'
  }
};
```

### ✅ 配置微信小程序服务器域名
1. 登录微信公众平台：https://mp.weixin.qq.com/
2. 进入"开发" -> "开发设置"
3. 配置服务器域名：
   - request 合法域名：`https://api.ninglawyer.com`
   - uploadFile 合法域名：`https://api.ninglawyer.com`
   - downloadFile 合法域名：`https://api.ninglawyer.com`

---

## 🧪 功能测试

### ✅ 咨询功能测试
1. 打开微信开发者工具
2. 导入 `legal-instructor` 项目
3. 点击"编译"
4. 进入咨询页面
5. 输入问题，测试咨询功能

### ✅ 其他功能测试
- [ ] 合同创建和签署
- [ ] 履约管理
- [ ] 风险扫描
- [ ] 判例查询
- [ ] 用户登录

---

## 📊 监控和维护

### ✅ 日志监控
```bash
# 查看后端日志
docker-compose logs -f backend

# 查看数据库日志
docker-compose logs -f postgres

# 查看 Nginx 日志
tail -f nginx/logs/access.log
tail -f nginx/logs/error.log
```

### ✅ 数据备份
```bash
# 创建备份脚本
vi scripts/backup.sh

# 添加定时任务
crontab -e

# 每天凌晨 2 点备份数据库
0 2 * * * /path/to/ninglawyer-miniapp/scripts/backup.sh
```

### ✅ 服务更新
```bash
# 拉取最新代码
git pull origin main

# 重新构建镜像
docker-compose build backend

# 重启服务
docker-compose up -d backend
```

---

## 🆘 常见问题排查

### ❌ 服务无法启动
```bash
# 查看详细日志
docker-compose logs backend

# 检查端口占用
sudo netstat -tulpn | grep -E ':(80|443|5000|5432|6379|19530)'

# 检查配置文件
docker-compose config
```

### ❌ 数据库连接失败
```bash
# 检查数据库状态
docker-compose exec postgres pg_isready -U postgres

# 检查数据库密码
docker-compose exec postgres psql -U postgres -c "SELECT version();"
```

### ❌ SSL 证书错误
```bash
# 检查证书文件
ls -l nginx/ssl/

# 检查证书有效期
openssl x509 -in nginx/ssl/cert.pem -noout -dates

# 检查 Nginx 配置
docker-compose exec nginx nginx -t
```

### ❌ API 调用失败
```bash
# 检查后端日志
docker-compose logs -f backend

# 检查 API Key 配置
grep DOUBAO_API_KEY .env

# 测试 API 连接
curl http://localhost:5000/api/consultation/test
```

---

## 📞 技术支持

如果遇到问题，请：

1. 查看日志：`docker-compose logs -f`
2. 检查配置：`.env` 和 `nginx/nginx.conf`
3. 查看文档：`DEPLOYMENT_GUIDE.md`

---

## ✅ 部署完成

恭喜！如果以上所有检查项都通过，说明部署成功！

**下一步**：
1. 配置定时备份
2. 配置监控告警
3. 开始使用！

---

**祝您使用愉快！** 🎉
