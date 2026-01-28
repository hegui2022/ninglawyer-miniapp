// 码上签约 - 首页（补充完整）
Page({
  data: {
    banners: [
      {
        id: 1,
        image: '/assets/images/banner1.png',
        title: '智能签约，高效便捷'
      },
      {
        id: 2,
        image: '/assets/images/banner2.png',
        title: '法律保障，安全可靠'
      }
    ],
    quickActions: [
      {
        id: 1,
        icon: '/assets/icons/contract-create.png',
        title: '创建合同',
        page: '/pages/create/create'
      },
      {
        id: 2,
        icon: '/assets/icons/sign.png',
        title: '待签署',
        page: '/pages/sign/sign'
      },
      {
        id: 3,
        icon: '/assets/icons/record.png',
        title: '签署记录',
        page: '/pages/record/record'
      },
      {
        id: 4,
        icon: '/assets/icons/template.png',
        title: '合同模板',
        page: '/pages/template/template'
      }
    ],
    recentContracts: [],
    stats: {
      total: 0,
      pending: 0,
      completed: 0
    }
  },
  
  onLoad() {
    this.loadStats();
    this.loadRecentContracts();
  },
  
  onShow() {
    this.loadStats();
    this.loadRecentContracts();
  },
  
  onBannerChange(e) {
    this.setData({
      currentBanner: e.detail.current
    });
  },
  
  loadStats() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/stats',
      method: 'GET',
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            stats: res.data.data
          });
        }
      }
    });
  },
  
  loadRecentContracts() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/recent',
      method: 'GET',
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            recentContracts: res.data.data
          });
        }
      }
    });
  },
  
  onQuickAction(e) {
    const action = e.currentTarget.dataset.action;
    wx.navigateTo({
      url: action.page
    });
  },
  
  onContractDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },
  
  onCreateContract() {
    wx.navigateTo({
      url: '/pages/create/create'
    });
  }
});
