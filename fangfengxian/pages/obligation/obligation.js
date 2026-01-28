// pages/obligation/obligation.js
Page({
  onLoad(options) {
    console.log('Obligation page loaded');
  },

  onShareAppMessage() {
    return {
      title: '义务',
      path: '/pages/obligation/obligation'
    };
  }
});
