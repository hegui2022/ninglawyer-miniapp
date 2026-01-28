// pages/profile/profile.js
Page({
  onLoad(options) {
    console.log('Profile page loaded');
  },

  onShareAppMessage() {
    return {
      title: '我的',
      path: '/pages/profile/profile'
    };
  }
});
