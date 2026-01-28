// pages/contract-list/contract-list.js
const app = getApp();

Page({
  data: {
    contracts: [],
    filterType: 'all',
    loading: false,
  },

  onLoad() {
    this.loadContracts();
  },

  onShow() {
    // 页面显示时刷新列表
    this.loadContracts();
  },

  // 加载合同列表
  loadContracts() {
    this.setData({ loading: true });

    app.request({
      url: '/contract/list',
      method: 'GET',
      data: {
        status: this.data.filterType === 'all' ? '' : this.data.filterType,
        limit: 50
      },
      success: (res) => {
        if (res.code === 0 && res.data) {
          // 格式化合同类型名称
          const contracts = res.data.map(contract => ({
            ...contract,
            contract_type_name: this.getContractTypeName(contract.contract_type),
            created_at: this.formatDate(contract.created_at)
          }));

          this.setData({ contracts });
        }
      },
      fail: (err) => {
        console.error('加载合同列表失败', err);
      },
      complete: () => {
        this.setData({ loading: false });
      }
    });
  },

  // 设置筛选条件
  setFilter(type) {
    this.setData({ filterType: type });
    this.loadContracts();
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
