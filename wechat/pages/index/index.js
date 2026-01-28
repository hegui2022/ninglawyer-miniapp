// pages/index/index.js
const app = getApp();

Page({
  data: {},

  onLoad() {
    console.log('首页加载');
  },

  // 跳转到合同起草页面
  goToDraft() {
    wx.navigateTo({
      url: '/pages/contract-draft/contract-draft'
    });
  },

  // 跳转到合同审查页面
  goToReview() {
    wx.navigateTo({
      url: '/pages/contract-list/contract-list'
    });
  },

  // 跳转到合同列表页面
  goToList() {
    wx.switchTab({
      url: '/pages/contract-list/contract-list'
    });
  },

  // 跳转到法律咨询页面（暂未实现）
  goToConsult() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    });
  },

  // 快速创建合同
  quickCreateContract(type) {
    wx.navigateTo({
      url: `/pages/contract-draft/contract-draft?type=${type}`
    });
  }
});
