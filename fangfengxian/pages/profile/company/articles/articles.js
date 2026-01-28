// pages/profile/company/articles/articles.js
Page({
  data: {
    companyName: '',
    registeredCapital: '',
    address: ''
  },

  onLoad(options) {
    console.log('Articles page loaded', options);
  },

  goBack() {
    wx.navigateBack();
  },

  // 公司名称输入
  onCompanyNameInput(e) {
    this.setData({
      companyName: e.detail.value
    });
  },

  // 注册资本输入
  onCapitalInput(e) {
    this.setData({
      registeredCapital: e.detail.value
    });
  },

  // 住所地输入
  onAddressInput(e) {
    this.setData({
      address: e.detail.value
    });
  },

  // 识别执照
  recognizeLicense() {
    console.log('Recognize license');
    wx.showToast({
      title: '识别执照',
      icon: 'none',
      duration: 1500
    });

    // 实际应该调用拍照或选择图片接口
    // wx.chooseImage({
    //   count: 1,
    //   sizeType: ['compressed'],
    //   sourceType: ['album', 'camera'],
    //   success: (res) => {
    //     // 上传图片进行OCR识别
    //   }
    // });
  },

  // 跳转到详情
  goToDetail(e) {
    const type = e.currentTarget.dataset.type;
    console.log('Go to detail:', type);

    const typeNames = {
      shareholders: '股东会',
      board: '董事会',
      supervisor: '监事会'
    };

    wx.showToast({
      title: `查看${typeNames[type]}`,
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到详情页面
    // wx.navigateTo({
    //   url: `/pages/${type}/${type}`
    // });
  },

  // 跳转到议事规则
  goToRules() {
    console.log('Go to rules');
    wx.showToast({
      title: '议事规则',
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到议事规则页面
    // wx.navigateTo({
    //   url: '/pages/rules/rules'
    // });
  },

  onShareAppMessage() {
    return {
      title: '公司章程',
      path: '/pages/profile/company/articles/articles'
    };
  }
});
