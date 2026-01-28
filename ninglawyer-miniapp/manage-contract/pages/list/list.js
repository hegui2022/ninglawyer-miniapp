// 理约小程序 - 合同列表页面
Page({
  data: {
    contractList: [],
    filterType: 'all',
    searchKeyword: '',
    loading: false,
    hasMore: true,
    page: 1
  },
  
  onLoad() {
    this.loadContracts();
  },
  
  onShow() {
    this.setData({
      page: 1,
      contractList: [],
      hasMore: true
    });
    this.loadContracts();
  },
  
  // 加载合同列表
  loadContracts() {
    if (this.data.loading || !this.data.hasMore) return;
    
    this.setData({ loading: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/list',
      method: 'GET',
      data: {
        type: this.data.filterType,
        keyword: this.data.searchKeyword,
        page: this.data.page,
        pageSize: 20
      },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          const newList = res.data.data.list || [];
          this.setData({
            contractList: [...this.data.contractList, ...newList],
            hasMore: newList.length >= 20,
            loading: false
          });
        }
      },
      fail: () => {
        this.setData({ loading: false });
      }
    });
  },
  
  // 筛选类型切换
  onFilterChange(e) {
    const type = e.currentTarget.dataset.type;
    this.setData({
      filterType: type,
      page: 1,
      contractList: [],
      hasMore: true
    });
    this.loadContracts();
  },
  
  // 搜索
  onSearch(e) {
    const keyword = e.detail.value;
    this.setData({
      searchKeyword: keyword,
      page: 1,
      contractList: [],
      hasMore: true
    });
    this.loadContracts();
  },
  
  // 触底加载更多
  onReachBottom() {
    this.setData({
      page: this.data.page + 1
    });
    this.loadContracts();
  },
  
  // 查看详情
  onContractDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  }
});
