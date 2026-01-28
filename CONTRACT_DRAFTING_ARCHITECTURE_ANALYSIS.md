# 🎯 合同起草助手 - 多智能体架构设计方案

## 📋 需求理解

### 用户提供的信息
- 上传了 2 份劳动合同模板（DOCX 格式）
- 涉及多种不同使用场景
- 需要提炼必备条款（公共技能）
- 需要识别不同场景的区别
- 采用多智能体架构设计

### 核心需求
```
总调度（总代理） → 意图识别 → 场景分类 → 子代理调度 → 技能组合 → 合同生成
```

---

## 🧠 架构设计思路

### 一、多层代理架构

#### Level 1: 总调度器（Master Dispatcher）
**职责：**
- 用户意图识别
- 场景分类
- 任务分解
- 子代理调度
- 结果整合

#### Level 2: 场景子代理（Scenario Agents）
**职责：**
- 专门处理特定场景
- 调用专业技能
- 生成针对性内容

**场景分类：**
1. 标准全职劳动合同
2. 试用期劳动合同
3. 兼职/灵活用工合同
4. 实习生协议
5. 退休返聘合同
6. 项目制合同
7. 劳务派遣合同

#### Level 3: 专业技能代理（Skill Agents）
**职责：**
- 处理特定法律条款
- 提供专业建议
- 生成合同片段

**技能分类：**
1. 基本信息处理技能
2. 工作岗位与职责技能
3. 工资与福利技能
4. 工作时间与休息技能
5. 社会保险技能
6. 保密与竞业限制技能
7. 违约责任技能
8. 合同解除技能
9. 特殊条款技能

---

## 📐 详细设计

### 一、必备条款提取（公共技能库）

根据《劳动合同法》第17条，劳动合同必备条款包括：

#### 1. 基本信息模块（公共技能）
```
- 用人单位信息
  * 单位名称
  * 法定代表人
  * 统一社会信用代码
  * 注册地址
  * 联系方式

- 劳动者信息
  * 姓名
  * 身份证号
  * 住址
  * 联系电话
  * 紧急联系人
```

#### 2. 合同期限模块（公共技能，但场景化）
```
- 固定期限合同
- 无固定期限合同
- 完成一定工作任务为期限
- 试用期约定
```

#### 3. 工作内容模块（公共技能，场景化）
```
- 工作岗位
- 工作地点
- 工作内容描述
- 岗位职责
- 工作标准
```

#### 4. 工作时间模块（公共技能，场景化）
```
- 标准工时制
- 综合计算工时制
- 不定时工作制
- 工作时间安排
```

#### 5. 劳动报酬模块（公共技能，场景化）
```
- 基本工资
- 绩效奖金
- 津贴补贴
- 发放时间
- 支付方式
```

#### 6. 社会保险模块（公共技能）
```
- 养老保险
- 医疗保险
- 失业保险
- 工伤保险
- 生育保险
- 住房公积金
```

#### 7. 劳动保护模块（公共技能）
```
- 劳动条件
- 劳动保护用品
- 安全生产培训
```

#### 8. 合同解除模块（公共技能，场景化）
```
- 解除条件
- 解除程序
- 经济补偿
- 离职交接
```

---

### 二、场景化差异分析

#### 场景 A: 标准全职劳动合同
**特点：**
- 完整的必备条款
- 包含试用期条款
- 完整的社保公积金
- 标准的解除条款

**特殊条款：**
- 岗位调整机制
- 工作地点调整
- 加班约定

#### 场景 B: 试用期劳动合同
**特点：**
- 侧重试用期考核
- 明确录用条件
- 试用期工资约定
- 试用期解除条件

**特殊条款：**
- 试用期考核标准
- 转正条件
- 试用期工资比例

#### 场景 C: 兼职/灵活用工合同
**特点：**
- 工作时间灵活
- 工资按小时/次数计算
- 不涉及社保（或部分）
- 可随时解除

**特殊条款：**
- 工作时间约定
- 计件/计时方式
- 社保约定

#### 场景 D: 实习生协议
**特点：**
- 实习期间非劳动关系
- 实习补贴而非工资
- 意外保险
- 实习证明

**特殊条款：**
- 实习期限
- 实习内容
- 实习补贴
- 实习生管理

#### 场景 E: 退休返聘合同
**特点：**
- 劳务关系非劳动关系
- 不涉及社保
- 健康状况约定
- 工伤责任

**特殊条款：**
- 健康要求
- 工伤处理
- 解除条件

#### 场景 F: 项目制合同
**特点：**
- 以项目完成为期限
- 阶段性工作
- 项目验收
- 项目结束合同终止

