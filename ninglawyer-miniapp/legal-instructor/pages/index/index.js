// 法律教官 - 首页
Page({
  data: {
    banners: [
      {
        id: 1,
        image: '/assets/images/banner1.png',
        title: '宁律师 - 您的专属法律顾问'
      },
      {
        id: 2,
        image: '/assets/images/banner2.png',
        title: '专业法律服务，随时随地'
      },
      {
        id: 3,
        image: '/assets/images/banner3.png',
        title: '7大领域，全方位保障'
      }
    ],
    services: [
      {
        id: 1,
        icon: '/assets/icons/consult.png',
        title: '法律咨询',
        description: '在线咨询专业律师',
        url: '/pages/consult/consult'
      },
      {
        id: 2,
        icon: '/assets/icons/contract.png',
        title: '合同服务',
        description: '起草、审查、管理',
        url: '/pages/contract/contract'
      },
      {
        id: 3,
        icon: '/assets/icons/sign.png',
        title: '电子签约',
        description: '便捷高效的签署',
        url: '/pages/sign/sign'
      },
      {
        id: 4,
        icon: '/assets/icons/judge.png',
        title: '案例查询',
        description: '海量案例库',
        url: '/pages/case/case'
      }
    ],
    stats: {
      users: 128000,
      consultations: 896000,
      satisfaction: 99.2
    },
    currentBanner: 0
  },
  
  onLoad() {
    this.loadStats();
  },
  
  // 轮播图切换
  onBannerChange(e) {
    this.setData({
      currentBanner: e.detail.current
    });
  },
  
  // 加载统计数据
  loadStats() {
    // 这里可以从服务器获取统计数据
  },
  
  // 点击服务
  onServiceTap(e) {
    const url = e.currentTarget.dataset.url;
    if (url) {
      wx.navigateTo({
        url: url,
        fail: () => {
          wx.showToast({
            title: '功能开发中',
            icon: 'none'
          });
        }
      });
    }
  },
  
  // 跳转宁律师家族
  onGoLawyerFamily() {
    wx.navigateTo({
      url: '/pages/lawyer-family/lawyer-family'
    });
  },
  
  // 跳转咨询
  onGoConsult() {
    wx.navigateTo({
      url: '/pages/consult/consult'
    });
  }
});
