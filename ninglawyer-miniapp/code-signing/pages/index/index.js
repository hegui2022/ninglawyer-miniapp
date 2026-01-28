// 码上签约 - 首页（使用网络图片）
Page({
  data: {
    stats: {
      total: 128,
      signed: 96,
      pending: 32
    },
    quickActions: [
      {
        id: 1,
        icon: '📝',
        title: '创建合同',
        desc: '快速创建新合同',
        url: '/pages/create/create'
      },
      {
        id: 2,
        icon: '📋',
        title: '合同模板',
        desc: '选择模板创建',
        url: '/pages/template/template'
      },
      {
        id: 3,
        icon: '✍️',
        title: '签署记录',
        desc: '查看签署历史',
        url: '/pages/record/record'
      },
      {
        id: 4,
        icon: '🔍',
        title: '搜索合同',
        desc: '快速查找合同',
        url: '/pages/search/search'
      }
    ],
    recentContracts: [
      {
        id: 1,
        name: '劳动合同',
        type: '劳动合同',
        status: 'signed',
        date: '2024-01-10',
        amount: '15000'
      },
      {
        id: 2,
        name: '服务合同',
        type: '服务合同',
        status: 'pending',
        date: '2024-01-08',
        amount: '50000'
      },
      {
        id: 3,
        name: '采购合同',
        type: '采购合同',
        status: 'signed',
        date: '2024-01-05',
        amount: '30000'
      }
    ]
  },
  
  onLoad() {
    this.loadStats();
  },
  
  loadStats() {
    // 加载统计数据
  },
  
  onQuickAction(e) {
    const url = e.currentTarget.dataset.url;
    if (url && url.includes('create')) {
      wx.navigateTo({
        url: '/pages/create/create'
      });
    } else {
      wx.showToast({
        title: '功能开发中',
        icon: 'none'
      });
    }
  },
  
  onContractTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/detail/detail?id=' + id
    });
  }
});
