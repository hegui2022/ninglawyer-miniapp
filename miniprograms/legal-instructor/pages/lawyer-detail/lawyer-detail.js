// 法律教官 - 律师详情页
Page({
  data: {
    lawyerId: '',
    lawyer: null
  },
  
  onLoad(options) {
    const id = options.id;
    this.setData({ lawyerId: id });
    this.loadLawyerDetail();
  },
  
  loadLawyerDetail() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/consultation/lawyer-detail',
      method: 'GET',
      data: { id: this.data.lawyerId },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({ lawyer: res.data.data });
        }
      }
    });
  },
  
  onStartConsultation() {
    wx.navigateTo({
      url: '/pages/chat/chat?lawyerId=' + this.data.lawyerId
    });
  },
  
  onShareAppMessage() {
    return {
      title: this.data.lawyer ? this.data.lawyer.name + ' - 宁律师' : '宁律师',
      path: '/pages/lawyer-detail/lawyer-detail?id=' + this.data.lawyerId
    };
  }
});
