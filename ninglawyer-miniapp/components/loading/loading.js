// 加载中组件
Component({
  properties: {
    loading: {
      type: Boolean,
      value: false
    },
    text: {
      type: String,
      value: '加载中...'
    },
    size: {
      type: String,
      value: 'default'
    }
  },
  
  methods: {
    // 获取加载图标大小
    getIconSize() {
      const sizeMap = {
        small: '32rpx',
        default: '48rpx',
        large: '64rpx'
      };
      return sizeMap[this.properties.size] || sizeMap.default;
    },
    
    // 获取文本大小
    getTextSize() {
      const sizeMap = {
        small: '24rpx',
        default: '28rpx',
        large: '32rpx'
      };
      return sizeMap[this.properties.size] || sizeMap.default;
    }
  }
});
