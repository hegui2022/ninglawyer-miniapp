// pages/contract-list/contract-list.js
const app = getApp();

Page({
  data: {
    contracts: [],
    filterType: 'all',
    loading: false,
    pagination: {
      page: 1,
      page_size: 10,
      total: 0,
      total_pages: 0,
      has_more: true
    }
  },

  onLoad() {
    this.loadContracts(true);
  },

  onShow() {
    // 页面显示时刷新列表
    this.refreshContracts();
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.refreshContracts();
  },

  // 上拉加载更多
  onReachBottom() {
    if (this.data.pagination.has_more && !this.data.loading) {
      this.loadContracts(false);
    }
  },

  // 刷新列表
  refreshContracts() {
    this.setData({
      pagination: {
        page: 1,
        page_size: 10,
        total: 0,
        total_pages: 0,
        has_more: true
      }
    });
    this.loadContracts(true);
  },

  // 加载合同列表
  loadContracts(isRefresh = false) {
    this.setData({ loading: true });

    app.request({
      url: '/contract/list',
      method: 'GET',
      data: {
        status: this.data.filterType === 'all' ? '' : this.data.filterType,
        page: this.data.pagination.page,
        page_size: this.data.pagination.page_size
      },
      success: (res) => {
        if (res.code === 0 && res.data) {
          const { contracts, pagination } = res.data;
          
          // 格式化合同数据
          const formattedContracts = contracts.map(contract => ({
            ...contract,
            contract_type_name: this.getContractTypeName(contract.contract_type),
            created_at: this.formatDate(contract.created_at)
          }));

          // 合并或替换数据
          const newContracts = isRefresh ? formattedContracts : [...this.data.contracts, ...formattedContracts];
          
          this.setData({
            contracts: newContracts,
            pagination: pagination
          });
        }
      },
      fail: (err) => {
        console.error('加载合同列表失败', err);
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        });
      },
      complete: () => {
        this.setData({ loading: false });
        
        // 停止下拉刷新
        if (isRefresh) {
          wx.stopPullDownRefresh();
        }
      }
    });
  },

  // 设置筛选条件
  setFilter(type) {
    if (this.data.filterType === type) return;
    
    this.setData({ filterType: type });
    this.refreshContracts();
  },

  // 跳转到合同详情
  goToDetail(id) {
    wx.navigateTo({
      url: `/pages/contract-detail/contract-detail?id=${id}`
    });
  },

  // 跳转到起草页面
  goToDraft() {
    wx.navigateTo({
      url: '/pages/contract-draft/contract-draft'
    });
  },

  // 跳转到模板库
  goToTemplates() {
    wx.navigateTo({
      url: '/pages/template-list/template-list'
    });
  },

  // 获取合同类型名称
  getContractTypeName(type) {
    const typeMap = {
      'standard': '标准劳动合同',
      'parttime': '非全日制用工合同',
      'intern': '实习协议',
      'retired': '退休返聘协议',
      'project': '项目制合同',
      'dispatch': '劳务派遣合同'
    };
    return typeMap[type] || type;
  },

  // 格式化日期
  formatDate(dateStr) {
    const date = new Date(dateStr);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
});
