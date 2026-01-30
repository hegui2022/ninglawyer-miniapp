// 消息通知页面
Page({
  data: {
    activeTab: 0,
    tabs: ['全部', '系统通知', '咨询回复', '合同提醒'],
    notifications: {
      all: [
        {
          id: 1,
          type: 'system',
          icon: '🔔',
          title: '欢迎使用宁律师',
          content: '感谢您选择宁律师，现在开始咨询吧！',
          time: '刚刚',
          isRead: false
        },
        {
          id: 2,
          type: 'consult',
          icon: '💬',
          title: '律师已回复',
          content: '宁律师·民事回复了您的咨询',
          time: '10分钟前',
          isRead: false
        },
        {
          id: 3,
          type: 'contract',
          icon: '📝',
          title: '合同即将到期',
          content: '您的劳动合同将于7天后到期',
          time: '1小时前',
          isRead: true
        },
        {
          id: 4,
          type: 'system',
          icon: '🎉',
          title: '新功能上线',
          content: '合同模板库已更新，快去看看吧',
          time: '2小时前',
          isRead: true
        },
        {
          id: 5,
          type: 'contract',
          icon: '⚠️',
          title: '签署提醒',
          content: '服务合同等待您的签署',
          time: '昨天',
          isRead: true
        }
      ],
      system: [],
      consult: [],
      contract: []
    }
  },
  
  onLoad() {
    this.filterNotifications();
  },
  
  onTabChange(e) {
    const index = e.detail.index;
    this.setData({
      activeTab: index
    });
  },
  
  filterNotifications() {
    const { notifications } = this.data;
    
    notifications.system = notifications.all.filter(n => n.type === 'system');
    notifications.consult = notifications.all.filter(n => n.type === 'consult');
    notifications.contract = notifications.all.filter(n => n.type === 'contract');
    
    this.setData({ notifications });
  },
  
  onNotificationTap(e) {
    const notification = e.currentTarget.dataset.notification;
    
    // 标记为已读
    this.markAsRead(notification.id);
    
    // 根据类型跳转
    if (notification.type === 'consult') {
      wx.navigateTo({
        url: '/pages/consult/consult'
      });
    } else if (notification.type === 'contract') {
      wx.switchTab({
        url: '/pages/list/list'
      });
    }
  },
  
  markAsRead(id) {
    const notifications = this.data.notifications.all.map(n => {
      if (n.id === id) {
        n.isRead = true;
      }
      return n;
    });
    
    this.setData({
      'notifications.all': notifications
    });
    this.filterNotifications();
  },
  
  onMarkAllRead() {
    const notifications = this.data.notifications.all.map(n => ({
      ...n,
      isRead: true
    }));
    
    this.setData({
      'notifications.all': notifications
    });
    this.filterNotifications();
    
    wx.showToast({
      title: '已全部标记为已读',
      icon: 'success'
    });
  }
});
