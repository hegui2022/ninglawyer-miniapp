// pages/profile/profile.js
Page({
  onLoad(options) {
    console.log('Profile page loaded');
  },

  // 跳转到理约上海
  goToBooking() {
    console.log('Go to booking');
    wx.showToast({
      title: '理约上海',
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到预约页面
    // wx.navigateTo({
    //   url: '/pages/booking/booking'
    // });
  },

  // 跳转到功能页面
  goToFunction(e) {
    const type = e.currentTarget.dataset.type;
    console.log('Go to function:', type);

    const typeNames = {
      company: '我的公司',
      position: '我的岗位'
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
      title: '我的',
      path: '/pages/profile/profile'
    };
  }
});
