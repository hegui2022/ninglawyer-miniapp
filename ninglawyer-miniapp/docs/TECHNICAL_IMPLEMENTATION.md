# 宁律师家族技术实现方案

## 技术栈

### 前端技术
- **框架**：微信小程序原生框架
- **样式**：WXSS + Flexbox + Grid
- **状态管理**：MobX（可选）
- **组件库**：Vant Weapp

### 后端技术
- **框架**：LangChain + LangGraph
- **模型**：doubao-seed + doubao-voice
- **知识库**：Milvus（向量数据库）
- **存储**：PostgreSQL + S3

---

## 1. 页面路由配置

### app.json（主小程序）

```json
{
  "pages": [
    "pages/index/index",
    "pages/lawyer-family/lawyer-family",
    "pages/lawyer-detail/lawyer-detail",
    "pages/consultation/consultation",
    "pages/profile/profile"
  ],
  "tabBar": {
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "images/tabbar/home.png",
        "selectedIconPath": "images/tabbar/home-active.png"
      },
      {
        "pagePath": "pages/lawyer-family/lawyer-family",
        "text": "宁律师",
        "iconPath": "images/tabbar/lawyer.png",
        "selectedIconPath": "images/tabbar/lawyer-active.png"
      },
      {
        "pagePath": "pages/services/services",
        "text": "服务",
        "iconPath": "images/tabbar/services.png",
        "selectedIconPath": "images/tabbar/services-active.png"
      },
      {
        "pagePath": "pages/profile/profile",
        "text": "我的",
        "iconPath": "images/tabbar/profile.png",
        "selectedIconPath": "images/tabbar/profile-active.png"
      }
    ],
    "color": "#9E9E9E",
    "selectedColor": "#4CAF50",
    "backgroundColor": "#FAFAFA"
  }
}
```

---

## 2. 数据结构设计

### 2.1 宁律师配置数据结构

```javascript
// data/lawyers.js

const CIVIL_LAWYER = {
  id: 'ning-lawyer-civil',
  name: '宁律师·民事',
  fullName: '宁律师·民事',
  icon: '👨‍⚖️',
  avatar: '/images/lawyers/civil.png',
  gradient: 'linear-gradient(135deg, #4CAF50 0%, #81C784 100%)',
  themeColor: '#4CAF50',
  description: '专注民事法律服务',
  helpCount: 12345,
  rating: 4.9,
  consultCount: 23000,
  expertise: [
    '合同纠纷', '侵权责任', '婚姻家庭', '继承',
    '劳动争议', '人格权', '物权纠纷', '不当得利'
  ],
  skills: [
    {
      id: 'civil-consult',
      name: '法律咨询',
      icon: '💬',
      description: '语音/文字咨询，7x24小时响应，专业解答民事法律问题',
      agent: 'VoiceConsultationAgent',
      api: '/api/voice/consult'
    },
    {
      id: 'contract-dispute',
      name: '合同纠纷',
      icon: '📄',
      description: '合同审查、违约责任、纠纷分析、维权指导',
      agent: 'ContractDisputeAgent',
      api: '/api/contract/dispute'
    },
    {
      id: 'tort-responsibility',
      name: '侵权责任',
      icon: '🏠',
      description: '侵权认定、损害赔偿、责任划分、证据收集',
      agent: 'TortAgent',
      api: '/api/tort/responsibility'
    },
    {
      id: 'marriage-family',
      name: '婚姻家庭',
      icon: '💑',
      description: '婚姻登记、离婚调解、财产分割、抚养权',
      agent: 'MarriageAgent',
      api: '/api/marriage/family'
    },
    {
      id: 'inheritance',
      name: '继承',
      icon: '👨‍👩‍👧',
      description: '遗嘱起草、继承纠纷、遗产分割、继承程序',
      agent: 'InheritanceAgent',
      api: '/api/inheritance'
    },
    {
      id: 'labor-dispute',
      name: '劳动争议',
      icon: '👷',
      description: '劳动合同、工资纠纷、工伤赔偿、离职补偿',
      agent: 'LaborDisputeAgent',
      api: '/api/labor/dispute'
    }
  ],
  reviews: [
    {
      id: 1,
      stars: '⭐⭐⭐⭐⭐',
      reviewer: '张女士',
      content: '非常专业，帮我解决了劳动合同违约问题，谢谢宁律师！',
      timestamp: '2024-01-20'
    },
    {
      id: 2,
      stars: '⭐⭐⭐⭐⭐',
      reviewer: '李先生',
      content: '咨询很耐心，回答详细，推荐',
      timestamp: '2024-01-18'
    }
  ]
};

// 导出所有宁律师
const LAWYERS = {
  civil: CIVIL_LAWYER,
  criminal: CRIMINAL_LAWYER,
  contract: CONTRACT_LAWYER,
  labor: LABOR_LAWYER,
  company: COMPANY_LAWYER,
  ip: IP_LAWYER,
  marriage: MARRIAGE_LAWYER
};

module.exports = {
  CIVIL_LAWYER,
  CRIMINAL_LAWYER,
  CONTRACT_LAWYER,
  LABOR_LAWYER,
  COMPANY_LAWYER,
  IP_LAWYER,
  MARRIAGE_LAWYER,
  LAWYERS
};
```

