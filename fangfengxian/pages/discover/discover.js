// pages/discover/discover.js
Page({
  onLoad(options) {
    console.log('Discover page loaded');
  },

  // 跳转到功能页面
  goToFunction(e) {
    const type = e.currentTarget.dataset.type;
    console.log('Go to function:', type);

    const typeNames = {
      regulation: '行业监管动态',
      training: '合规培训',
      message: '消息',
      contract: '合同场景师'
    };

    wx.showToast({
      title: `打开${typeNames[type]}`,
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到对应功能页面
    // wx.navigateTo({
    //   url: `/pages/${type}/${type}`
    // });
  },

  onShareAppMessage() {
    return {
      title: '发现',
      path: '/pages/discover/discover'
    };
  }
});