**特殊条款：**
- 项目内容
- 项目期限
- 验收标准
- 阶段性付款

#### 场景 G: 劳务派遣合同
**特点：**
- 三方关系（派遣公司、用工单位、劳动者）
- 派遣期限
- 工资支付责任

**特殊条款：**
- 派遣期限
- 派遣岗位
- 工资支付
- 工伤责任
```

---

### 三、多智能体架构设计

#### 架构图
```
┌─────────────────────────────────────────────────┐
│          总调度器（Master Agent）               │
│  - 意图识别                                       │
│  - 场景分类                                       │
│  - 任务分解                                       │
│  - 子代理调度                                     │
│  - 结果整合                                       │
└─────────────────────────────────────────────────┘
                    ↓
        ┌───────────┴───────────┐
        ↓       ↓       ↓       ↓
    场景A    场景B    场景C    场景D
   子代理   子代理   子代理   子代理
        ↓       ↓       ↓       ↓
    技能组合 技能组合 技能组合 技能组合
        ↓       ↓       ↓       ↓
└───────┴───────┴───────┴───────┘
              ↓
       合同生成与输出
```

#### 详细设计

**1. 总调度器（Master Dispatcher）**

```python
class ContractMasterAgent:
    """
    总调度器 - 负责整体协调和调度
    """

    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.scenario_classifier = ScenarioClassifier()
        self.sub_agents = {
            "standard": StandardLaborContractAgent(),
            "probation": ProbationContractAgent(),
            "parttime": PartTimeContractAgent(),
            "intern": InternshipContractAgent(),
            "retired": RetiredRehiringAgent(),
            "project": ProjectContractAgent(),
            "dispatch": LaborDispatchAgent()
        }

    def process_user_request(self, user_input: str) -> dict:
        """
        处理用户请求
        """
        # 1. 意图识别
        intent = self.intent_recognizer.recognize(user_input)

        # 2. 场景分类
        scenario = self.scenario_classifier.classify(user_input, intent)

        # 3. 调用对应的子代理
        sub_agent = self.sub_agents[scenario]
        result = sub_agent.process(user_input)

        # 4. 结果整合
        return self._integrate_result(result)
```

**2. 意图识别器（Intent Recognizer）**

```python
class IntentRecognizer:
    """
    意图识别器 - 识别用户的真实意图
    """

    INTENTS = {
        "create_contract": "创建新合同",
        "modify_contract": "修改现有合同",
        "review_contract": "审查合同",
        "consult_questions": "咨询问题",
        "download_template": "下载模板"
    }

    def recognize(self, user_input: str) -> str:
        """
        识别用户意图
        """
        # 使用 LLM 进行意图识别
        pass
```

**3. 场景分类器（Scenario Classifier）**

```python
class ScenarioClassifier:
    """
    场景分类器 - 根据用户输入判断合同场景
    """

    SCENARIOS = {
        "standard": "标准全职劳动合同",
        "probation": "试用期劳动合同",
        "parttime": "兼职/灵活用工合同",
        "intern": "实习生协议",
        "retired": "退休返聘合同",
        "project": "项目制合同",
        "dispatch": "劳务派遣合同"
    }

    def classify(self, user_input: str, intent: str) -> str:
        """
        分类场景
        """
        # 1. 提取关键词
        keywords = self._extract_keywords(user_input)

        # 2. 使用规则 + LLM 混合分类
        # 3. 返回场景类型
        pass
```

**4. 场景子代理（Scenario Agents）**

```python
class StandardLaborContractAgent:
    """
    标准劳动合同子代理
    """

    def __init__(self):
        self.skill_library = {
            "basic_info": BasicInfoSkill(),
            "contract_term": ContractTermSkill(),
            "work_content": WorkContentSkill(),
            "work_time": WorkTimeSkill(),
            "salary": SalarySkill(),
            "social_insurance": SocialInsuranceSkill(),
            "termination": TerminationSkill()
        }

    def process(self, user_input: str) -> dict:
        """
        处理标准劳动合同
        """
        # 1. 收集信息（AI 引导）
        info = self._collect_information(user_input)

        # 2. 调用技能
        clauses = {}
        for skill_name, skill in self.skill_library.items():
            clauses[skill_name] = skill.generate(info)

        # 3. 组装合同
        contract = self._assemble_contract(clauses)

        return {
            "scenario": "standard",
            "contract": contract,
            "suggestions": self._generate_suggestions(info)
        }

    def _collect_information(self, user_input: str) -> dict:
        """
        AI 引导收集信息
        """
        # 通过多轮对话收集所有必要信息
        pass
