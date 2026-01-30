// 合同预览页面
Page({
  data: {
    contract: null
  },
  
  onLoad(options) {
    if (options.content) {
      const contract = JSON.parse(decodeURIComponent(options.content));
      this.setData({ contract });
    }
  },
  
  onEdit() {
    const contract = this.data.contract;
    const content = encodeURIComponent(JSON.stringify(contract));
    
    wx.navigateBack();
  },
  
  onSign() {
    const contract = this.data.contract;
    const content = encodeURIComponent(JSON.stringify(contract));
    
    wx.redirectTo({
      url: `/pages/sign/sign?content=${content}`
    });
  },
  
  onShare() {
    wx.showShareMenu({
      withShareTicket: true
    });
  }
});
