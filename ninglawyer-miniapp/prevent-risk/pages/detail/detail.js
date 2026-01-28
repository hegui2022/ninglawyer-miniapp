// 防风险 - 详情页
Page({
  data: {
    riskId: '',
    riskInfo: null,
    suggestions: []
  },
  
  onLoad(options) {
    const id = options.id;
    this.setData({ riskId: id });
    this.loadRiskDetail();
  },
  
  loadRiskDetail() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/risk/detail',
      method: 'GET',
      data: { id: this.data.riskId },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            riskInfo: res.data.data,
            suggestions: res.data.data.suggestions || []
          });
        }
      }
    });
  },
  
  onImplementSuggestion(e) {
    const index = e.currentTarget.dataset.index;
    wx.showToast({
      title: '已采纳建议',
      icon: 'success'
    });
  }
});