---

## 3. 页面实现

### 3.1 宁律师家族首页

```javascript
// pages/lawyer-family/lawyer-family.js
const { LAWYERS } = require('../../data/lawyers');

Page({
  data: {
    searchQuery: '',
    lawyers: [
      LAWYERS.civil,
      LAWYERS.criminal,
      LAWYERS.contract,
      LAWYERS.labor,
      LAWYERS.company,
      LAWYERS.ip,
      LAWYERS.marriage
    ],
    hotConsultations: [
      {
        icon: '📄',
        question: '劳动合同违约怎么办？',
        count: '2.3w次咨询',
        lawyer: '宁律师·劳动',
        domain: 'labor'
      },
      {
        icon: '💑',
        question: '离婚财产如何分割？',
        count: '1.8w次咨询',
        lawyer: '宁律师·婚姻',
        domain: 'marriage'
      },
      {
        icon: '🏢',
        question: '公司如何设立？',
        count: '1.5w次咨询',
        lawyer: '宁律师·公司',
        domain: 'company'
      }
    ],
    recentConsultations: []
  },

  onLoad() {
    this.loadRecentConsultations();
  },

  // 搜索宁律师
  onSearch(e) {
    const query = e.detail.value;
    this.setData({ searchQuery: query });
    
    // 搜索逻辑
    const filtered = this.data.lawyers.filter(lawyer => 
      lawyer.name.includes(query) || 
      lawyer.description.includes(query)
    );
    this.setData({ lawyers: filtered });
  },

  // 选择宁律师
  selectLawyer(e) {
    const domain = e.currentTarget.dataset.domain;
    wx.navigateTo({
      url: `/pages/lawyer-detail/lawyer-detail?domain=${domain}`
    });
  },

  // 热门咨询
  onHotConsultation(e) {
    const domain = e.currentTarget.dataset.domain;
    wx.navigateTo({
      url: `/pages/lawyer-detail/lawyer-detail?domain=${domain}`
    });
  },

  // 加载最近咨询
  loadRecentConsultations() {
    // 从本地存储或API加载
    const recent = wx.getStorageSync('recentConsultations') || [];
    this.setData({ recentConsultations: recent });
  }
});
```

### 3.2 宁律师详情页

