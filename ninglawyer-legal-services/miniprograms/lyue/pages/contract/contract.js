// 合同履约页面
Page({
  data: {
    contractId: null,
    contract: null,
    performance: {
      startDate: '2024-01-01',
      totalDays: 365,
      passedDays: 60,
      progress: 16
    },
    milestones: [
      {
        id: 1,
        title: '试用期考核',
        date: '2024-04-01',
        status: 'completed',
        description: '完成试用期考核评估'
      },
      {
        id: 2,
        title: '年中绩效评估',
        date: '2024-07-01',
        status: 'pending',
        description: '进行年中绩效评估'
      },
      {
        id: 3,
        title: '年终绩效评估',
        date: '2025-01-01',
        status: 'pending',
        description: '进行年终绩效评估'
      },
      {
        id: 4,
        title: '合同续签评估',
        date: '2025-01-01',
        status: 'pending',
        description: '决定是否续签合同'
      }
    ],
    reminders: [
      {
        id: 1,
        type: 'payment',
        title: '工资发放',
        date: '每月15日',
        nextDate: '2025-01-15',
        status: 'active'
      },
      {
        id: 2,
        type: 'insurance',
        title: '社保缴纳',
        date: '每月25日',
        nextDate: '2025-01-25',
        status: 'active'
      },
      {
        id: 3,
        type: 'renewal',
        title: '合同续签',
        date: '到期前30天',
        nextDate: '2024-12-02',
        status: 'pending'
      }
    ],
    records: [
      {
        id: 1,
        type: 'payment',
        title: '工资发放',
        date: '2024-12-15',
        amount: '¥15,000',
        status: 'completed'
      },
      {
        id: 2,
        type: 'insurance',
        title: '社保缴纳',
        date: '2024-12-25',
        status: 'completed'
      },
      {
        id: 3,
        type: 'milestone',
        title: '试用期考核通过',
        date: '2024-04-01',
        status: 'completed'
      }
    ]
  },
  
  onLoad(options) {
    if (options.id) {
      this.setData({ contractId: options.id });
      this.loadContract();
    }
  },
  
  loadContract() {
    // 加载合同数据
  },
  
  onMilestoneTap(e) {
    const milestone = e.currentTarget.dataset.milestone;
    wx.showModal({
      title: milestone.title,
      content: milestone.description,
      showCancel: false
    });
  },
  
  onReminderTap(e) {
    const reminder = e.currentTarget.dataset.reminder;
    wx.navigateTo({
      url: `/pages/reminder/detail?id=${reminder.id}`
    });
  },
  
  onRecordTap(e) {
    const record = e.currentTarget.dataset.record;
    wx.showModal({
      title: record.title,
      content: `时间：${record.date}\n状态：${record.status === 'completed' ? '已完成' : '进行中'}`,
      showCancel: false
    });
  },
  
  onAddRecord() {
    wx.navigateTo({
      url: `/pages/record/add?contractId=${this.data.contractId}`
    });
  },
  
  onEditReminder() {
    wx.navigateTo({
      url: `/pages/reminder/edit?contractId=${this.data.contractId}`
    });
  },
  
  onStatusText(status) {
    const statusMap = {
      'completed': '已完成',
      'pending': '待完成',
      'active': '进行中'
    };
    return statusMap[status] || status;
  },
  
  onStatusColor(status) {
    const colorMap = {
      'completed': '#07C160',
      'pending': '#FF9800',
      'active': '#2196F3'
    };
    return colorMap[status] || '#999999';
  }
});
