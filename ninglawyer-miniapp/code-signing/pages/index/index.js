// 码上签约小程序 - 首页
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
      },
      {
        id: 3,
        image: '/assets/images/banner3.png',
        title: '电子签名，即时生效'
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
    },
    currentBanner: 0
  },
  
  onLoad() {
    this.loadStats();
    this.loadRecentContracts();
  },
  
  onShow() {
    this.loadStats();
    this.loadRecentContracts();
  },
  
  onShareAppMessage() {
    return {
      title: '码上签约 - 智能电子签约',
      path: '/pages/index/index'
    };
  },
  
  // 轮播图切换
  onBannerChange(e) {
    this.setData({
      currentBanner: e.detail.current
    });
  },
  
  // 加载统计数据
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
  
  // 加载最近合同
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
  
  // 快捷操作点击
  onQuickAction(e) {
    const action = e.currentTarget.dataset.action;
    wx.navigateTo({
      url: action.page
    });
  },
  
  // 查看合同详情
  onContractDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },
  
  // 创建合同
  onCreateContract() {
    wx.navigateTo({
      url: '/pages/create/create'
    });
  },
  
  // 查看全部
  onViewAll() {
    wx.switchTab({
      url: '/pages/record/record'
    });
  }
});
