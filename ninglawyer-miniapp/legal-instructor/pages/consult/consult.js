// pages/consult/consult.js - 咨询对话页面（连接真实后端）
const app = getApp()

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
    ],
    // 当前法律领域
    currentDomain: 'civil'
  },

  onLoad(options) {
    const lawyerId = options.lawyerId || 'civil';
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
      lawyerInfo: lawyers[lawyerId] || lawyers['civil'],
      currentDomain: lawyerId
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
  async onSend() {
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

    // 调用真实后端 API
    try {
      await this.sendToBackend(inputText);
    } catch (error) {
      console.error('咨询失败', error);
      this.handleError(error);
    }
  },

  // 发送到后端 API（真实调用）
  async sendToBackend(question) {
    const apiUrl = app.globalData.config.apiUrl;

    try {
      wx.showLoading({
        title: '思考中...',
        mask: true
      });

      const response = await new Promise((resolve, reject) => {
        wx.request({
          url: `${apiUrl}/consultation/consult`,
          method: 'POST',
          data: {
            domain: this.data.currentDomain,
            question: question,
            chat_history: this.getChatHistory()
          },
          header: {
            'Content-Type': 'application/json',
            'Authorization': wx.getStorageSync('token') || ''
          },
          timeout: 30000,
          success: (res) => {
            if (res.statusCode === 200 && res.data.code === 0) {
              resolve(res.data);
            } else {
              reject(new Error(res.data.message || '请求失败'));
            }
          },
          fail: (err) => {
            reject(err);
          }
        });
      });

      // 添加 AI 回复
      const aiMessage = {
        id: Date.now(),
        type: 'ai',
        content: response.data.answer,
        time: this.formatTime(new Date())
      };

      this.setData({
        messages: [...this.data.messages, aiMessage],
        isTyping: false,
        scrollToView: 'msg-' + aiMessage.id
      });

      // 保存对话历史到本地存储
      this.saveChatHistory();

    } catch (error) {
      throw error;
    } finally {
      wx.hideLoading();
    }
  },

  // 获取对话历史
  getChatHistory() {
    return this.data.messages.map(msg => ({
      role: msg.type === 'user' ? 'user' : 'assistant',
      content: msg.content
    }));
  },

  // 保存对话历史
  saveChatHistory() {
    const historyKey = `chat_history_${this.data.currentDomain}`;
    try {
      wx.setStorageSync(historyKey, this.getChatHistory());
    } catch (error) {
      console.error('保存对话历史失败', error);
    }
  },

  // 加载对话历史
  loadChatHistory() {
    const historyKey = `chat_history_${this.data.currentDomain}`;
    try {
      const history = wx.getStorageSync(historyKey);
      if (history && history.length > 0) {
        const messages = history.map((msg, index) => ({
          id: Date.now() - (history.length - index) * 1000,
          type: msg.role === 'user' ? 'user' : 'ai',
          content: msg.content,
          time: this.formatTime(new Date(Date.now() - (history.length - index) * 1000))
        }));

        this.setData({
          messages: messages
        });
      }
    } catch (error) {
      console.error('加载对话历史失败', error);
    }
  },

  // 错误处理
  handleError(error) {
    console.error('咨询失败', error);

    const errorMessage = {
      id: Date.now(),
      type: 'error',
      content: '抱歉，咨询出现问题，请稍后重试。\n\n错误信息：' + (error.message || '网络错误'),
      time: this.formatTime(new Date())
    };

    this.setData({
      messages: [...this.data.messages, errorMessage],
      isTyping: false
    });

    wx.showToast({
      title: '咨询失败，请稍后重试',
      icon: 'none',
      duration: 2000
    });
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

          // TODO: 上传图片到后端，进行图片分析
          this.uploadImageForAnalysis(filePath);
        });
      }
    });
  },

  // 上传图片进行分析
  async uploadImageForAnalysis(filePath) {
    try {
      wx.showLoading({
        title: '分析中...',
        mask: true
      });

      const apiUrl = app.globalData.config.apiUrl;

      // 先上传图片
      const uploadResponse = await new Promise((resolve, reject) => {
        wx.uploadFile({
          url: `${apiUrl}/upload`,
          filePath: filePath,
          name: 'file',
          header: {
            'Authorization': wx.getStorageSync('token') || ''
          },
          success: (res) => {
            try {
              const data = JSON.parse(res.data);
              if (data.code === 0) {
                resolve(data.data);
              } else {
                reject(new Error(data.message || '上传失败'));
              }
            } catch (error) {
              reject(error);
            }
          },
          fail: (err) => {
            reject(err);
          }
        });
      });

      // 发送图片分析请求
      const analysisResponse = await new Promise((resolve, reject) => {
        wx.request({
          url: `${apiUrl}/consultation/analyze-image`,
          method: 'POST',
          data: {
            image_url: uploadResponse.url,
            domain: this.data.currentDomain
          },
          header: {
            'Content-Type': 'application/json',
            'Authorization': wx.getStorageSync('token') || ''
          },
          success: (res) => {
            if (res.statusCode === 200 && res.data.code === 0) {
              resolve(res.data);
            } else {
              reject(new Error(res.data.message || '分析失败'));
            }
          },
          fail: (err) => {
            reject(err);
          }
        });
      });

      // 添加 AI 回复
      const aiMessage = {
        id: Date.now(),
        type: 'ai',
        content: analysisResponse.data.answer,
        time: this.formatTime(new Date())
      };

      this.setData({
        messages: [...this.data.messages, aiMessage],
        scrollToView: 'msg-' + aiMessage.id
      });

    } catch (error) {
      console.error('图片分析失败', error);
      wx.showToast({
        title: '图片分析失败',
        icon: 'none'
      });
    } finally {
      wx.hideLoading();
    }
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

  // 清空对话
  onClearChat() {
    wx.showModal({
      title: '清空对话',
      content: '确定要清空当前对话吗？',
      success: (res) => {
        if (res.confirm) {
          // 清空消息
          this.setData({
            messages: []
          });

          // 清空本地存储
          const historyKey = `chat_history_${this.data.currentDomain}`;
          try {
            wx.removeStorageSync(historyKey);
          } catch (error) {
            console.error('清空对话历史失败', error);
          }

          // 重新初始化欢迎消息
          this.initWelcomeMessage();

          wx.showToast({
            title: '已清空',
            icon: 'success'
          });
        }
      }
    });
  },

  // 复制内容
  onCopyContent(e) {
    const content = e.currentTarget.dataset.content;
    wx.setClipboardData({
      data: content,
      success: () => {
        wx.showToast({
          title: '已复制',
          icon: 'success'
        });
      }
    });
  },

  onShareAppMessage() {
    return {
      title: this.data.lawyerInfo ? this.data.lawyerInfo.name + ' - 法律咨询' : '宁律师法律咨询',
      path: '/pages/consult/consult?lawyerId=' + (this.data.lawyerInfo ? this.data.lawyerInfo.id : '')
    };
  }
});
