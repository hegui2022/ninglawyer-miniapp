# API Token安全配置指南

## 🔒 安全原则

**绝对不要将API Token硬编码在代码或配置文件中！**

## ✅ 正确的做法

### 1. 使用环境变量

API Token应该存储在环境变量中，通过`.env`文件管理。

### 2. 配置步骤

#### 步骤1：复制示例文件

```bash
cp .env.example .env
```

#### 步骤2：编辑.env文件

```bash
nano .env
# 或使用其他编辑器
```

#### 步骤3：填入真实的API Token

```env
# 脱敏Bot Token
COZE_DESENSITIZE_BOT_TOKEN=pat_你的真实Token
```

#### 步骤4：.env文件不会被提交到git

`.gitignore`已配置忽略`.env`文件，确保Token安全。

## 📝 配置文件说明

### config/coze_bots.json

此文件只存储Bot的元数据，不存储敏感信息：

```json
{
  "desensitize": {
    "name": "宁律师脱敏助手",
    "bot_id": "7600730158433550363",
    "api_url": "https://api.coze.cn/v3/chat",
    "api_token_env": "COZE_DESENSITIZE_BOT_TOKEN"  // 环境变量名，不是Token本身
  }
}
```

### .env文件

此文件存储真实的API Token（不会被提交到git）：

```env
COZE_DESENSITIZE_BOT_TOKEN=pat_真实的Token
```

## 🛡️ 安全最佳实践

1. ✅ 使用环境变量存储敏感信息
2. ✅ .env文件加入.gitignore
3. ✅ 提供.env.example作为示例
4. ✅ 不同环境使用不同的Token（开发/测试/生产）
5. ❌ 不要将Token提交到git
6. ❌ 不要在代码中硬编码Token
7. ❌ 不要在公开场合分享Token

## 🚀 部署时如何配置

### Docker部署

```bash
# 方式1：使用环境变量文件
docker run -e COZE_DESENSITIZE_BOT_TOKEN=pat_xxx ...

# 方式2：使用.env文件
docker run --env-file .env ...
```

### 云服务器部署

```bash
# 在服务器上设置环境变量
export COZE_DESENSITIZE_BOT_TOKEN=pat_xxx

# 或添加到 ~/.bashrc
echo 'export COZE_DESENSITIZE_BOT_TOKEN=pat_xxx' >> ~/.bashrc
```

## 📋 Token获取方式

1. 登录扣子平台
2. 进入Bot的API设置页面
3. 点击"管理API Token"或"生成Token"
4. 复制生成的Token（以`pat_`开头）
5. 粘贴到.env文件中

## 🔍 验证配置

运行以下命令验证Token是否正确：

```bash
python tests/test_desensitize_bot.py
```

如果看到"✅ 脱敏Bot测试成功！"，说明配置正确。

## ⚠️ 如果Token泄露怎么办？

1. 立即到扣子平台删除旧Token
2. 生成新的Token
3. 更新.env文件
4. 重启应用

## 📞 问题反馈

如果遇到配置问题，请检查：
1. .env文件是否存在
2. 环境变量名是否正确
3. Token格式是否正确（应该以`pat_`开头）
4. Token是否有效（可以在扣子平台验证）
