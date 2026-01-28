// 导航栏组件
Component({
  properties: {
    title: {
      type: String,
      value: ''
    },
    background: {
      type: String,
      value: '#07C160'
    },
    textColor: {
      type: String,
      value: '#ffffff'
    },
    showBack: {
      type: Boolean,
      value: true
    },
    showHome: {
      type: Boolean,
      value: false
    },
    fixed: {
      type: Boolean,
      value: true
    }
  },
  
  methods: {
    // 返回上一页
    onBack() {
      const pages = getCurrentPages();
      if (pages.length > 1) {
        wx.navigateBack();
      } else {
        wx.switchTab({
          url: '/pages/index/index'
        });
      }
    },
    
    // 返回首页
    onHome() {
      wx.switchTab({
        url: '/pages/index/index'
      });
    }
  }
});
