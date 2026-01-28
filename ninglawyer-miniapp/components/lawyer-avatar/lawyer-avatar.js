// 律师头像组件
Component({
  properties: {
    name: {
      type: String,
      value: ''
    },
    avatar: {
      type: String,
      value: ''
    },
    domain: {
      type: String,
      value: ''
    },
    status: {
      type: String,
      value: 'online' // online, busy, offline
    },
    size: {
      type: String,
      value: 'default' // small, default, large
    },
    clickable: {
      type: Boolean,
      value: true
    }
  },
  
  methods: {
    // 点击头像
    onAvatarTap() {
      if (!this.properties.clickable) return;
      
      this.triggerEvent('tap', {
        name: this.properties.name,
        domain: this.properties.domain
      });
    },
    
    // 获取头像大小
    getAvatarSize() {
      const sizeMap = {
        small: '64rpx',
        default: '96rpx',
        large: '128rpx'
      };
      return sizeMap[this.properties.size] || sizeMap.default;
    },
    
    // 获取状态指示器大小
    getStatusSize() {
      const sizeMap = {
        small: '16rpx',
        default: '20rpx',
        large: '24rpx'
      };
      return sizeMap[this.properties.size] || sizeMap.default;
    },
    
    // 获取状态颜色
    getStatusColor() {
      const colorMap = {
        online: '#07C160',
        busy: '#FF9500',
        offline: '#C8C9CC'
      };
      return colorMap[this.properties.status] || colorMap.offline;
    }
  }
});
