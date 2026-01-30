// 合同列表页面
Page({
  data: {
    contracts: [],
    filteredContracts: [],
    currentTab: 'all',
    tabs: [
      { id: 'all', name: '全部' },
      { id: 'draft', name: '草稿' },
      { id: 'signed', name: '已签署' },
      { id: 'expired', name: '已过期' }
    ]
  },
  
  onLoad() {
    this.loadContracts();
  },
  
  onShow() {
    // 每次显示页面都刷新数据
    this.loadContracts();
  },
  
  loadContracts() {
    const contracts = wx.getStorageSync('contracts') || [];
    
    // 检查合同是否过期
    const processedContracts = contracts.map(contract => {
      if (contract.status === 'signed' && contract.contractTerm.endDate) {
        const endDate = new Date(contract.contractTerm.endDate);
        const now = new Date();
        if (endDate < now) {
          return { ...contract, status: 'expired' };
        }
      }
      return contract;
    });
    
    // 更新存储
    wx.setStorageSync('contracts', processedContracts);
    
    this.setData({
      contracts: processedContracts,
      filteredContracts: processedContracts
    });
  },
  
  onTabChange(e) {
    const tabId = e.currentTarget.dataset.id;
    this.setData({
      currentTab: tabId
    });
    this.filterContracts();
  },
  
  filterContracts() {
    const { currentTab, contracts } = this.data;
    
    let filtered = contracts;
    
    if (currentTab !== 'all') {
      filtered = contracts.filter(c => c.status === currentTab);
    }
    
    this.setData({
      filteredContracts: filtered
    });
  },
  
  onContractTap(e) {
    const contract = e.currentTarget.dataset.contract;
    const content = encodeURIComponent(JSON.stringify(contract));
    
    wx.navigateTo({
      url: `/pages/detail/detail?content=${content}`
    });
  },
  
  onCreateContract() {
    wx.navigateTo({
      url: '/pages/template/template'
    });
  },
  
  onStatusText(status) {
    const statusMap = {
      'draft': '草稿',
      'signed': '已签署',
      'expired': '已过期'
    };
    return statusMap[status] || status;
  },
  
  onStatusColor(status) {
    const colorMap = {
      'draft': '#FF9800',
      'signed': '#07C160',
      'expired': '#F44336'
    };
    return colorMap[status] || '#999999';
  }
});
