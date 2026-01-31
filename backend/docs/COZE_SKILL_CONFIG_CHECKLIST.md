# 扣子SKILL集成 - 需要配置的环境变量清单

## 📋 您需要配置的环境变量

### 核心配置（必须）

| 环境变量名 | 说明 | 您需要填入的值 |
|-----------|------|--------------|
| `COZE_SKILL_API_BASE_URL` | SKILL API基础URL | ? |
| `COZE_SKILL_API_KEY` | SKILL API认证密钥 | ? |

### SKILL ID配置（必须）

| 环境变量名 | 对应SKILL | 您需要填入的值 |
|-----------|----------|--------------|
| `COZE_SKILL_CIVIL_ID` | 民事咨询SKILL | ? |
| `COZE_SKILL_CRIMINAL_ID` | 刑事咨询SKILL | ? |
| `COZE_SKILL_COMPANY_ID` | 公司法务SKILL | ? |
| `COZE_SKILL_LABOR_ID` | 劳动纠纷SKILL | ? |
| `COZE_SKILL_MARRIAGE_ID` | 婚姻家庭SKILL | ? |
| `COZE_SKILL_IP_ID` | 知识产权SKILL | ? |
| `COZE_SKILL_CONTRACT_DRAFT_ID` | 合同起草SKILL | ? |
| `COZE_SKILL_CONTRACT_REVIEW_ID` | 合同审查SKILL | ? |
| `COZE_SKILL_DESENSITIZE_ID` | 信息脱敏SKILL | ? |

### 可选配置

| 环境变量名 | 说明 | 默认值 |
|-----------|------|--------|
| `COZE_SKILL_TIMEOUT` | API调用超时时间（秒） | 300 |

---

## ✅ 配置检查清单

请按照以下步骤配置：

### 第1步：获取API信息

- [ ] 登录扣子平台
- [ ] 获取SKILL API Base URL
- [ ] 获取SKILL API Key

### 第2步：获取SKILL ID

- [ ] 获取民事咨询SKILL ID
- [ ] 获取刑事咨询SKILL ID
- [ ] 获取公司法务SKILL ID
- [ ] 获取劳动纠纷SKILL ID
- [ ] 获取婚姻家庭SKILL ID
- [ ] 获取知识产权SKILL ID
- [ ] 获取合同起草SKILL ID
- [ ] 获取合同审查SKILL ID
- [ ] 获取信息脱敏SKILL ID

### 第3步：配置环境变量

**本地开发**：

编辑 `backend/.env` 文件，添加：

```env
COZE_SKILL_API_BASE_URL=?
COZE_SKILL_API_KEY=?
COZE_SKILL_CIVIL_ID=?
COZE_SKILL_CRIMINAL_ID=?
COZE_SKILL_COMPANY_ID=?
COZE_SKILL_LABOR_ID=?
COZE_SKILL_MARRIAGE_ID=?
COZE_SKILL_IP_ID=?
COZE_SKILL_CONTRACT_DRAFT_ID=?
COZE_SKILL_CONTRACT_REVIEW_ID=?
COZE_SKILL_DESENSITIZE_ID=?
COZE_SKILL_TIMEOUT=300
```

**云平台部署**：

在部署平台的"环境变量"配置页面添加上述所有变量。

### 第4步：告诉我配置完成

配置完成后，请回复：**"环境变量配置完成"**

然后我会：
1. 创建SKILL调用服务模块
2. 修改后端代码集成SKILL调用
3. 创建测试脚本
4. 测试SKILL调用功能

---

## 📝 配置示例

假设您的SKILL信息如下：

```
API Base URL: https://api.coze.com/v1
API Key: pat_1234567890abcdefghijklmnopqrstuvwxyz

民事咨询SKILL ID: skill_abc123
刑事咨询SKILL ID: skill_def456
合同起草SKILL ID: skill_ghi789
...
```

那么您的环境变量配置应该是：

```env
COZE_SKILL_API_BASE_URL=https://api.coze.com/v1
COZE_SKILL_API_KEY=pat_1234567890abcdefghijklmnopqrstuvwxyz
COZE_SKILL_CIVIL_ID=skill_abc123
COZE_SKILL_CRIMINAL_ID=skill_def456
COZE_SKILL_COMPANY_ID=skill_jkl012
COZE_SKILL_LABOR_ID=skill_mno345
COZE_SKILL_MARRIAGE_ID=skill_pqr678
COZE_SKILL_IP_ID=skill_stu901
COZE_SKILL_CONTRACT_DRAFT_ID=skill_ghi789
COZE_SKILL_CONTRACT_REVIEW_ID=skill_vwx234
COZE_SKILL_DESENSITIZE_ID=skill_yza567
COZE_SKILL_TIMEOUT=300
```

---

## 🚀 配置完成后

请回复：**"环境变量配置完成"**

我会立即开始：
1. ✅ 创建SKILL调用服务模块
2. ✅ 修改咨询、合同等API集成SKILL
3. ✅ 创建SKILL测试脚本
4. ✅ 更新相关文档

---

**注意**：
- 请将 `?` 替换为您的实际值
- API Key请妥善保管，不要泄露
- .env文件不要提交到版本控制
