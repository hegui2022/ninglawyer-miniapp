// 怎么判小程序 - 首页
Page({
  data: {
    hotCases: [],
    categories: [
      {
        id: 'civil',
        name: '民事纠纷',
        icon: '/assets/icons/civil.png',
        count: 12800
      },
      {
        id: 'criminal',
        name: '刑事辩护',
        icon: '/assets/icons/criminal.png',
        count: 8600
      },
      {
        id: 'contract',
        name: '合同纠纷',
        icon: '/assets/icons/contract.png',
        count: 15600
      },
      {
        id: 'labor',
        name: '劳动争议',
        icon: '/assets/icons/labor.png',
        count: 9200
      },
      {
        id: 'property',
        name: '房产纠纷',
        icon: '/assets/icons/property.png',
        count: 6800
      },
      {
        id: 'marriage',
        name: '婚姻家庭',
        icon: '/assets/icons/marriage.png',
        count: 11200
      }
    ],
    recentCases: []
  },
  
  onLoad() {
    this.loadHotCases();
    this.loadRecentCases();
  },
  
  // 加载热门案例
  loadHotCases() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/case/hot',
      method: 'GET',
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            hotCases: res.data.data
          });
        }
      }
    });
  },
  
  // 加载最近案例
  loadRecentCases() {
    wx.request({
      url: getApp().globalData.config.apiUrl + '/case/recent',
      method: 'GET',
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            recentCases: res.data.data
          });
        }
      }
    });
  },
  
  // 分类点击
  onCategoryClick(e) {
    const category = e.currentTarget.dataset.category;
    wx.navigateTo({
      url: `/pages/search/search?category=${category.id}`
    });
  },
  
  // 查看案例详情
  onCaseDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },
  
  // 快速查询
  onQuickSearch() {
    wx.navigateTo({
      url: '/pages/search/search'
    });
  },
  
  // 智能分析
  onAnalyze() {
    wx.switchTab({
      url: '/pages/analyze/analyze'
    });
  }
});
