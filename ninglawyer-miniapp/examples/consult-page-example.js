// 咨询页面示例 - 展示如何使用组件和 API
const { aiChat } = require('../../utils/ai-interaction');
const { createMCPClient } = require('../../utils/mcp-client');
const { navigateToCodeSigning, navigateToLyue } = require('../../utils/mini-program-navigator');
const { saveConsultationData, setSceneData } = require('../../utils/data-interaction');

Page({
  data: {
    // 消息列表
    messages: [],
    // 用户信息
    userInfo: {
      avatar: '/assets/images/user-avatar-default.png'
    },
    // 律师信息
    lawyerInfo: {
      avatar: '/assets/images/lawyer-avatar-default.png',
      name: '宁律师'
    },
    // 是否加载中
    loading: false,
    // 当前咨询领域
    domain: 'civil',
    // MCP 客户端
    mcpClient: null,
    // 会话 ID
    sessionId: null
  },

  onLoad(options) {
    console.log('咨询页面加载', options);
    
    // 获取场景参数
    const scene = options.scene;
    if (scene) {
      this.handleScene(scene);
    }
    
    // 初始化 MCP 客户端
    this.initMCP();
  },

  onUnload() {
    // 结束 MCP 会话
    if (this.data.mcpClient) {
      this.data.mcpClient.endSession();
    }
  },

  /**
   * 初始化 MCP 客户端
   */
  async initMCP() {
    try {
      const mcpClient = createMCPClient({
        sessionId: this.data.sessionId,
        context: {
          domain: this.data.domain,
          platform: 'wechat-miniapp'
        }
      });
      
      await mcpClient.init();
      
      this.setData({ mcpClient });
      console.log('MCP 客户端初始化成功');
    } catch (err) {
      console.error('MCP 客户端初始化失败', err);
    }
  },

  /**
   * 处理场景参数
   */
  async handleScene(scene) {
    try {
      // 获取场景数据
      const res = await getDataByScene(scene);
      
      if (res.code === 200 && res.data) {
        const sceneData = res.data;
        
        // 显示欢迎消息
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
   * 发送消息
   */
  async onSendMessage(e) {
    const { text, image } = e.detail;
    
    if (!text && !image) return;
    
    // 添加用户消息
    this.addMessage({
      role: 'user',
      content: text,
      image: image
    });
    
    // 设置加载状态
    this.setData({ loading: true });
    
    try {
      // 使用 MCP 客户端发送消息
      const mcpClient = this.data.mcpClient;
      if (mcpClient) {
        const response = await mcpClient.sendMessage(text);
        
        // 添加助手消息
        this.addMessage({
          role: 'assistant',
          content: response.response,
          actions: response.actions,
          card: response.card
        });
        
        // 处理工具调用结果
        if (response.toolCalls && response.toolCalls.length > 0) {
          await this.handleToolCalls(response.toolCalls);
        }
      } else {
        // 降级使用普通 AI 聊天
        const res = await aiChat({
          domain: this.data.domain,
          question: text,
          chat_history: this.getChatHistory()
        });
        
        // 添加助手消息
        this.addMessage({
          role: 'assistant',
          content: res.data.answer
        });
      }
      
      // 保存咨询数据
      await this.saveConsultation(text, res.data.answer);
      
    } catch (err) {
      console.error('发送消息失败', err);
      
      // 添加错误消息
      this.addMessage({
        role: 'system',
        content: '抱歉，服务暂时不可用，请稍后再试。'
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
      if (toolCall.name === 'draft_contract') {
        // 跳转到合同起草
        await this.jumpToContractDraft(toolCall.parameters);
      } else if (toolCall.name === 'check_performance') {
        // 跳转到履约管理
        await this.jumpToPerformance(toolCall.parameters);
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
        contractInfo,
        from: 'consultation'
      });
      
      // 跳转到码上签约
      await navigateToCodeSigning(contractInfo);
    } catch (err) {
      console.error('跳转失败', err);
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
        contractInfo,
        from: 'consultation'
      });
      
      // 跳转到理约
      await navigateToLyue(contractInfo);
    } catch (err) {
      console.error('跳转失败', err);
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
    
    // 执行快捷操作
    if (action.type === 'navigate') {
      this.handleNavigation(action);
    } else if (action.type === 'api_call') {
      this.handleApiCall(action);
    }
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
    }
  },

  /**
   * 处理 API 调用
   */
  async handleApiCall(action) {
    // 执行 API 调用
    // ...
  },

  /**
   * 添加消息
   */
  addMessage(message) {
    const messages = [...this.data.messages, {
      id: Date.now(),
      timestamp: Date.now(),
      ...message
    }];
    
    this.setData({ messages });
  },

  /**
   * 获取聊天历史
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
        domain: this.data.domain,
        question,
        answer,
        timestamp: Date.now()
      });
    } catch (err) {
      console.error('保存咨询数据失败', err);
    }
  }
});
