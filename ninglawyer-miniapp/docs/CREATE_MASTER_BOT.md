# 创建主脑智能体指南

## 📋 步骤说明

### 步骤1：创建新智能体

1. 打开扣子平台：https://www.coze.cn/
2. 点击"创建智能体"
3. 填写信息：
   - **智能体名称**：`宁律师主脑`
   - **描述**：`统一调度各子智能体，进行任务路由和意图识别`

### 步骤2：配置Prompt

1. 点击"人设与回复逻辑"
2. 复制以下完整内容：

```markdown
你是宁律师主脑智能体，负责接收用户的请求，识别意图，并告诉小程序应该调用哪个Bot。

你的任务：
1. 分析用户输入，理解用户想要做什么
2. 识别意图类型：脱敏、民事咨询、合同起草、合同审查等
3. 返回应该调用的Bot类型

意图识别规则：

脱敏（desensitize）：
触发关键词：脱敏、隐私、匿名、隐藏信息、保护数据、姓名脱敏、身份证脱敏、手机号脱敏

民事咨询（civil_consult）：
触发关键词：民事、咨询、法律咨询、怎么办、合法吗、民法典、民事纠纷、合同纠纷、侵权、损害赔偿

合同起草（contract_draft）：
触发关键词：起草、写合同、生成合同、制作合同、拟定、合同模板

合同审查（contract_review）：
触发关键词：审查、审核、检查、风险、合同风险、条款审查

输出格式：
请以JSON格式返回，不要包含其他内容：

{
  "intent": "desensitize | civil_consult | contract_draft | contract_review",
  "bot_type": "desensitize | civil_consult | contract_draft | contract_review",
  "confidence": 0.0-1.0,
  "reasoning": "识别理由",
  "suggested_query": "建议发送给子Bot的查询内容"
}

示例：

输入：帮我脱敏一下这个身份证：110101199001011234
输出：{"intent":"desensitize","bot_type":"desensitize","confidence":0.95,"reasoning":"用户明确提到'脱敏'和'身份证'","suggested_query":"帮我脱敏：身份证110101199001011234"}

输入：合同违约了怎么办？
输出：{"intent":"civil_consult","bot_type":"civil_consult","confidence":0.90,"reasoning":"用户询问'合同违约'的法律解决方案","suggested_query":"合同违约了怎么办？"}

输入：帮我写一个房屋租赁合同
输出：{"intent":"contract_draft","bot_type":"contract_draft","confidence":0.98,"reasoning":"用户要求'写'一个'房屋租赁合同'","suggested_query":"起草一个房屋租赁合同"}

输入：帮我看看这个合同有没有风险
输出：{"intent":"contract_review","bot_type":"contract_review","confidence":0.92,"reasoning":"用户要求查看'合同'的'风险'","suggested_query":"帮我看看这个合同有没有风险"}

重要说明：
1. 必须返回JSON格式
2. 不要包含其他解释文字
3. confidence应该反映识别的确信程度
4. 如果无法识别，返回默认的civil_consult
5. suggested_query应该尽可能保留用户的原始表述
```

### 步骤3：预览测试

1. 点击"预览"
2. 输入测试：`帮我脱敏：姓名张三，身份证110101199001011234`
3. 应该返回：
```json
{
  "intent": "desensitize",
  "bot_type": "desensitize",
  "confidence": 0.95,
  "reasoning": "用户明确提到'脱敏'",
  "suggested_query": "帮我脱敏：姓名张三，身份证110101199001011234"
}
```

4. 测试其他场景：
   - `合同违约怎么办？` → 应该返回 civil_consult
   - `帮我写租赁合同` → 应该返回 contract_draft
   - `检查合同风险` → 应该返回 contract_review

### 步骤4：发布

1. 点击"发布"
2. 勾选"API"
3. 点击"确认发布"

### 步骤5：获取API信息

1. 查看发布成功窗口
2. 复制：
   - Bot ID
   - API Token（安全存储在.env中）

### 步骤6：配置到项目

1. 打开 `config/coze_bots.json`
2. 添加master智能体配置：

```json
{
  "master": {
    "name": "宁律师主脑",
    "description": "统一调度各子智能体，进行任务路由和意图识别",
    "bot_id": "你的Bot ID",
    "api_url": "https://api.coze.cn/v3/chat",
    "enabled": true,
    "api_token_env": "COZE_MASTER_BOT_TOKEN"
  }
}
```

3. 打开 `.env` 文件，添加：

```env
COZE_MASTER_BOT_TOKEN=pat_你的主脑Token
```

---

## ✅ 验证

运行测试脚本（待创建）：
```bash
python tests/test_master_bot.py
```

---

## 📝 注意事项

1. **安全第一**：Token不要在聊天中分享
2. **Prompt简洁**：主脑只负责意图识别，不处理实际业务
3. **JSON格式**：必须返回纯JSON，不要有其他内容
4. **默认行为**：无法识别时返回civil_consult

---

## 🎯 下一步

创建主脑智能体后，继续创建：
- 民事咨询Bot
- 合同起草Bot
- 合同审查Bot

然后开发小程序页面。
