// 码上签约 - 签署页
Page({
  data: {
    contractId: '',
    contract: null,
    signing: false,
    signatureImage: ''
  },
  
  onLoad(options) {
    const id = options.id;
    this.setData({ contractId: id });
    this.loadContract();
  },
  
  loadContract() {
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
  
  onChooseSignature() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePath = res.tempFilePaths[0];
        this.setData({ signatureImage: tempFilePath });
      }
    });
  },
  
  onSign() {
    if (!this.data.signatureImage) {
      wx.showToast({
        title: '请先上传签名',
        icon: 'none'
      });
      return;
    }
    
    this.setData({ signing: true });
    
    wx.uploadFile({
      url: getApp().globalData.config.apiUrl + '/contract/sign',
      filePath: this.data.signatureImage,
      name: 'signature',
      formData: {
        contract_id: this.data.contractId
      },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        const data = JSON.parse(res.data);
        if (data.code === 200) {
          wx.showToast({
            title: '签署成功',
            icon: 'success'
          });
          setTimeout(() => {
            wx.navigateBack();
          }, 1500);
        }
      },
      fail: () => {
        wx.showToast({
          title: '签署失败',
          icon: 'none'
        });
      },
      complete: () => {
        this.setData({ signing: false });
      }
    });
  }
});
