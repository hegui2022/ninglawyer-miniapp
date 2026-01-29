// 导航栏组件
Component({
  properties: {
    // 标题
    title: {
      type: String,
      value: ''
    },
    // 背景颜色
    background: {
      type: String,
      value: '#07C160'
    },
    // 文字颜色
    textColor: {
      type: String,
      value: '#ffffff'
    },
    // 是否显示返回按钮
    showBack: {
      type: Boolean,
      value: true
    },
    // 是否显示首页按钮
    showHome: {
      type: Boolean,
      value: false
    },
    // 是否固定在顶部
    fixed: {
      type: Boolean,
      value: true
    }
  },

  data: {
    // 状态栏高度
    statusBarHeight: 0
  },

  lifetimes: {
    attached() {
      // 获取状态栏高度
      const systemInfo = wx.getSystemInfoSync();
      this.setData({
        statusBarHeight: systemInfo.statusBarHeight || 0
      });
    }
  },

  methods: {
    // 返回上一页
    onBack() {
      const pages = getCurrentPages();
      if (pages.length > 1) {
        wx.navigateBack({
          delta: 1
        });
      } else {
        // 如果是第一页，返回首页
        wx.reLaunch({
          url: '/pages/index/index'
        });
      }
    },

    // 返回首页
    onHome() {
      wx.reLaunch({
        url: '/pages/index/index'
      });
    }
  }
});
