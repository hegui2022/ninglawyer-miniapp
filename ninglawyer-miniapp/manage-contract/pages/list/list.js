// 理约 - 合同列表页面
Page({
  data: {
    contractList: [],
    filterType: 'all',
    searchKeyword: '',
    loading: false,
    page: 1,
    hasMore: true
  },
  
  onLoad() {
    this.loadContracts();
  },
  
  loadContracts() {
    this.setData({ loading: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/list',
      method: 'GET',
      data: {
        type: this.data.filterType,
        page: this.data.page
      },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          const newList = res.data.data.list || [];
          this.setData({
            contractList: [...this.data.contractList, ...newList],
            hasMore: newList.length >= 20,
            loading: false
          });
        }
      },
      fail: () => {
        this.setData({ loading: false });
      }
    });
  },
  
  onContractDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  }
});
