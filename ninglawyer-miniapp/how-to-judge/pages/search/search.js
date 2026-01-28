// 怎么判小程序 - 搜索页面
Page({
  data: {
    searchKeyword: '',
    searchHistory: [],
    hotKeywords: [
      '合同纠纷',
      '离婚',
      '交通事故',
      '劳动争议',
      '刑事辩护',
      '房产纠纷'
    ],
    searchResults: [],
    searching: false
  },
  
  onLoad() {
    this.loadSearchHistory();
  },
  
  // 加载搜索历史
  loadSearchHistory() {
    const history = wx.getStorageSync('searchHistory') || [];
    this.setData({
      searchHistory: history
    });
  },
  
  // 搜索输入
  onSearchInput(e) {
    this.setData({
      searchKeyword: e.detail.value
    });
  },
  
  // 执行搜索
  onSearch() {
    if (!this.data.searchKeyword.trim()) {
      return;
    }
    
    this.setData({ searching: true });
    
    // 保存搜索历史
    let history = this.data.searchHistory;
    history = history.filter(item => item !== this.data.searchKeyword);
    history.unshift(this.data.searchKeyword);
    history = history.slice(0, 10);
    wx.setStorageSync('searchHistory', history);
    this.setData({ searchHistory: history });
    
    // 执行搜索
    wx.request({
      url: getApp().globalData.config.apiUrl + '/case/search',
      method: 'GET',
      data: {
        keyword: this.data.searchKeyword
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            searchResults: res.data.data,
            searching: false
          });
        }
      },
      fail: () => {
        this.setData({ searching: false });
      }
    });
  },
  
  // 点击历史关键词
  onHistoryKeyword(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ searchKeyword: keyword });
    this.onSearch();
  },
  
  // 点击热门关键词
  onHotKeyword(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ searchKeyword: keyword });
    this.onSearch();
  },
  
  // 清除搜索历史
  onClearHistory() {
    wx.showModal({
      title: '提示',
      content: '确定清除搜索历史吗？',
      success: (res) => {
        if (res.confirm) {
          wx.removeStorageSync('searchHistory');
          this.setData({ searchHistory: [] });
        }
      }
    });
  },
  
  // 查看案例详情
  onCaseDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  }
});
