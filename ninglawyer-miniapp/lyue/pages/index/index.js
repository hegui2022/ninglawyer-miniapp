// 理约 - 首页
Page({
  data: {
    overview: {
      totalContracts: 8,
      activeContracts: 6,
      expiringSoon: 2,
      completedMilestones: 18
    },
    expiringContracts: [
      {
        id: 1,
        title: '标准劳动合同',
        partyA: 'XX科技有限公司',
        partyB: '张三',
        endDate: '2025-02-15',
        daysLeft: 30,
        status: 'active'
      },
      {
        id: 2,
        title: '技术服务合同',
        partyA: 'XX科技有限公司',
        partyB: '李四',
        endDate: '2025-01-28',
        daysLeft: 12,
        status: 'active'
      }
    ],
    recentActivities: [
      {
        id: 1,
        contractTitle: '标准劳动合同',
        activityType: 'payment',
        description: '工资发放提醒',
        time: '2小时前',
        status: 'pending'
      },
      {
        id: 2,
        contractTitle: '技术服务合同',
        activityType: 'milestone',
        description: '项目里程碑节点',
        time: '昨天',
        status: 'completed'
      },
      {
        id: 3,
        contractTitle: '兼职劳动合同',
        activityType: 'renewal',
        description: '合同续签提醒',
        time: '3天前',
        status: 'pending'
      },
      {
        id: 4,
        contractTitle: '标准劳动合同',
        activityType: 'insurance',
        description: '社保缴纳提醒',
        time: '1周前',
        status: 'completed'
      }
    ]
  },
  
  onLoad() {
    this.loadOverview();
  },
  
  onShow() {
    // 每次显示页面都刷新数据
    this.loadOverview();
  },
  
  loadOverview() {
    // 加载概览数据
  },
  
  onContractTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/contract/contract?id=${id}`
    });
  },
  
  onActivityTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/reminder/reminder?id=${id}`
    });
  },
  
  onAllContracts() {
    wx.switchTab({
      url: '/pages/contract/contract'
    });
  },
  
  onAllReminders() {
    wx.navigateTo({
      url: '/pages/reminder/reminder'
    });
  },
  
  onSettings() {
    wx.navigateTo({
      url: '/pages/settings/settings'
    });
  }
});
