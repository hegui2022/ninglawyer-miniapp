# 套餐权限系统实施总结

## ✅ 已完成的工作

### 1. 数据库模型更新
- ✅ 在 `User` 表中添加套餐相关字段：
  - `subscription_type`: 套餐类型（basic/premium/enterprise）
  - `subscription_start_at`: 套餐开始时间
  - `subscription_end_at`: 套餐结束时间
  - `enabled_modules`: 启用的模块列表（JSON）
  - `usage_stats`: 使用统计（JSON）

- ✅ 创建 `SkillPermission` 表：
  - 技能权限管理
  - 套餐级别限制
  - 使用量限制（日/月）

### 2. 套餐配置文件
- ✅ 创建 `src/config/subscription.py`：
  - 定义3种套餐（基础版/专业版/企业版）
  - 定义8个模块及其映射关系
  - 提供权限检查工具函数

### 3. 技能注册表升级
- ✅ 修改 `src/utils/skill_registry.py`：
  - 添加 `required_subscription` 参数
  - 添加权限检查方法 `check_user_permission()`
  - 执行技能时自动检查权限

- ✅ 更新技能注册：
  - `desensitize`: 基础版可用
  - `civil_consult`: 基础版可用
  - `contract_draft`: 专业版及以上可用
  - `contract_review`: 专业版及以上可用

### 4. 主脑智能体升级
- ✅ 修改 `src/agents/master_brain.py`：
  - `route()` 方法添加 `user_id` 参数
  - 路由前检查用户权限
  - 无权限时返回升级提示

### 5. 用户套餐管理API
- ✅ 创建 `src/api/subscription.py`：
  - `GET /api/subscription/plans`: 获取所有套餐
  - `GET /api/user/subscription`: 获取用户套餐
  - `POST /api/subscription/upgrade`: 升级套餐
  - `POST /api/subscription/downgrade`: 降级套餐
  - `GET /api/subscription/modules`: 获取可用模块
  - `GET /api/subscription/usage`: 获取使用统计

- ✅ 注册到路由系统

### 6. 权限检查装饰器
- ✅ 创建 `src/middleware/permission.py`：
  - `@check_subscription_permission()`: 套餐权限检查
  - `@check_skill_permission()`: 技能权限检查
  - `@check_usage_limit()`: 使用量限制检查

### 7. API接口升级
- ✅ 修改 `src/api/consultation.py`：
  - 添加技能权限检查
  - 添加使用量限制
  - 传递用户ID到主脑

---

## 📋 待完成的工作

### 1. 其他API接口权限升级
需要为以下API接口添加权限检查：

#### 高优先级
- [ ] `src/api/contract.py` - 合同API
  - 添加 `@check_skill_permission("contract_draft")`
  - 添加 `@check_usage_limit("contracts_this_month", 50)`

- [ ] `src/api/files.py` - 文件API
  - 添加 `@check_subscription_permission("premium")`
  - 检查文件大小限制

#### 中优先级
- [ ] `src/api/desensitize.py` - 脱敏API
  - 添加 `@check_skill_permission("desensitize")`
  - 添加 `@check_usage_limit("desensitize_this_month", 20)`

- [ ] `src/api/session.py` - 会话API
  - 添加会话数量限制
  - 添加套餐级别检查

#### 低优先级
- [ ] `src/api/admin.py` - 管理API
  - 添加管理员权限检查
  - 添加企业版专属功能检查

### 2. 前端页面开发
需要创建以下前端页面：

#### 套餐管理页面
- [ ] `miniprogram/pages/subscription/subscription.js`
- [ ] `miniprogram/pages/subscription/subscription.wxml`
- [ ] `miniprogram/pages/subscription/subscription.wxss`
- [ ] `miniprogram/pages/subscription/subscription.json`

功能：
- 显示当前套餐信息
- 显示可用套餐列表
- 套餐对比功能
- 升级/降级功能
- 支付集成（可选）

#### 动态菜单组件
- [ ] 修改 `miniprogram/pages/index/index.js`
- [ ] 根据用户套餐动态显示功能菜单
- [ ] 跨小程序跳转功能

### 3. 数据库迁移脚本
需要创建数据库迁移脚本：

- [ ] `scripts/migrate_subscription.py`
  - 添加新字段到 `users` 表
  - 创建 `skill_permissions` 表
  - 初始化默认数据

### 4. 测试用例
需要创建完整的测试用例：

- [ ] `tests/test_subscription.py`
  - 测试套餐升级/降级
  - 测试权限检查
  - 测试使用量限制
  - 测试跨小程序跳转

---

## 🎯 实施指南

### 1. 完成API接口升级

#### 示例：升级 contract.py
```python
from src.middleware.permission import check_skill_permission, check_usage_limit

@contract_bp.route('/draft', methods=['POST'])
@check_skill_permission("contract_draft")
@check_usage_limit("contracts_this_month", 50)
def draft_contract():
    """
    合同起草（需要专业版套餐）
    """
    # ... 原有逻辑
```

#### 示例：升级 files.py
```python
from src.middleware.permission import check_subscription_permission

@files_bp.route('/upload', methods=['POST'])
@check_subscription_permission("premium")
def upload_file():
    """
    文件上传（需要专业版套餐）
    """
    # ... 原有逻辑
```

### 2. 创建前端页面

