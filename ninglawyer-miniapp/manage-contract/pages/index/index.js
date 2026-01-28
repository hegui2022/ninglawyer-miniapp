// 理约小程序 - 首页
Page({
  data: {
    stats: {
      total: 0,
      active: 0,
      expiring: 0,
      completed: 0
    },
    upcomingDeadlines: [],
    recentActivities: [],
    chartData: null
  },
  
  onLoad() {
    this.loadStats();
    this.loadUpcomingDeadlines();
    this.loadRecentActivities();
  },
  
  onShow() {
    this.loadStats();
  },
  
  // 加载统计数据
  loadStats() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/stats',
      method: 'GET',
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            stats: res.data.data
          });
        }
      }
    });
  },
  
  // 加载即将到期的合同
  loadUpcomingDeadlines() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/expiring',
      method: 'GET',
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            upcomingDeadlines: res.data.data
          });
        }
      }
    });
  },
  
  // 加载最近活动
  loadRecentActivities() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/activity/recent',
      method: 'GET',
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            recentActivities: res.data.data
          });
        }
      }
    });
  },
  
  // 查看合同详情
  onContractDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },
  
  // 跳转到提醒页面
  onGoReminder() {
    wx.switchTab({
      url: '/pages/reminder/reminder'
    });
  },
  
  // 跳转到合同列表
  onGoList() {
    wx.switchTab({
      url: '/pages/list/list'
    });
  },
  
  // 跳转到履约页面
  onGoPerformance() {
    wx.switchTab({
      url: '/pages/performance/performance'
    });
  }
});
