// 法律教官 - 个人中心页
Page({
  data: {
    userInfo: null,
    unreadCount: 2,
    serviceList: [
      { id: 'notification', name: '消息通知', icon: '🔔', hasBadge: true },
      { id: 'history', name: '咨询历史', icon: '📋' },
      { id: 'contracts', name: '我的合同', icon: '📝' },
      { id: 'statistics', name: '数据统计', icon: '📊' },
      { id: 'collection', name: '我的收藏', icon: '⭐' },
      { id: 'settings', name: '设置', icon: '⚙️' }
    ]
  },
  
  onLoad() {
    this.loadUserInfo();
  },
  
  loadUserInfo() {
    const userInfo = wx.getStorageSync('userInfo');
    this.setData({ userInfo });
  },
  
  onServiceTap(e) {
    const id = e.currentTarget.dataset.id;
    if (id === 'notification') {
      wx.navigateTo({
        url: '/pages/notification/notification'
      });
    } else if (id === 'statistics') {
      wx.navigateTo({
        url: '/pages/statistics/statistics'
      });
    } else {
      wx.showToast({
        title: '功能开发中',
        icon: 'none'
      });
    }
  },
  
  onLogout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync();
          wx.reLaunch({
            url: '/pages/index/index'
          });
        }
      }
    });
  }
});
