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
        pagePath: '/pages/guide/guide',
        text: '指引',
        icon: '📋'
      },
      {
        pagePath: '/pages/manage/manage',
        text: '管理',
        icon: '⚙️'
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