```javascript
// pages/lawyer-detail/lawyer-detail.js
const { LAWYERS } = require('../../data/lawyers');

Page({
  data: {
    domain: '',
    lawyer: null,
    activeSkill: null
  },

  onLoad(options) {
    const { domain } = options;
    this.setData({ 
      domain: domain,
      lawyer: LAWYERS[domain]
    });
  },

  // 返回
  goBack() {
    wx.navigateBack();
  },

  // 选择技能
  selectSkill(e) {
    const skill = e.currentTarget.dataset.skill;
    this.setData({ activeSkill: skill });
    
    // 根据技能类型跳转
    if (skill.id.includes('consult')) {
      this.startConsultation();
    } else if (skill.id.includes('draft')) {
      this.startContractDraft();
    } else {
      this.startSkillService(skill);
    }
  },

  // 文字咨询
  textConsult() {
    wx.navigateTo({
      url: `/pages/consultation/consultation?domain=${this.data.domain}&type=text`
    });
  },

  // 语音咨询
  voiceConsult() {
    wx.navigateTo({
      url: `/pages/consultation/consultation?domain=${this.data.domain}&type=voice`
    });
  },

  // 开始咨询
  startConsultation() {
    this.textConsult();
  },

  // 合同起草
  startContractDraft() {
    wx.navigateTo({
      url: `/contract-workshop/pages/draft/draft?domain=contract`
    });
  },

  // 技能服务
  startSkillService(skill) {
    // 调用对应的API
    wx.request({
      url: skill.api,
      method: 'POST',
      data: {
        domain: this.data.domain,
        skillId: skill.id
      },
      success: (res) => {
        // 处理返回结果
        this.showSkillResult(res.data);
      }
    });
  },

  // 显示技能结果
  showSkillResult(result) {
    wx.showModal({
      title: '服务结果',
      content: result.message,
      showCancel: false
    });
  }
});
```

---

## 4. AGENT 后端实现

### 4.1 Master Agent（主脑）

```python
# src/agents/master_agent.py
from typing import Dict, Any
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from .lawyer_factory import LawyerAgentFactory

class MasterAgent:
    """主脑 AGENT - 负责任务路由"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="doubao-seed")
        self.lawyer_factory = LawyerAgentFactory()
        
    def route(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """路由到对应的宁律师"""
        # 1. 意图识别
        intent = self._identify_intent(user_input)
        
        # 2. 获取对应的宁律师
        lawyer_agent = self.lawyer_factory.get_lawyer(intent["domain"])
        
        # 3. 执行任务
        result = lawyer_agent.execute(user_input, context)
        
        return result
    
    def _identify_intent(self, user_input: str) -> Dict[str, Any]:
        """识别用户意图"""
        # 使用 LLM 识别意图
        prompt = f"""
        请分析以下用户输入，识别其法律咨询意图：
        
        用户输入：{user_input}
        
        请返回JSON格式，包含：
        - domain: 法律领域（civil/criminal/contract/labor/company/ip/marriage）
        - intent: 具体意图（consult/draft/review/dispute等）
        - urgency: 紧急程度（high/medium/low）
        """
        
        response = self.llm.invoke(prompt)
        import json
        return json.loads(response)
```

### 4.2 Lawyer Agent Factory（宁律师工厂）

```python
# src/agents/lawyer_factory.py
from typing import Dict
from .ning_lawyer_template import NingLawyerTemplate
from ..config.lawyer_domains import (
    CIVIL_LAWYER_CONFIG,
    CRIMINAL_LAWYER_CONFIG,
    CONTRACT_LAWYER_CONFIG,
    LABOR_LAWYER_CONFIG,
    COMPANY_LAWYER_CONFIG,
    IP_LAWYER_CONFIG,
    MARRIAGE_LAWYER_CONFIG
)

class LawyerAgentFactory:
    """宁律师工厂"""
    
    def __init__(self):
        self._lawyer_cache = {}
        self.domain_configs = {
            'civil': CIVIL_LAWYER_CONFIG,
            'criminal': CRIMINAL_LAWYER_CONFIG,
            'contract': CONTRACT_LAWYER_CONFIG,
            'labor': LABOR_LAWYER_CONFIG,
            'company': COMPANY_LAWYER_CONFIG,
            'ip': IP_LAWYER_CONFIG,
            'marriage': MARRIAGE_LAWYER_CONFIG
        }
    
    def create_lawyer(self, domain: str) -> NingLawyerTemplate:
        """创建宁律师"""
        if domain not in self.domain_configs:
            raise ValueError(f"Unknown domain: {domain}")
        
        config = self.domain_configs[domain]
        return NingLawyerTemplate(config)
    
    def get_lawyer(self, domain: str) -> NingLawyerTemplate:
        """获取宁律师（带缓存）"""
        if domain not in self._lawyer_cache:
            self._lawyer_cache[domain] = self.create_lawyer(domain)
        
        return self._lawyer_cache[domain]
    
    def list_lawyers(self) -> list:
        """列出所有宁律师"""
        return [
            {
                'domain': domain,
                'name': config['persona']['name'],
                'icon': config['persona']['avatar'],
                'description': config['persona']['system_prompt'][:100]
            }
            for domain, config in self.domain_configs.items()
        ]
```

