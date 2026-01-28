// 怎么判 - 首页
Page({
  data: {
    services: [
      {
        id: 'breach',
        name: '违约判断',
        description: '判断合同是否违约',
        icon: '⚖️',
        color: '#F44336'
      },
      {
        id: 'rights',
        name: '维权指导',
        description: '获取维权操作指引',
        icon: '🛡️',
        color: '#2196F3'
      },
      {
        id: 'cases',
        name: '判例查询',
        description: '查询相似案例',
        icon: '📚',
        color: '#FF9800'
      }
    ],
    recentCases: [
      {
        id: 1,
        title: '未按时支付工资违约',
        type: 'breach',
        result: '构成违约',
        date: '2024-12-20'
      },
      {
        id: 2,
        title: '单方面解除合同',
        type: 'breach',
        result: '需支付补偿',
        date: '2024-12-18'
      },
      {
        id: 3,
        title: '未按约定交付货物',
        type: 'breach',
        result: '构成违约',
        date: '2024-12-15'
      }
    ],
    hotTopics: [
      '工资拖欠',
      '合同解除',
      '质量不合格',
      '逾期交付',
      '违约金'
    ]
  },
  
  onLoad() {
    this.loadRecentCases();
  },
  
  loadRecentCases() {
    // 加载最近案例
  },
  
  onServiceTap(e) {
    const id = e.currentTarget.dataset.id;
    
    switch(id) {
      case 'breach':
        wx.navigateTo({
          url: '/pages/breach/breach'
        });
        break;
      case 'rights':
        wx.navigateTo({
          url: '/pages/rights/rights'
        });
        break;
      case 'cases':
        wx.navigateTo({
          url: '/pages/cases/cases'
        });
        break;
    }
  },
  
  onCaseTap(e) {
    const caseId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/case-detail/case-detail?id=${caseId}`
    });
  },
  
  onTopicTap(e) {
    const topic = e.currentTarget.dataset.topic;
    wx.navigateTo({
      url: `/pages/cases/cases?keyword=${topic}`
    });
  },
  
  onConsult() {
    wx.showModal({
      title: '法律咨询',
      content: '是否跳转到法律教官进行详细咨询？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({
            title: '跳转中...',
            icon: 'loading'
          });
        }
      }
    });
  }
});
