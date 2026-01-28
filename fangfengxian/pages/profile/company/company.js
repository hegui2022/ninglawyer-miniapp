// pages/profile/company/company.js
Page({
  data: {
    basicExpanded: true // 基础合规默认展开
  },

  onLoad(options) {
    console.log('Company page loaded', options);
  },

  // 切换分类展开/收起
  toggleCategory(e) {
    const category = e.currentTarget.dataset.category;
    console.log('Toggle category:', category);

    if (category === 'basic') {
      this.setData({
        basicExpanded: !this.data.basicExpanded
      });
    }
  },

  // 跳转到详情
  goToDetail(e) {
    const item = e.currentTarget.dataset.item;
    console.log('Go to detail:', item);

    if (item === 'procurement') {
      // 跳转到采购合规页面
      wx.navigateTo({
        url: '/pages/profile/company/procurement-compliance/procurement-compliance'
      });
      return;
    }

    const itemNames = {
      qualification: '资格资质合规',
      governance: '企业治理合规',
      finance: '财务合规',
      labor: '劳动用工合规'
    };

    wx.showToast({
      title: `查看${itemNames[item]}`,
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到详情页面
    // wx.navigateTo({
    //   url: `/pages/compliance/detail?item=${item}`
    // });
  },

  // 跳转到数据合规页面
  goToDataCompliance() {
    wx.navigateTo({
      url: '/pages/profile/company/data-compliance/data-compliance'
    });
  },

  // 跳转到功能
  goToFunction(e) {
    const type = e.currentTarget.dataset.type;
    console.log('Go to function:', type);

    const typeNames = {
      audit: '合规审计',
      training: '合规培训',
      culture: '合规文化'
    };

    wx.showToast({
      title: `打开${typeNames[type]}`,
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到对应功能页面
    // wx.navigateTo({
    //   url: `/pages/${type}/${type}`
    // });
  },

  // 跳转到搭建页面
  goToBuild() {
    console.log('Go to build');
    wx.showToast({
      title: '合规体系搭建',
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到搭建页面
    // wx.navigateTo({
    //   url: '/pages/build/build'
    // });
  },

  onShareAppMessage() {
    return {
      title: '我的公司',
      path: '/pages/profile/company/company'
    };
  }
});