### 4.3 NingLawyerTemplate（宁律师模板）

```python
# src/agents/ning_lawyer_template.py
from typing import Dict, Any
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from ..tools.voice_tool import VoiceTool
from ..tools.knowledge_retrieval_tool import KnowledgeRetrievalTool
from ..tools.evidence_collection_tool import EvidenceCollectionTool

class NingLawyerTemplate:
    """宁律师模板 - 可复用的 AGENT 基类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.domain = config['domain']
        self.persona = config['persona']
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model="doubao-seed",
            system_prompt=self.persona['system_prompt'],
            temperature=self.persona.get('temperature', 0.7)
        )
        
        # 加载工具
        self.tools = self._load_tools()
        
        # 创建 Agent
        self.agent = self._create_agent()
    
    def _load_tools(self) -> list:
        """加载工具"""
        tools = []
        
        # 语音工具
        if 'voice' in self.config:
            tools.append(VoiceTool(
                voice_id=self.config['voice'].get('voice_id')
            ))
        
        # 知识检索工具
        if 'kb' in self.config:
            tools.append(KnowledgeRetrievalTool(
                kb_path=self.config['kb']
            ))
        
        # 证据收集工具
        tools.append(EvidenceCollectionTool())
        
        # 领域专用工具
        for skill in self.config['skills']:
            tool = self._load_skill_tool(skill)
            if tool:
                tools.append(tool)
        
        return tools
    
    def _load_skill_tool(self, skill: str) -> Tool:
        """加载技能工具"""
        # 根据技能名称加载对应的工具
        skill_map = {
            'legal_consult': 'LegalConsultTool',
            'contract_draft': 'ContractDraftTool',
            'contract_review': 'ContractReviewTool',
            'contract_dispute': 'ContractDisputeTool',
            'risk_identification': 'RiskIdentificationTool',
            'compliance_check': 'ComplianceCheckTool'
        }
        
        tool_class_name = skill_map.get(skill)
        if tool_class_name:
            # 动态导入
            from ..tools import legal_consult_tool, contract_tools
            
            if tool_class_name == 'LegalConsultTool':
                return legal_consult_tool
            elif tool_class_name in ['ContractDraftTool', 'ContractReviewTool', 'ContractDisputeTool']:
                return contract_tools.ContractTool(skill)
        
        return None
    
    def _create_agent(self):
        """创建 Agent"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.persona['system_prompt']),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行任务"""
        if context is None:
            context = {}
        
        # 调用 Agent
        result = self.agent.invoke({
            "input": user_input,
            **context
        })
        
        return result
    
    def consult(self, question: str) -> Dict[str, Any]:
        """法律咨询"""
        return self.execute(f"请回答以下法律问题：{question}")
    
    def draft_contract(self, contract_info: Dict[str, Any]) -> Dict[str, Any]:
        """起草合同"""
        if 'contract_draft' not in self.config['skills']:
            return {"error": "该宁律师不具备合同起草技能"}
        
        prompt = f"""
        请根据以下信息起草一份合同：
        
        {contract_info}
        
        要求：
        1. 合同条款完整
        2. 符合法律规定
        3. 保护客户权益
        4. 格式规范
        """
        
        return self.execute(prompt)
```

