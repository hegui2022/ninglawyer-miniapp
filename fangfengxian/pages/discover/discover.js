// pages/discover/discover.js
Page({
  onLoad(options) {
    console.log('Discover page loaded');
  },

  onShareAppMessage() {
    return {
      title: '发现',
      path: '/pages/discover/discover'
    };
  }
});
