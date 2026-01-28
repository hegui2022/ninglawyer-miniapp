// pages/profile/company/data-compliance/data-compliance.js
Page({
  onLoad(options) {
    console.log('Data compliance page loaded', options);
  },

  goBack() {
    wx.navigateBack();
  },

  // 跳转到清单
  goToList(e) {
    const list = e.currentTarget.dataset.list;
    console.log('Go to list:', list);

    const listNames = {
      risk: '风险清单',
      system: '制度清单'
    };

    wx.showToast({
      title: `查看${listNames[list]}`,
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到清单页面
    // wx.navigateTo({
    //   url: `/pages/list/list?type=${list}`
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
      'data-collection': '数据收集',
      'procurement-application': '采购申请',
      'data-security': '数据安全管理制度',
      'data-asset': '数据资产管理（分类分级）制度',
      'data-incident': '数据安全事件管理制度'
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
      title: '数据合规',
      path: '/pages/profile/company/data-compliance/data-compliance'
    };
  }
});
