// pages/alert/alert.js
Page({
  data: {
    alertCount: {
      high: 2,
      medium: 5,
      low: 8
    },
    tabs: [
      { name: '全部', value: 'all' },
      { name: '紧急', value: 'high' },
      { name: '重要', value: 'medium' },
      { name: '一般', value: 'low' }
    ],
    filterLevel: 'all',
    alerts: [
      {
        id: 1,
        title: '合同即将到期',
        desc: '合同编号 HT20250109 将在 3 天后到期，请及时处理续签或终止事宜。',
        level: 'high',
        time: '2025-01-09 10:30',
        handled: false
      },
      {
        id: 2,
        title: '履约提醒',
        desc: '合同编号 HT20241201 需要在 7 天内完成第二期付款。',
        level: 'high',
        time: '2025-01-09 09:15',
        handled: false
      },
      {
        id: 3,
        title: '信用风险预警',
        desc: '合作方 XX 公司信用评级下降，建议加强风险管控。',
        level: 'medium',
        time: '2025-01-08 16:20',
        handled: false
      },
      {
        id: 4,
        title: '合规提醒',
        desc: '新法规《XX条例》将于下月生效，请检查合同合规性。',
        level: 'medium',
        time: '2025-01-08 14:00',
        handled: false
      },
      {
        id: 5,
        title: '合同审查提醒',
        desc: '您有 3 份合同待审查，请及时处理。',
        level: 'low',
        time: '2025-01-08 10:30',
        handled: true
      }
    ],
    notificationEnabled: true,
    soundEnabled: true,
    vibrateEnabled: true
  },

  onLoad(options) {
    this.loadData()
  },

  onShow() {
    this.loadAlerts()
  },

  // 加载数据
  loadData() {
    // 加载预警数据
  },

  // 加载预警
  loadAlerts() {
    // 从后端加载最新预警数据
  },

  // 计算过滤后的预警
  get filteredAlerts() {
    if (this.data.filterLevel === 'all') {
      return this.data.alerts
    }
    return this.data.alerts.filter(alert => alert.level === this.data.filterLevel)
  },

  // 刷新预警
  refreshAlerts() {
    wx.showLoading({
      title: '刷新中...'
    })

    setTimeout(() => {
      wx.hideLoading()
      wx.showToast({
        title: '刷新成功',
        icon: 'success'
      })
    }, 1000)
  },

  // 过滤预警
  filterAlert(e) {
    const level = e.currentTarget.dataset.level
    this.setData({
      filterLevel: level
    })
  },

  // 切换过滤器
  switchFilter(e) {
    const value = e.currentTarget.dataset.value
    this.setData({
      filterLevel: value
    })
  },

  // 查看预警详情
  viewAlertDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({
      title: '预警详情',
      content: '查看完整的预警信息',
      showCancel: false
    })
  },

  // 处理预警
  handleAlert(e) {
    e.stopPropagation()
    const id = e.currentTarget.dataset.id

    wx.showModal({
      title: '确认处理',
      content: '确认处理此预警？',
      success: (res) => {
        if (res.confirm) {
          const alerts = this.data.alerts.map(alert => {
            if (alert.id === id) {
              return { ...alert, handled: true }
            }
            return alert
          })

          this.setData({
            alerts: alerts
          })

          wx.showToast({
            title: '已处理',
            icon: 'success'
          })
        }
      }
    })
  },

  // 查看详情
  viewDetail(e) {
    e.stopPropagation()
    const id = e.currentTarget.dataset.id
    this.viewAlertDetail({ currentTarget: { dataset: { id } } })
  },

  // 切换通知
  toggleNotification(e) {
    this.setData({
      notificationEnabled: e.detail.value
    })
  },

  // 切换声音
  toggleSound(e) {
    this.setData({
      soundEnabled: e.detail.value
    })
  },

  // 切换震动
  toggleVibrate(e) {
    this.setData({
      vibrateEnabled: e.detail.value
    })
  }
})