#### 套餐管理页面结构
```javascript
// miniprogram/pages/subscription/subscription.js
Page({
  data: {
    currentPlan: {},
    availablePlans: [],
    upgradePath: []
  },
  
  async onLoad() {
    await this.loadCurrentPlan()
    await this.loadAvailablePlans()
  },
  
  async loadCurrentPlan() {
    const res = await wx.request({
      url: `${API_BASE_URL}/api/user/subscription`,
      data: { user_id: wx.getStorageSync('user_id') }
    })
    this.setData({ currentPlan: res.data.data })
  },
  
  async loadAvailablePlans() {
    const res = await wx.request({
      url: `${API_BASE_URL}/api/subscription/plans`
    })
    this.setData({ availablePlans: res.data.data })
  },
  
  async handleUpgrade(e) {
    const planId = e.currentTarget.dataset.plan
    const res = await wx.request({
      url: `${API_BASE_URL}/api/subscription/upgrade`,
      method: 'POST',
      data: {
        user_id: wx.getStorageSync('user_id'),
        plan: planId
      }
    })
    // 处理支付或直接升级
    wx.showToast({
      title: '升级成功',
      icon: 'success'
    })
    this.onLoad() // 刷新页面
  }
})
```

### 3. 运行数据库迁移

```bash
# 执行迁移脚本
python scripts/migrate_subscription.py

# 验证迁移结果
python -c "
from src.storage.db import get_db_session
from src.models.models import User, SkillPermission, Base
import inspect

# 检查表结构
print('User模型字段：')
for col in User.__table__.columns:
    print(f'  {col.name}: {col.type}')

print('\nSkillPermission模型字段：')
for col in SkillPermission.__table__.columns:
    print(f'  {col.name}: {col.type}')
"
```

### 4. 测试整个系统

```bash
# 运行测试
python tests/test_subscription.py

# 手动测试
curl http://localhost:5000/api/user/subscription?user_id=1
curl -X POST http://localhost:5000/api/subscription/upgrade \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "plan": "premium"}'
```

---

## 📊 套餐对比

| 功能 | 基础版 | 专业版 | 企业版 |
|------|--------|--------|--------|
| 价格 | ¥0/月 | ¥99/月 | ¥999/月 |
| 法律咨询 | 10次/月 | 100次/月 | 1000次/月 |
| 隐私脱敏 | 20次/月 | 200次/月 | 1000次/月 |
| 合同起草 | ❌ | 50次/月 | 500次/月 |
| 合同审查 | ❌ | 50次/月 | 500次/月 |
| 风险扫描 | ❌ | ❌ | 100次/月 |
| 合规检查 | ❌ | ❌ | 无限次 |
| 电子签约 | ❌ | ❌ | 支持 |
| 合同管理 | ❌ | ❌ | 支持 |
| 文件大小 | 5MB | 20MB | 100MB |
| 优先支持 | ❌ | ✅ | ✅ |
| 数据导出 | ❌ | ✅ | ✅ |
| 团队协作 | ❌ | ❌ | ✅ |
| API访问 | ❌ | ❌ | ✅ |

---

## 🔐 权限级别

### 套餐级别（从低到高）
```
basic (1) < premium (2) < enterprise (3)
```

### 技能权限映射
```python
# 基础版可用
"desensitize" -> "basic"
"civil_consult" -> "basic"

# 专业版可用
"contract_draft" -> "premium"
"contract_review" -> "premium"

# 企业版可用
"risk_scan" -> "enterprise"
"compliance_check" -> "enterprise"
"e_signing" -> "enterprise"
```

---

## 🚀 使用示例

### 用户升级套餐流程

1. **查看当前套餐**
```bash
GET /api/user/subscription?user_id=1
```

2. **查看可用套餐**
```bash
GET /api/subscription/plans
```

3. **升级套餐**
```bash
POST /api/subscription/upgrade
{
  "user_id": 1,
  "plan": "premium"
}
```

4. **获取可用模块**
```bash
GET /api/subscription/modules?user_id=1
```

### 权限检查流程

1. **用户发起请求**
```bash
POST /api/consultation/consult
{
  "user_id": 1,
  "domain": "civil",
  "question": "我遇到了债务纠纷怎么办？"
}
```

2. **装饰器检查权限**
   - 检查用户套餐类型
   - 检查技能需要的套餐
   - 比较套餐级别

3. **检查使用量**
   - 获取当前使用量
   - 检查是否超过限制
   - 更新使用量

4. **执行业务逻辑**
   - 调用技能
   - 返回结果

---

## 📝 注意事项

1. **数据库迁移**：必须在生产环境执行迁移脚本
2. **兼容性**：确保现有用户默认为 basic 套餐
3. **缓存**：套餐信息应该缓存，避免频繁查询数据库
4. **日志**：记录所有权限检查和使用量统计
5. **测试**：务必在测试环境充分测试后再上线

---

## 🎉 完成标志

- [ ] 所有API接口都添加了权限检查
- [ ] 前端套餐管理页面开发完成
- [ ] 数据库迁移脚本执行成功
- [ ] 所有测试用例通过
- [ ] 生产环境部署成功

---

## 📞 支持

如有问题，请查看：
- `src/config/subscription.py` - 套餐配置
- `src/middleware/permission.py` - 权限检查装饰器
- `src/api/subscription.py` - 套餐管理API
