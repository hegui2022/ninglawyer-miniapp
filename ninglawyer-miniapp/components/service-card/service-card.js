// 服务卡片组件
Component({
  properties: {
    title: {
      type: String,
      value: ''
    },
    description: {
      type: String,
      value: ''
    },
    icon: {
      type: String,
      value: ''
    },
    tag: {
      type: String,
      value: ''
    },
    tagType: {
      type: String,
      value: 'default'
    },
    count: {
      type: Number,
      value: 0
    },
    url: {
      type: String,
      value: ''
    }
  },
  
  methods: {
    // 点击卡片
    onCardTap() {
      const url = this.properties.url;
      if (url) {
        wx.navigateTo({
          url: url
        });
      }
      
      this.triggerEvent('tap', {
        title: this.properties.title
      });
    },
    
    // 获取标签类型样式
    getTagTypeClass() {
      const typeMap = {
        primary: 'tag-primary',
        success: 'tag-success',
        warning: 'tag-warning',
        error: 'tag-error',
        default: 'tag-default'
      };
      return typeMap[this.properties.tagType] || typeMap.default;
    }
  }
});
