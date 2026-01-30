// 咨询对话页面 - 组件化版本
const { aiChat } = require('../../utils/ai-interaction');
const { createMCPClient } = require('../../utils/mcp-client');
const { navigateToCodeSigning, navigateToLyue, navigateToZenmePan, navigateToPreventRisk } = require('../../utils/mini-program-navigator');
const { saveConsultationData, setSceneData, getDataByScene } = require('../../utils/data-interaction');

Page({
  data: {
    // 消息列表
    messages: [],
    // 用户信息
    userInfo: {
      avatar: '/assets/images/user-avatar-default.png',
      nickname: '用户'
    },
    // 律师信息
    lawyerInfo: {
      avatar: '/assets/images/lawyer-avatar-default.png',
      name: '宁律师',
      domain: 'civil'
    },
    // 是否显示欢迎消息
    showWelcome: true,
    // 欢迎消息
    welcomeMessage: {
      text: '您好！我是宁律师，很高兴为您服务。\n\n我可以帮助您：\n• 解答法律咨询\n• 起草合同\n• 审查合同\n• 分析违约风险\n• 提供维权建议\n\n请问有什么法律问题需要咨询？',
      avatar: '/assets/images/lawyer-avatar-default.png'
    },
    // 是否加载中
    loading: false,
    // 是否显示快捷问题
    showQuickQuestions: true,
    // 快捷问题
    quickQuestions: [
      '合同违约怎么办？',
      '如何起草劳动合同？',
      '公司注册需要什么材料？',
      '离婚财产如何分割？',
      '知识产权怎么保护？'
    ],
    // 滚动到的消息 ID
    scrollToView: '',
    // MCP 客户端
    mcpClient: null,
    // 当前咨询领域
    currentDomain: 'civil',
    // 会话 ID
    sessionId: null
  },

  onLoad(options) {
    console.log('咨询页面加载', options);
    
    // 获取用户信息
    this.getUserInfo();
    
    // 处理场景参数
    if (options.scene) {
      this.handleScene(options.scene);
    }
    
    // 获取传递的参数
    if (options.domain) {
      this.setData({ currentDomain: options.domain });
    }
    
    // 初始化 MCP 客户端
    this.initMCP();
    
    // 加载聊天历史
    this.loadChatHistory();
  },

  onShow() {
    // 页面显示时检查是否有新的场景数据
    this.checkSceneData();
  },

  onUnload() {
    // 结束 MCP 会话
    if (this.data.mcpClient) {
      this.data.mcpClient.endSession().catch(err => {
        console.error('结束 MCP 会话失败', err);
      });
    }
  },

  /**
   * 获取用户信息
   */
  getUserInfo() {
    try {
      const userInfo = wx.getStorageSync('userInfo');
      if (userInfo) {
        this.setData({ userInfo });
      }
    } catch (err) {
      console.error('获取用户信息失败', err);
    }
  },

  /**
   * 初始化 MCP 客户端
   */
  async initMCP() {
    try {
      const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      const mcpClient = createMCPClient({
        sessionId,
        context: {
          domain: this.data.currentDomain,
          platform: 'wechat-miniapp',
          user_id: this.data.userInfo.id || 'anonymous'
        }
      });
      
      await mcpClient.init();
      
      this.setData({ 
        mcpClient, 
        sessionId 
      });
      
      console.log('MCP 客户端初始化成功');
    } catch (err) {
      console.error('MCP 客户端初始化失败', err);
      // MCP 初始化失败不影响基本功能
    }
  },

  /**
   * 加载聊天历史
   */
  loadChatHistory() {
    try {
      const history = wx.getStorageSync('chatHistory') || [];
      if (history.length > 0) {
        this.setData({ 
          messages: history,
          showWelcome: false,
          showQuickQuestions: false
        });
        
        // 滚动到底部
        setTimeout(() => {
          this.scrollToBottom();
        }, 100);
      }
    } catch (err) {
      console.error('加载聊天历史失败', err);
    }
  },

  /**
   * 保存聊天历史
   */
  saveChatHistory() {
    try {
      const messages = this.data.messages;
      if (messages.length > 0) {
        wx.setStorageSync('chatHistory', messages);
      }
    } catch (err) {
      console.error('保存聊天历史失败', err);
    }
  },

  /**
   * 处理场景参数
   */
  async handleScene(scene) {
    try {
      const res = await getDataByScene(scene);
      
      if (res.code === 200 && res.data) {
        const sceneData = res.data;
        
        // 隐藏欢迎消息和快捷问题
        this.setData({
          showWelcome: false,
          showQuickQuestions: false
        });
        
        // 添加场景消息
        this.addMessage({
          role: 'assistant',
          content: sceneData.welcomeMessage || '您好！有什么我可以帮助您的吗？',
          card: sceneData.card
        });
      }
    } catch (err) {
      console.error('处理场景失败', err);
    }
  },

  /**
   * 检查场景数据
   */
  async checkSceneData() {
    // 这里可以检查是否有其他小程序传来的数据
    // ...
  },

  /**
   * 发送消息
   */
  async onSendMessage(e) {
    const { text, image } = e.detail;
    
    if (!text && !image) return;
    
    // 隐藏欢迎消息和快捷问题
    this.setData({
      showWelcome: false,
      showQuickQuestions: false
    });
    
    // 添加用户消息
    this.addMessage({
      role: 'user',
      content: text,
      image: image
    });
    
    // 设置加载状态
    this.setData({ loading: true });
    
    try {
      let response;
      
      // 优先使用 MCP 客户端
      if (this.data.mcpClient) {
        response = await this.data.mcpClient.sendMessage(text);
        
        // 添加助手消息
        this.addMessage({
          role: 'assistant',
          content: response.response,
          actions: response.actions,
          card: response.card
        });
        
        // 处理工具调用
        if (response.toolCalls && response.toolCalls.length > 0) {
          await this.handleToolCalls(response.toolCalls);
        }
      } else {
        // 降级使用普通 AI 聊天
        const res = await aiChat({
          domain: this.data.currentDomain,
          question: text,
          chat_history: this.getChatHistory()
        });
        
        response = res.data;
        
        // 添加助手消息
        this.addMessage({
          role: 'assistant',
          content: response.answer
        });
      }
      
      // 保存咨询数据
      await this.saveConsultation(text, response.response || response.answer);
      
      // 保存聊天历史
      this.saveChatHistory();
      
    } catch (err) {
      console.error('发送消息失败', err);
      
      // 添加错误消息
      this.addMessage({
        role: 'system',
        content: '抱歉，服务暂时不可用，请稍后再试。'
      });
      
      wx.showToast({
        title: '发送失败，请重试',
        icon: 'none'
      });
    } finally {
      this.setData({ loading: false });
    }
  },

  /**
   * 处理工具调用
   */
  async handleToolCalls(toolCalls) {
    for (const toolCall of toolCalls) {
      try {
        if (toolCall.name === 'draft_contract') {
          await this.jumpToContractDraft(toolCall.parameters);
        } else if (toolCall.name === 'check_performance') {
          await this.jumpToPerformance(toolCall.parameters);
        } else if (toolCall.name === 'analyze_breach') {
          await this.jumpToJudgment(toolCall.parameters);
        } else if (toolCall.name === 'scan_risk') {
          await this.jumpToRisk(toolCall.parameters);
        }
      } catch (err) {
        console.error(`工具调用失败: ${toolCall.name}`, err);
      }
    }
  },

  /**
   * 跳转到合同起草
   */
  async jumpToContractDraft(contractInfo) {
    try {
      // 设置场景数据
      await setSceneData('contract_draft', {
        contractInfo: contractInfo || {},
        from: 'consultation',
        timestamp: Date.now()
      });
      
      // 跳转到码上签约
      await navigateToCodeSigning(contractInfo);
    } catch (err) {
      console.error('跳转到合同起草失败', err);
      wx.showToast({
        title: '跳转失败',
        icon: 'none'
      });
    }
  },

  /**
   * 跳转到履约管理
   */
  async jumpToPerformance(contractInfo) {
    try {
      // 设置场景数据
      await setSceneData('contract_performance', {
        contractInfo: contractInfo || {},
        from: 'consultation',
        timestamp: Date.now()
      });
      
      // 跳转到理约
      await navigateToLyue(contractInfo);
    } catch (err) {
      console.error('跳转到履约管理失败', err);
      wx.showToast({
        title: '跳转失败',
        icon: 'none'
      });
    }
  },

  /**
   * 跳转到违约判断
   */
  async jumpToJudgment(disputeInfo) {
    try {
      // 设置场景数据
      await setSceneData('breach_judgment', {
        disputeInfo: disputeInfo || {},
        from: 'consultation',
        timestamp: Date.now()
      });
      
      // 跳转到怎么判
      await navigateToZenmePan(disputeInfo);
    } catch (err) {
      console.error('跳转到违约判断失败', err);
      wx.showToast({
        title: '跳转失败',
        icon: 'none'
      });
    }
  },

  /**
   * 跳转到风险防控
   */
  async jumpToRisk(riskInfo) {
    try {
      // 设置场景数据
      await setSceneData('risk_prevention', {
        riskInfo: riskInfo || {},
        from: 'consultation',
        timestamp: Date.now()
      });
      
      // 跳转到防风险
      await navigateToPreventRisk(riskInfo);
    } catch (err) {
      console.error('跳转到风险防控失败', err);
      wx.showToast({
        title: '跳转失败',
        icon: 'none'
      });
    }
  },

  /**
   * 处理快捷操作点击
   */
  onActionClick(e) {
    const { action } = e.detail;
    console.log('快捷操作点击', action);
    
    // 执行快捷操作
    if (action.type === 'navigate') {
      this.handleNavigation(action);
    } else if (action.type === 'api_call') {
      this.handleApiCall(action);
    } else if (action.type === 'message') {
      // 发送消息
      this.triggerSendMessage(action.message);
    }
  },

  /**
   * 处理卡片操作点击
   */
  onCardActionClick(e) {
    const { action } = e.detail;
    console.log('卡片操作点击', action);
    this.onActionClick({ detail: { action } });
  },

  /**
   * 处理导航操作
   */
  async handleNavigation(action) {
    const { target, params } = action;
    
    if (target === 'contract') {
      await this.jumpToContractDraft(params);
    } else if (target === 'performance') {
      await this.jumpToPerformance(params);
    } else if (target === 'judgment') {
      await this.jumpToJudgment(params);
    } else if (target === 'risk') {
      await this.jumpToRisk(params);
    }
  },

  /**
   * 处理 API 调用
   */
  async handleApiCall(action) {
    // 执行 API 调用
    // ...
    console.log('执行 API 调用', action);
  },

  /**
   * 触发发送消息
   */
  triggerSendMessage(message) {
    this.onSendMessage({ detail: { text: message } });
  },

  /**
   * 点击快捷问题
   */
  onQuickQuestion(e) {
    const question = e.currentTarget.dataset.question;
    this.triggerSendMessage(question);
  },

  /**
   * 输入框聚焦
   */
  onInputFocus(e) {
    console.log('输入框聚焦', e);
  },

  /**
   * 输入框失焦
   */
  onInputBlur(e) {
    console.log('输入框失焦', e);
  },

  /**
   * 添加消息
   */
  addMessage(message) {
    const messages = [...this.data.messages, {
      id: Date.now() + Math.random().toString(36).substr(2, 9),
      timestamp: Date.now(),
      ...message
    }];
    
    this.setData({ messages });
    
    // 滚动到底部
    setTimeout(() => {
      this.scrollToBottom();
    }, 100);
  },

  /**
   * 滚动到底部
   */
  scrollToBottom() {
    const messages = this.data.messages;
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      this.setData({
        scrollToView: `msg-${lastMessage.id}`
      });
    }
  },

  /**
   * 获取聊天历史（用于 API 调用）
   */
  getChatHistory() {
    return this.data.messages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));
  },

  /**
   * 保存咨询数据
   */
  async saveConsultation(question, answer) {
    try {
      await saveConsultationData({
        domain: this.data.currentDomain,
        question,
        answer,
        user_id: this.data.userInfo.id || 'anonymous',
        timestamp: Date.now()
      });
    } catch (err) {
      console.error('保存咨询数据失败', err);
    }
  },

  /**
   * 清空聊天
   */
  clearChat() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有聊天记录吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({
            messages: [],
            showWelcome: true,
            showQuickQuestions: true
          });
          
          // 清空本地存储
          try {
            wx.removeStorageSync('chatHistory');
          } catch (err) {
            console.error('清空聊天历史失败', err);
          }
          
          // 清空 MCP 历史
          if (this.data.mcpClient) {
            this.data.mcpClient.clearHistory();
          }
          
          wx.showToast({
            title: '已清空',
            icon: 'success'
          });
        }
      }
    });
  }
});
