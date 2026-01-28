// 防风险 - 首页
Page({
  data: {
    riskLevel: 'unknown',
    score: 0,
    categories: [
      { id: 'contract', name: '合同风险', checked: false },
      { id: 'labor', name: '劳动风险', checked: false },
      { id: 'company', name: '公司治理', checked: false },
      { id: 'ip', name: '知识产权', checked: false },
      { id: 'compliance', name: '合规风险', checked: false }
    ],
    analyzing: false,
    result: null
  },
  
  onLoad() {
    this.loadRiskProfile();
  },
  
  loadRiskProfile() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/risk/profile',
      method: 'GET',
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            riskLevel: res.data.data.level,
            score: res.data.data.score
          });
        }
      }
    });
  },
  
  onCategoryChange(e) {
    const categories = this.data.categories.map(cat => ({
      ...cat,
      checked: cat.id === e.detail.value
    }));
    this.setData({ categories });
  },
  
  onAnalyze() {
    const selected = this.data.categories.find(c => c.checked);
    if (!selected) {
      wx.showToast({
        title: '请选择风险类型',
        icon: 'none'
      });
      return;
    }
    
    this.setData({ analyzing: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/risk/analyze',
      method: 'POST',
      data: {
        category: selected.id
      },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            result: res.data.data,
            analyzing: false
          });
        }
      },
      fail: () => {
        this.setData({ analyzing: false });
        wx.showToast({
          title: '分析失败',
          icon: 'none'
        });
      }
    });
  },
  
  onDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/detail/detail?id=' + id
    });
  }
});
