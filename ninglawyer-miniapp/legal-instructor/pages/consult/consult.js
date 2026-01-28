// 咨询对话页面
Page({
  data: {
    lawyerInfo: null,
    messages: [],
    inputText: '',
    isTyping: false,
    scrollToView: '',
    quickQuestions: [
      '请帮我分析这个合同',
      '离婚需要什么手续',
      '工伤赔偿标准是什么',
      '公司违法解除劳动合同怎么办'
    ]
  },

  onLoad(options) {
    const lawyerId = options.lawyerId;
    if (lawyerId) {
      this.loadLawyerInfo(lawyerId);
    }
    
    // 初始化欢迎消息
    this.initWelcomeMessage();
  },

  onReady() {
    // 设置导航栏
    wx.setNavigationBarTitle({
      title: this.data.lawyerInfo ? this.data.lawyerInfo.name : '咨询'
    });
  },

  // 加载律师信息
  loadLawyerInfo(lawyerId) {
    // 这里从参数获取或从API获取
    const lawyers = {
      'civil': { id: 'civil', name: '宁律师·民事', avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=民事', description: '民事纠纷专家' },
      'criminal': { id: 'criminal', name: '宁律师·刑事', avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=刑事', description: '刑事辩护专家' },
      'labor': { id: 'labor', name: '宁律师·劳动', avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=劳动', description: '劳动纠纷专家' },
      'company': { id: 'company', name: '宁律师·公司', avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=公司', description: '公司法律专家' },
      'ip': { id: 'ip', name: '宁律师·知识产权', avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=知识产权', description: '知识产权专家' },
      'marriage': { id: 'marriage', name: '宁律师·婚姻', avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=婚姻', description: '婚姻家庭专家' },
      'contract': { id: 'contract', name: '宁律师·合同', avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=合同', description: '合同法律专家' }
    };

    this.setData({
      lawyerInfo: lawyers[lawyerId] || lawyers['civil']
    });
  },

  // 初始化欢迎消息
  initWelcomeMessage() {
    const welcomeMessage = {
      id: Date.now(),
      type: 'system',
      content: '您好！我是' + (this.data.lawyerInfo ? this.data.lawyerInfo.name : '宁律师') + '，请问有什么可以帮助您的？',
      time: this.formatTime(new Date())
    };

    this.setData({
      messages: [welcomeMessage]
    });
  },

  // 输入框输入
  onInput(e) {
    this.setData({
      inputText: e.detail.value
    });
  },

  // 发送消息
  onSend() {
    const inputText = this.data.inputText.trim();
    if (!inputText) return;

    // 添加用户消息
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputText,
      time: this.formatTime(new Date())
    };

    this.setData({
      messages: [...this.data.messages, userMessage],
      inputText: '',
      isTyping: true,
      scrollToView: 'msg-' + userMessage.id
    });

    // 模拟AI回复
    this.simulateAIReply(inputText);
  },

  // 模拟AI回复
  simulateAIReply(question) {
    setTimeout(() => {
      const replies = [
        '根据您的描述，我建议您首先收集相关证据，包括合同、聊天记录等。然后可以考虑以下几种解决方式...',
        '这是一个常见的法律问题。根据《民法典》相关规定，您有权要求对方承担违约责任...',
        '针对您的情况，建议您先与对方进行协商，如果协商不成，可以考虑通过法律途径解决...',
        '您的这个问题涉及到多个法律方面，我建议您提供更详细的信息，以便我给出更准确的建议...'
      ];

      const reply = {
        id: Date.now(),
        type: 'ai',
        content: replies[Math.floor(Math.random() * replies.length)],
        time: this.formatTime(new Date())
      };

      this.setData({
        messages: [...this.data.messages, reply],
        isTyping: false,
        scrollToView: 'msg-' + reply.id
      });
    }, 1500);
  },

  // 点击快捷问题
  onQuickQuestion(e) {
    const question = e.currentTarget.dataset.question;
    this.setData({
      inputText: question
    });
    this.onSend();
  },

  // 图片上传
  onChooseImage() {
    wx.chooseImage({
      count: 3,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePaths = res.tempFilePaths;
        
        // 发送图片消息
        tempFilePaths.forEach((filePath) => {
          const message = {
            id: Date.now(),
            type: 'image',
            content: filePath,
            time: this.formatTime(new Date())
          };

          this.setData({
            messages: [...this.data.messages, message]
          });
        });
      }
    });
  },

  // 语音输入
  onVoiceInput() {
    wx.showToast({
      title: '语音功能开发中',
      icon: 'none'
    });
  },

  // 查看图片
  onViewImage(e) {
    const url = e.currentTarget.dataset.url;
    wx.previewImage({
      urls: [url]
    });
  },

  // 格式化时间
  formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  },

  // 滚动到底部
  scrollToBottom() {
    this.setData({
      scrollToView: ''
    });
    setTimeout(() => {
      const messages = this.data.messages;
      if (messages.length > 0) {
        this.setData({
          scrollToView: 'msg-' + messages[messages.length - 1].id
        });
      }
    }, 100);
  },

  onShareAppMessage() {
    return {
      title: this.data.lawyerInfo ? this.data.lawyerInfo.name + ' - 法律咨询' : '宁律师法律咨询',
      path: '/pages/consult/consult?lawyerId=' + (this.data.lawyerInfo ? this.data.lawyerInfo.id : '')
    };
  }
});
