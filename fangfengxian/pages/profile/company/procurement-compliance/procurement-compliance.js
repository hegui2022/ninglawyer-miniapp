// pages/profile/company/procurement-compliance/procurement-compliance.js
Page({
  onLoad(options) {
    console.log('Procurement compliance page loaded', options);
  },

  goBack() {
    wx.navigateBack();
  },

  // 跳转到搜索
  goToSearch() {
    console.log('Go to search');
    wx.showToast({
      title: '采购风险识别',
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到搜索页面
    // wx.navigateTo({
    //   url: '/pages/search/search'
    // });
  },

  // 跳转到详情
  goToDetail(e) {
    const item = e.currentTarget.dataset.item;
    console.log('Go to detail:', item);

    const itemNames = {
      'must-comply': '企业必须遵守',
      'promise-comply': '企业承诺遵守',
      'review-power': '审核权',
      'procurement-power': '采购权',
      'confirm-requirement': '确认需求',
      'procurement-application': '采购申请'
    };

    wx.showToast({
      title: `查看${itemNames[item]}`,
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到详情页面
    // wx.navigateTo({
    //   url: `/pages/detail/detail?item=${item}`
    // });
  },

  onShareAppMessage() {
    return {
      title: '采购合规',
      path: '/pages/profile/company/procurement-compliance/procurement-compliance'
    };
  }
});
