// 消息列表组件
Component({
  properties: {
    // 消息列表
    messages: {
      type: Array,
      value: []
    },
    // 用户信息
    userInfo: {
      type: Object,
      value: {
        avatar: '/assets/images/user-avatar-default.png'
      }
    },
    // 律师信息
    lawyerInfo: {
      type: Object,
      value: {
        avatar: '/assets/images/lawyer-avatar-default.png'
      }
    },
    // 是否显示欢迎消息
    showWelcome: {
      type: Boolean,
      value: true
    },
    // 欢迎消息
    welcomeMessage: {
      type: Object,
      value: {
        text: '您好！我是宁律师，很高兴为您服务。请问有什么法律问题需要咨询？',
        avatar: '/assets/images/lawyer-avatar-default.png'
      }
    },
    // 是否加载中
    loading: {
      type: Boolean,
      value: false
    },
    // 滚动到的消息 ID
    scrollIntoView: {
      type: String,
      value: ''
    }
  },

  data: {},

  methods: {
    // 预览图片
    onPreviewImage(e) {
      const url = e.currentTarget.dataset.url;
      wx.previewImage({
        current: url,
        urls: [url]
      });
    },

    // 快捷操作点击
    onActionClick(e) {
      const action = e.currentTarget.dataset.action;
      this.triggerEvent('action', { action });
    },

    // 卡片操作点击
    onCardActionClick(e) {
      const action = e.currentTarget.dataset.action;
      this.triggerEvent('cardAction', { action });
    },

    // 滚动到底部
    scrollToBottom() {
      const messages = this.properties.messages;
      if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        this.setData({
          scrollIntoView: `msg-${lastMessage.id}`
        });
      }
    },

    // 添加消息
    addMessage(message) {
      const messages = [...this.properties.messages, message];
      this.setData({ messages });
      
      // 滚动到底部
      setTimeout(() => {
        this.scrollToBottom();
      }, 100);
    },

    // 更新最后一条消息
    updateLastMessage(content) {
      const messages = [...this.properties.messages];
      const lastMessage = messages[messages.length - 1];
      
      if (lastMessage) {
        lastMessage.content = content;
        this.setData({ messages });
      }
    },

    // 清空消息列表
    clearMessages() {
      this.setData({
        messages: []
      });
    }
  },

  observers: {
    'messages.length': function(length) {
      if (length > 0) {
        setTimeout(() => {
          this.scrollToBottom();
        }, 100);
      }
    }
  }
});
