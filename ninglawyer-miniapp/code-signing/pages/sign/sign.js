// 码上签约小程序 - 签署页面
Page({
  data: {
    pendingList: [],
    signingList: [],
    currentTab: 0,
    loading: false
  },
  
  onLoad() {
    this.loadPendingContracts();
  },
  
  onShow() {
    this.loadPendingContracts();
  },
  
  onTabChange(e) {
    this.setData({
      currentTab: e.detail.index
    });
    
    if (e.detail.index === 0) {
      this.loadPendingContracts();
    } else {
      this.loadSigningContracts();
    }
  },
  
  // 加载待签署合同
  loadPendingContracts() {
    this.setData({ loading: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/pending',
      method: 'GET',
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            pendingList: res.data.data,
            loading: false
          });
        }
      },
      fail: () => {
        this.setData({ loading: false });
      }
    });
  },
  
  // 加载签署中合同
  loadSigningContracts() {
    this.setData({ loading: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/signing',
      method: 'GET',
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            signingList: res.data.data,
            loading: false
          });
        }
      },
      fail: () => {
        this.setData({ loading: false });
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
  
  // 签署合同
  onSignContract(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/sign/signature?id=${id}`
    });
  }
});
