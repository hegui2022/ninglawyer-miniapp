// 理约小程序 - 履约跟踪页面
Page({
  data: {
    performanceList: [],
    stats: {
      onTrack: 0,
      delayed: 0,
      risk: 0
    },
    loading: false
  },
  
  onLoad() {
    this.loadStats();
    this.loadPerformanceList();
  },
  
  onShow() {
    this.loadStats();
    this.loadPerformanceList();
  },
  
  // 加载统计数据
  loadStats() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/performance/stats',
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
  
  // 加载履约列表
  loadPerformanceList() {
    this.setData({ loading: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/performance/list',
      method: 'GET',
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            performanceList: res.data.data,
            loading: false
          });
        }
      },
      fail: () => {
        this.setData({ loading: false });
      }
    });
  },
  
  // 更新履约状态
  onUpdateStatus(e) {
    const contractId = e.currentTarget.dataset.id;
    const status = e.currentTarget.dataset.status;
    
    wx.showActionSheet({
      itemList: ['正常', '延期', '风险'],
      success: (res) => {
        const statuses = ['normal', 'delayed', 'risk'];
        const selectedStatus = statuses[res.tapIndex];
        
        wx.request({
          url: getApp().globalData.config.apiUrl + '/contract/performance/status',
          method: 'POST',
          data: {
            contractId: contractId,
            status: selectedStatus
          },
          header: {
            'Authorization': wx.getStorageSync('token')
          },
          success: () => {
            wx.showToast({
              title: '更新成功',
              icon: 'success'
            });
            this.loadPerformanceList();
            this.loadStats();
          }
        });
      }
    });
  },
  
  // 查看履约详情
  onDetail(e) {
    const contractId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/performance/detail?id=${contractId}`
    });
  }
});
