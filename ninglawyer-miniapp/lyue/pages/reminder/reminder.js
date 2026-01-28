// 履约提醒页面
Page({
  data: {
    reminders: [
      {
        id: 1,
        type: 'payment',
        title: '工资发放提醒',
        contractTitle: '标准劳动合同',
        partyB: '张三',
        date: '每月15日',
        nextDate: '2025-01-15',
        status: 'active',
        daysLeft: 10,
        importance: 'high'
      },
      {
        id: 2,
        type: 'insurance',
        title: '社保缴纳提醒',
        contractTitle: '标准劳动合同',
        partyB: '张三',
        date: '每月25日',
        nextDate: '2025-01-25',
        status: 'active',
        daysLeft: 20,
        importance: 'medium'
      },
      {
        id: 3,
        type: 'renewal',
        title: '合同续签提醒',
        contractTitle: '技术服务合同',
        partyB: '李四',
        date: '到期前30天',
        nextDate: '2024-12-02',
        status: 'active',
        daysLeft: -8,
        importance: 'high'
      },
      {
        id: 4,
        type: 'milestone',
        title: '绩效评估提醒',
        contractTitle: '标准劳动合同',
        partyB: '张三',
        date: '2025-01-01',
        nextDate: '2025-01-01',
        status: 'pending',
        daysLeft: 27,
        importance: 'medium'
      },
      {
        id: 5,
        type: 'payment',
        title: '工资发放提醒',
        contractTitle: '兼职劳动合同',
        partyB: '王五',
        date: '每月15日',
        nextDate: '2025-01-15',
        status: 'completed',
        daysLeft: 0,
        importance: 'low'
      }
    ],
    filterType: 'all',
    filterTypes: [
      { id: 'all', name: '全部' },
      { id: 'pending', name: '待处理' },
      { id: 'active', name: '进行中' },
      { id: 'completed', name: '已完成' }
    ]
  },
  
  onLoad() {
    this.loadReminders();
  },
  
  loadReminders() {
    // 加载提醒数据
  },
  
  onFilterChange(e) {
    const type = e.currentTarget.dataset.type;
    this.setData({
      filterType: type
    });
    this.filterReminders();
  },
  
  filterReminders() {
    // 过滤提醒列表
  },
  
  onReminderTap(e) {
    const reminder = e.currentTarget.dataset.reminder;
    
    if (reminder.status === 'completed') {
      wx.showModal({
        title: reminder.title,
        content: `合同：${reminder.contractTitle}\n人员：${reminder.partyB}\n时间：${reminder.date}`,
        showCancel: false
      });
    } else {
      wx.showModal({
        title: reminder.title,
        content: `合同：${reminder.contractTitle}\n人员：${reminder.partyB}\n时间：${reminder.date}\n下次提醒：${reminder.nextDate}`,
        confirmText: '标记完成',
        success: (res) => {
          if (res.confirm) {
            this.markAsCompleted(reminder.id);
          }
        }
      });
    }
  },
  
  markAsCompleted(id) {
    const reminders = this.data.reminders.map(r => {
      if (r.id === id) {
        return { ...r, status: 'completed' };
      }
      return r;
    });
    
    this.setData({ reminders });
    
    wx.showToast({
      title: '已完成',
      icon: 'success'
    });
  },
  
  onAddReminder() {
    wx.navigateTo({
      url: '/pages/reminder/add'
    });
  },
  
  onSettings() {
    wx.navigateTo({
      url: '/pages/settings/settings'
    });
  },
  
  onTypeIcon(type) {
    const icons = {
      'payment': '💰',
      'insurance': '🛡️',
      'renewal': '🔄',
      'milestone': '🎯'
    };
    return icons[type] || '📋';
  },
  
  onImportanceColor(importance) {
    const colors = {
      'high': '#F44336',
      'medium': '#FF9800',
      'low': '#2196F3'
    };
    return colors[importance] || '#999999';
  }
});
