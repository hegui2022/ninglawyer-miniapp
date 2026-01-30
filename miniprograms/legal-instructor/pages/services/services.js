// 法律教官 - 服务列表页
Page({
  data: {
    categories: [
      { id: 'all', name: '全部' },
      { id: 'consultation', name: '咨询' },
      { id: 'contract', name: '合同' },
      { id: 'litigation', name: '诉讼' },
      { id: 'other', name: '其他' }
    ],
    currentCategory: 'all',
    serviceList: []
  },
  
  onLoad() {
    this.loadServices();
  },
  
  onCategoryChange(e) {
    const category = e.currentTarget.dataset.category;
    this.setData({ currentCategory: category });
    this.loadServices();
  },
  
  loadServices() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/services',
      method: 'GET',
      data: {
        category: this.data.currentCategory
      },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({ serviceList: res.data.data || [] });
        }
      }
    });
  },
  
  onServiceTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/service-detail/service-detail?id=' + id
    });
  }
});
