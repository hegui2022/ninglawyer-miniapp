# 扣子SKILL环境变量配置说明

本文档说明了调用扣子SKILL技能需要配置的环境变量。

## 环境变量列表

### 1. SKILL API基础配置

| 环境变量名 | 说明 | 示例值 | 必填 |
|-----------|------|--------|------|
| `COZE_SKILL_API_BASE_URL` | SKILL API的基础URL | `https://api.coze.com/v1` | 是 |
| `COZE_SKILL_API_KEY` | 调用SKILL的认证密钥 | `pat_xxxxxxxxxxxxxxxx` | 是 |
| `COZE_SKILL_TIMEOUT` | API调用超时时间（秒） | `300` | 否 |

### 2. SKILL ID配置

| 环境变量名 | 说明 | 对应SKILL功能 | 必填 |
|-----------|------|-------------|------|
| `COZE_SKILL_CIVIL_ID` | 民事咨询SKILL ID | 民事法律咨询 | 是 |
| `COZE_SKILL_CRIMINAL_ID` | 刑事咨询SKILL ID | 刑事法律咨询 | 是 |
| `COZE_SKILL_COMPANY_ID` | 公司法务SKILL ID | 公司法律事务 | 是 |
| `COZE_SKILL_LABOR_ID` | 劳动纠纷SKILL ID | 劳动法律咨询 | 是 |
| `COZE_SKILL_MARRIAGE_ID` | 婚姻家庭SKILL ID | 婚姻家庭法律 | 是 |
| `COZE_SKILL_IP_ID` | 知识产权SKILL ID | 知识产权保护 | 是 |
| `COZE_SKILL_CONTRACT_DRAFT_ID` | 合同起草SKILL ID | 合同起草功能 | 是 |
| `COZE_SKILL_CONTRACT_REVIEW_ID` | 合同审查SKILL ID | 合同审查功能 | 是 |
| `COZE_SKILL_DESENSITIZE_ID` | 信息脱敏SKILL ID | 信息脱敏功能 | 是 |

## 配置步骤

### 1. 获取SKILL信息

1. 登录扣子平台
2. 进入"技能商店"或"我的技能"
3. 查看您开发的每个SKILL
4. 记录每个SKILL的ID（通常在SKILL详情页可以看到）

### 2. 获取API Key

1. 登录扣子平台
2. 进入"个人中心" → "API Key"
3. 创建或复制API Key

### 3. 配置环境变量

在部署环境中添加以下环境变量：

```bash
# SKILL API配置
COZE_SKILL_API_BASE_URL=https://api.coze.com/v1
COZE_SKILL_API_KEY=你的SKILL_API_KEY

# SKILL ID列表
COZE_SKILL_CIVIL_ID=你的民事咨询SKILL_ID
COZE_SKILL_CRIMINAL_ID=你的刑事咨询SKILL_ID
COZE_SKILL_COMPANY_ID=你的公司法务SKILL_ID
COZE_SKILL_LABOR_ID=你的劳动纠纷SKILL_ID
COZE_SKILL_MARRIAGE_ID=你的婚姻家庭SKILL_ID
COZE_SKILL_IP_ID=你的知识产权SKILL_ID
COZE_SKILL_CONTRACT_DRAFT_ID=你的合同起草SKILL_ID
COZE_SKILL_CONTRACT_REVIEW_ID=你的合同审查SKILL_ID
COZE_SKILL_DESENSITIZE_ID=你的信息脱敏SKILL_ID

# API超时（可选）
COZE_SKILL_TIMEOUT=300
```

### 4. 在不同平台配置环境变量

#### 本地开发

编辑 `backend/.env` 文件：

```env
COZE_SKILL_API_BASE_URL=https://api.coze.com/v1
COZE_SKILL_API_KEY=你的SKILL_API_KEY
COZE_SKILL_CIVIL_ID=你的民事咨询SKILL_ID
# ... 其他SKILL ID
```

#### Docker部署

在 `docker-compose.yml` 中配置：

```yaml
services:
  backend:
    environment:
      - COZE_SKILL_API_BASE_URL=https://api.coze.com/v1
      - COZE_SKILL_API_KEY=${COZE_SKILL_API_KEY}
      - COZE_SKILL_CIVIL_ID=${COZE_SKILL_CIVIL_ID}
      # ... 其他SKILL ID
```

#### 云平台部署

在云平台的"环境变量"配置页面中添加上述变量。

## 安全提示

⚠️ **重要安全注意事项**：

1. **不要在代码中硬编码API Key**
   - ❌ 错误：`api_key = "pat_xxxxxxxxxxxxxxxx"`
   - ✅ 正确：`api_key = os.getenv('COZE_SKILL_API_KEY')`

2. **不要将.env文件提交到版本控制**
   - .env文件应该在.gitignore中
   - 只提交.env.example文件

3. **定期更换API Key**
   - 建议每3-6个月更换一次
   - 如果API Key泄露，立即更换

4. **使用强密钥**
   - 不要使用简单的密码
   - API Key应该足够长且复杂

5. **限制API Key权限**
   - 只授予必要的权限
   - 不要使用管理员密钥

## 验证配置

配置完成后，可以运行以下命令验证：

```bash
cd backend
python scripts/test_skill.py
```

（此脚本会在后续创建）

## 常见问题

### 1. 找不到SKILL ID？

**解决方案**：
- 登录扣子平台
- 进入"我的技能"
- 点击SKILL名称进入详情页
- SKILL ID通常在详情页顶部或设置中

### 2. API Key无效？

**解决方案**：
- 确认API Key是否正确复制（包括pat_前缀）
- 确认API Key是否已启用
- 确认API Key是否有调用SKILL的权限

### 3. 调用失败？

**解决方案**：
- 检查COZE_SKILL_API_BASE_URL是否正确
- 检查SKILL ID是否正确
- 检查网络连接
- 查看日志文件获取详细错误信息

## 相关文档

- [扣子平台API文档](https://www.coze.com/docs)
- [环境变量配置最佳实践](./ENV_SECURITY.md)
- [SKILL调用示例](./SKILL_USAGE_EXAMPLES.md)

---

**更新时间**: 2026-01-31
**维护人员**: Coze Coding
