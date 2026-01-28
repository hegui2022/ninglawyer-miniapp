// components/tab-bar/tab-bar.js
Component({
  properties: {
    currentPath: {
      type: String,
      value: ''
    }
  },

  data: {
    tabs: [
      {
        pagePath: '/pages/obligation/obligation',
        text: '义务',
        icon: '📜'
      },
      {
        pagePath: '/pages/manage/manage',
        text: '管理',
        icon: '⚙️'
      },
      {
        pagePath: '/pages/discover/discover',
        text: '发现',
        icon: '🔍'
      },
      {
        pagePath: '/pages/profile/profile',
        text: '我的',
        icon: '👤'
      }
    ]
  },

  methods: {
    switchTab(e) {
      const path = e.currentTarget.dataset.path;

      if (path === this.data.currentPath) {
        return;
      }

      wx.switchTab({
        url: path
      });
    }
  }
});
