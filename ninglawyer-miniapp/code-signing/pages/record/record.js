// 码上签约 - 签署记录页
Page({
  data: {
    recordList: [],
    loading: false
  },
  
  onLoad() {
    this.loadRecords();
  },
  
  loadRecords() {
    this.setData({ loading: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/sign-records',
      method: 'GET',
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            recordList: res.data.data || []
          });
        }
      },
      complete: () => {
        this.setData({ loading: false });
      }
    });
  },
  
  onViewDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/detail/detail?id=' + id
    });
  },
  
  onRefresh() {
    this.loadRecords();
  }
});