---

## 5. API 接口设计

### 5.1 咨询接口

```python
# src/api/consultation.py
from flask import Flask, request, jsonify
from src.agents.master_agent import MasterAgent

app = Flask(__name__)
master_agent = MasterAgent()

@app.route('/api/consult', methods=['POST'])
def consult():
    """法律咨询接口"""
    data = request.json
    user_input = data.get('input')
    context = data.get('context', {})
    
    # 路由并执行
    result = master_agent.route(user_input, context)
    
    return jsonify({
        'success': True,
        'data': result
    })

@app.route('/api/voice/consult', methods=['POST'])
def voice_consult():
    """语音咨询接口"""
    data = request.json
    audio_data = data.get('audio')
    
    # 1. 语音识别
    from src.tools.voice_tool import VoiceTool
    voice_tool = VoiceTool()
    text = voice_tool.asr(audio_data)
    
    # 2. 文本咨询
    result = master_agent.route(text, {})
    
    # 3. 语音合成
    audio = voice_tool.tts(result['output'])
    
    return jsonify({
        'success': True,
        'data': {
            'text': result['output'],
            'audio': audio
        }
    })
```

### 5.2 合同起草接口

```python
# src/api/contract.py
from flask import request, jsonify
from src.agents.lawyer_factory import LawyerAgentFactory

lawyer_factory = LawyerAgentFactory()

@app.route('/api/contract/draft', methods=['POST'])
def draft_contract():
    """合同起草接口"""
    data = request.json
    contract_type = data.get('type')
    parties = data.get('parties')
    terms = data.get('terms')
    
    # 获取宁律师·合同
    contract_lawyer = lawyer_factory.get_lawyer('contract')
    
    # 起草合同
    result = contract_lawyer.draft_contract({
        'type': contract_type,
        'parties': parties,
        'terms': terms
    })
    
    return jsonify({
        'success': True,
        'data': result
    })
```

---

## 6. 前端小程序与后端交互

### 6.1 咨询页面

```javascript
// pages/consultation/consultation.js
Page({
  data: {
    domain: '',
    type: '', // text or voice
    messages: [],
    inputText: '',
    isRecording: false,
    recorderManager: null
  },

  onLoad(options) {
    const { domain, type } = options;
    this.setData({ 
      domain: domain,
      type: type
    });
    
    if (type === 'voice') {
      this.initRecorder();
    }
  },

  // 初始化录音
  initRecorder() {
    this.setData({
      recorderManager: wx.getRecorderManager()
    });
    
    this.data.recorderManager.onStop((res) => {
      this.uploadAudio(res.tempFilePath);
    });
  },

  // 发送文字消息
  sendText() {
    const text = this.data.inputText.trim();
    if (!text) return;
    
    // 添加用户消息
    this.addMessage({
      role: 'user',
      content: text
    });
    
    // 调用 API
    this.callConsultationAPI(text);
    
    // 清空输入
    this.setData({ inputText: '' });
  },

  // 开始录音
  startRecord() {
    this.setData({ isRecording: true });
    this.data.recorderManager.start({
      duration: 60000,
      format: 'mp3'
    });
  },

  // 停止录音
  stopRecord() {
    this.setData({ isRecording: false });
    this.data.recorderManager.stop();
  },

  // 上传音频
  uploadAudio(tempFilePath) {
    wx.uploadFile({
      url: 'https://api.example.com/upload',
      filePath: tempFilePath,
      name: 'audio',
      success: (res) => {
        const data = JSON.parse(res.data);
        if (data.success) {
          this.addMessage({
            role: 'user',
            content: '🎤 语音消息',
            audioUrl: data.url
          });
          
          this.callVoiceConsultationAPI(data.url);
        }
      }
    });
  },

  // 调用咨询 API
  callConsultationAPI(text) {
    wx.request({
      url: 'https://api.example.com/api/consult',
      method: 'POST',
      data: {
        input: text,
        context: {
          domain: this.data.domain
        }
      },
      success: (res) => {
        const result = res.data.data;
        this.addMessage({
          role: 'assistant',
          content: result.output
        });
      }
    });
  },

  // 调用语音咨询 API
  callVoiceConsultationAPI(audioUrl) {
    wx.request({
      url: 'https://api.example.com/api/voice/consult',
      method: 'POST',
      data: {
        audio: audioUrl,
        context: {
          domain: this.data.domain
        }
      },
      success: (res) => {
        const result = res.data.data;
        this.addMessage({
          role: 'assistant',
          content: result.text,
          audioUrl: result.audio
        });
      }
    });
  },

  // 添加消息
  addMessage(message) {
    const messages = this.data.messages;
    messages.push({
      ...message,
      timestamp: Date.now()
    });
    this.setData({ messages });
  }
});
```