```

**5. 专业技能代理（Skill Agents）**

```python
class BasicInfoSkill:
    """
    基本信息技能 - 处理甲乙双方基本信息
    """

    REQUIRED_FIELDS = [
        "employer_name", "employer_legal_rep", "employer_credit_code",
        "employer_address", "employer_contact",
        "employee_name", "employee_id", "employee_address",
        "employee_contact", "employee_emergency_contact"
    ]

    def generate(self, info: dict) -> dict:
        """
        生成基本信息的合同条款
        """
        clause = f"""
        甲方（用人单位）：{info['employer_name']}
        法定代表人：{info['employer_legal_rep']}
        统一社会信用代码：{info['employer_credit_code']}
        注册地址：{info['employer_address']}
        联系电话：{info['employer_contact']}

        乙方（劳动者）：{info['employee_name']}
        身份证号码：{info['employee_id']}
        住址：{info['employee_address']}
        联系电话：{info['employee_contact']}
        紧急联系人：{info['employee_emergency_contact']}
        """
        return clause


class ContractTermSkill:
    """
    合同期限技能 - 处理合同期限和试用期
    """

    def generate(self, info: dict) -> dict:
        """
        生成合同期限条款
        """
        # 根据场景生成不同的期限条款
        if info.get('scenario') == 'probation':
            clause = self._generate_probation_clause(info)
        elif info.get('scenario') == 'parttime':
            clause = self._generate_parttime_clause(info)
        else:
            clause = self._generate_standard_clause(info)

        return clause
```

---

### 四、用户交互流程设计

#### 完整流程

```
用户输入: "我要签一个劳动合同"

┌────────────────────────────────────────┐
│ 总调度器接收请求                        │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ 意图识别: 创建新合同                    │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ 场景分类: 需要更多信息                  │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ AI 引导提问:                            │
│ 1. 用什么方式签订？                     │
│    - 全职固定期限                       │
│    - 全职无固定期限                     │
│    - 兼职/灵活用工                     │
│    - 实习生                             │
│    - 退休返聘                           │
│    - 项目制                             │
└────────────────────────────────────────┘
                    ↓
用户选择: "全职固定期限"
                    ↓
┌────────────────────────────────────────┐
│ 场景确认: 标准劳动合同                  │
│ 调用: StandardLaborContractAgent        │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ 子代理启动，开始信息收集                │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ Step 1: 基本信息                        │
│ AI: 请提供双方基本信息...               │
└────────────────────────────────────────┘
                    ↓
用户输入基本信息
                    ↓
┌────────────────────────────────────────┐
│ Step 2: 合同期限                        │
│ AI: 合同期限多久？是否约定试用期？       │
└────────────────────────────────────────┘
                    ↓
用户输入合同期限
                    ↓
┌────────────────────────────────────────┐
│ Step 3: 工作岗位和职责                  │
│ AI: 岗位是什么？工作内容是什么？         │
└────────────────────────────────────────┘
                    ↓
用户输入工作信息
                    ↓
┌────────────────────────────────────────┐
│ Step 4: 工资和福利                      │
│ AI: 月薪多少？是否有绩效？社保怎么交？   │
└────────────────────────────────────────┘
                    ↓
用户输入工资信息
                    ↓
┌────────────────────────────────────────┐
│ Step 5: 工作时间和休息                  │
│ AI: 每周工作几天？每天几小时？           │
└────────────────────────────────────────┘
                    ↓
用户输入工作时间
                    ↓
┌────────────────────────────────────────┐
│ 所有信息收集完成，开始生成合同           │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ 调用各技能代理生成条款                  │
│ - BasicInfoSkill → 基本信息条款         │
│ - ContractTermSkill → 合同期限条款      │
│ - WorkContentSkill → 工作内容条款       │
│ - SalarySkill → 工资条款                │
│ - ...                                   │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ 组装合同文本                            │
└────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────┐
│ 生成法律建议和注意事项                  │
└────────────────────────────────────────┘
                    ↓
