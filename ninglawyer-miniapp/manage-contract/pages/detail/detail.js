// 理约 - 合同详情页
Page({
  data: {
    contractId: '',
    contract: null
  },
  
  onLoad(options) {
    const id = options.id;
    this.setData({ contractId: id });
    this.loadContractDetail();
  },
  
  loadContractDetail() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/detail',
      method: 'GET',
      data: { id: this.data.contractId },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({ contract: res.data.data });
        }
      }
    });
  },
  
  onEdit() {
    wx.navigateTo({
      url: '/pages/edit/edit?id=' + this.data.contractId
    });
  },
  
  onDelete() {
    wx.showModal({
      title: '提示',
      content: '确定要删除该合同吗？',
      success: (res) => {
        if (res.confirm) {
          wx.request({
            url: getApp().globalData.config.apiUrl + '/contract/delete',
            method: 'POST',
            data: { id: this.data.contractId },
            header: {
              'Authorization': wx.getStorageSync('token')
            },
            success: () => {
              wx.showToast({
                title: '删除成功',
                icon: 'success'
              });
              setTimeout(() => {
                wx.navigateBack();
              }, 1500);
            }
          });
        }
      }
    });
  }
});
