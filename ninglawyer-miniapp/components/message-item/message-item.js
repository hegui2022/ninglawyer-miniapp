// 消息项组件
Component({
  properties: {
    message: {
      type: Object,
      value: {}
    },
    isSelf: {
      type: Boolean,
      value: false
    }
  },
  
  methods: {
    // 获取消息类型
    getMessageType() {
      return this.properties.message.type || 'text';
    },
    
    // 获取消息内容
    getMessageContent() {
      return this.properties.message.content || '';
    },
    
    // 获取消息时间
    getMessageTime() {
      const time = this.properties.message.time;
      if (!time) return '';
      return this.formatTime(time);
    },
    
    // 格式化时间
    formatTime(timestamp) {
      const date = new Date(timestamp);
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return `${hours}:${minutes}`;
    },
    
    // 点击消息
    onMessageTap() {
      this.triggerEvent('messageTap', {
        message: this.properties.message
      });
    }
  }
});