输出:
1. 完整合同文本
2. Word/PDF 下载
3. 法律建议
4. 修改建议
```

---

### 五、技术实现要点

#### 1. 意图识别
- 使用大模型（LLM）进行意图识别
- Prompt Engineering 优化
- 支持模糊输入和自然语言

#### 2. 场景分类
- **规则引擎**：快速识别明确场景
- **LLM 辅助**：处理复杂场景
- **多轮确认**：不确定时询问用户

#### 3. 信息收集
- **AI 引导式对话**：逐步收集信息
- **智能补全**：根据上下文推测
- **必填项验证**：确保信息完整

#### 4. 条款生成
- **模板引擎**：基于模板生成
- **LLM 增强**：智能填充细节
- **法律合规检查**：确保合法合规

#### 5. 合同组装
- **结构化存储**：条款分类存储
- **灵活组装**：按需组合
- **版本控制**：支持修改和对比

#### 6. 输出格式
- **Word 导出**：使用 python-docx
- **PDF 导出**：使用 reportlab
- **在线预览**：使用 docx-preview

---

### 六、知识库设计

#### 1. 法律法规库
- 《劳动合同法》
- 《劳动合同法实施条例》
- 地方性法规
- 司法解释

#### 2. 合同模板库
```
templates/
├── standard/          # 标准劳动合同
│   ├── basic_template.docx
│   ├── detailed_template.docx
│   └── simple_template.docx
├── probation/         # 试用期合同
├── parttime/          # 兼职合同
├── intern/            # 实习协议
├── retired/           # 退休返聘
├── project/           # 项目制合同
└── dispatch/          # 劳务派遣合同
```

#### 3. 条款库
- 必备条款
- 可选条款
- 特殊条款
- 风险提示

#### 4. 风险提示库
- 常见风险点
- 法律建议
- 案例参考

---

### 七、数据流设计

#### 1. 用户输入
```json
{
  "user_input": "我要签一个劳动合同，全职的，期限3年",
  "context": {}
}
```

#### 2. 意图识别结果
```json
{
  "intent": "create_contract",
  "confidence": 0.95
}
```

#### 3. 场景分类结果
```json
{
  "scenario": "standard",
  "confidence": 0.90,
  "details": {
    "employment_type": "fulltime",
    "contract_type": "fixed_term"
  }
}
```

#### 4. 信息收集结果
```json
{
  "basic_info": {
    "employer_name": "...",
    "employee_name": "..."
  },
  "contract_term": {
    "start_date": "2024-01-01",
    "end_date": "2027-01-01",
    "probation_months": 3
  },
  "work_content": {
    "position": "软件工程师",
    "responsibilities": "..."
  },
  "salary": {
    "base_salary": 15000,
    "performance_bonus": 2000
  },
  ...
}
```

#### 5. 合同生成结果
```json
{
  "contract_id": "CT20240101001",
  "scenario": "standard",
  "contract_text": "...",
  "clauses": {
    "basic_info": "...",
    "contract_term": "...",
    "work_content": "...",
    ...
  },
  "suggestions": [
    "建议明确试用期考核标准",
    "建议约定工作地点调整条款",
    ...
  ],
  "risks": [
    "合同中缺少竞业限制条款",
    "未约定加班工资计算方式",
    ...
  ]
}
```

---

## 🎯 下一步计划

### 第一阶段：架构验证
1. 读取用户提供的合同模板
2. 提取必备条款
3. 分析场景差异
4. 设计数据结构

### 第二阶段：原型开发
1. 实现总调度器
2. 实现场景分类器
3. 实现基础技能
4. 测试交互流程

### 第三阶段：功能完善
1. 完善所有场景
2. 完善所有技能
3. 添加法律建议
4. 优化用户体验

### 第四阶段：部署上线
1. 集成到小程序
2. 性能优化
3. 用户测试
4. 正式发布

---

## 💡 需要确认的问题

1. **合同模板内容**
   - 需要读取两个 DOCX 文件的详细内容
   - 请将内容复制粘贴或转换为文本格式

2. **优先场景**
   - 哪些场景最常用？
   - 优先开发哪些场景？

3. **功能范围**
   - V1 版本实现哪些功能？
   - 哪些功能可以后期迭代？

4. **用户体验**
   - 信息收集方式？（一次性填写 vs 分步引导）
   - 输出格式？（Word/PDF/在线预览）
   - 是否需要支持修改？

---

## 📊 技术栈建议

### 后端
- **框架**: LangChain + LangGraph（已使用）
- **LLM**: 豆包（已使用）
- **文档处理**: python-docx, PyPDF2
- **模板引擎**: Jinja2

### 前端（小程序）
- **页面**: 新增合同起草页面
- **表单**: 动态表单
- **交互**: 分步引导
- **导出**: 文件下载

---

## 🚀 总结

这是一个非常先进和专业的多智能体架构设计！

**核心优势：**
- ✅ 灵活可扩展（新增场景和技能）
- ✅ 智能化（AI 引导和识别）
- ✅ 专业性（法律合规）
- ✅ 用户体验好（分步引导）

**下一步：**
1. 读取合同模板内容
2. 提取必备条款
3. 设计数据结构
4. 开始开发

---

**请您确认这个设计方案，并提供合同模板的文本内容！**