### 6.2 咨询页面 WXML

```wxml
<!-- pages/consultation/consultation.wxml -->
<view class="consultation-page">
  <!-- 消息列表 -->
  <scroll-view scroll-y class="message-list">
    <view 
      class="message {{item.role}}" 
      wx:for="{{messages}}" 
      wx:key="timestamp"
    >
      <view class="message-content">
        <text wx:if="{{!item.audioUrl}}">{{item.content}}</text>
        
        <!-- 语音消息 -->
        <view wx:if="{{item.audioUrl}}" class="audio-player">
          <audio src="{{item.audioUrl}}" controls />
        </view>
      </view>
      
      <text class="message-time">{{item.timestamp | formatTime}}</text>
    </view>
  </scroll-view>

  <!-- 输入区域 -->
  <view class="input-area">
    <!-- 文字输入 -->
    <block wx:if="{{type === 'text'}}">
      <input 
        class="input" 
        value="{{inputText}}" 
        bindinput="onInput"
        placeholder="请输入您的问题..."
      />
      <button class="send-btn" bindtap="sendText">发送</button>
    </block>

    <!-- 语音输入 -->
    <block wx:if="{{type === 'voice'}}">
      <button 
        class="record-btn {{isRecording ? 'recording' : ''}}" 
        bindtap="{{isRecording ? 'stopRecord' : 'startRecord'}}"
      >
        {{isRecording ? '🔴 录音中...' : '🎙️ 按住说话'}}
      </button>
    </block>
  </view>
</view>
```

---

## 7. 部署方案

### 7.1 小程序部署

```bash
# 1. 使用微信开发者工具
# 2. 点击"上传"
# 3. 填写版本号和备注
# 4. 提交审核
```

### 7.2 后端部署

```bash
# 使用 Docker 部署
docker build -t ning-lawyer-api .
docker run -p 8080:8080 ning-lawyer-api

# 或使用 Kubernetes
kubectl apply -f k8s/
```

---

## 8. 监控与日志

### 8.1 性能监控

```python
# src/utils/monitor.py
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # 记录性能
        performance_log = {
            'function': func.__name__,
            'duration': end_time - start_time,
            'timestamp': time.time()
        }
        
        # 发送到监控系统
        send_to_monitoring(performance_log)
        
        return result
    return wrapper
```

### 8.2 日志记录

```python
import logging

logger = logging.getLogger(__name__)

class LawyerConsultationLogger:
    @staticmethod
    def log_consultation(domain: str, user_input: str, result: dict):
        logger.info({
            'event': 'consultation',
            'domain': domain,
            'user_input': user_input,
            'result': result
        })
```

---

## 总结

本技术实现方案包含：

1. ✅ **前端页面**：首页、详情页、咨询页
2. ✅ **数据结构**：宁律师配置、技能映射
3. ✅ **后端 AGENT**：Master Agent、Lawyer Factory、NingLawyer Template
4. ✅ **API 接口**：咨询接口、合同起草接口
5. ✅ **前后端交互**：文字咨询、语音咨询
6. ✅ **部署方案**：小程序部署、后端部署
7. ✅ **监控日志**：性能监控、日志记录

这个技术方案完整支撑了宁律师家族的开发和部署！🎉
