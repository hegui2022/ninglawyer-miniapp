// pages/mine/mine.js
const app = getApp()

Page({
  data: {
    messageCount: 0,
    todayCount: 0,
    cacheSize: 0
  },

  onLoad() {
    console.log('我的页面加载')
    
    // 加载统计数据
    this.loadStats()
    
    // 计算缓存大小
    this.calculateCacheSize()
  },

  onShow() {
    // 每次显示都重新加载
    this.loadStats()
  },

  // 加载统计数据
  loadStats() {
    const messages = app.globalData.messageHistory || []
    const messageCount = messages.length
    
    // 计算今日咨询次数
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    
    let todayCount = 0
    messages.forEach(msg => {
      const msgTime = new Date(msg.id)
      if (msgTime >= today && msg.role === 'user') {
        todayCount++
      }
    })
    
    this.setData({
      messageCount: messageCount,
      todayCount: todayCount
    })
  },

  // 计算缓存大小
  calculateCacheSize() {
    try {
      const info = wx.getStorageInfoSync()
      const sizeKB = info.currentSize
      const sizeMB = (sizeKB / 1024).toFixed(2)
      this.setData({ cacheSize: sizeMB })
    } catch (e) {
      console.error('计算缓存大小失败', e)
    }
  },

  // 关于宁律师
  showAbout() {
    wx.showModal({
      title: '关于宁律师',
      content: '宁律师是一款智能法律咨询小程序，基于人工智能技术，为您提供专业的法律咨询服务。\n\n特点：\n• 大白话讲法律\n• 语音交互\n• 知识库支持\n• 24小时在线',
      showCancel: false,
      confirmText: '知道了'
    })
  },

  // 使用帮助
  showHelp() {
    wx.showModal({
      title: '使用帮助',
      content: '1. 在聊天页面输入法律问题\n2. 点击发送或使用语音输入\n3. 等待宁律师回复\n4. 查看历史记录\n\n提示：可以使用快捷标签快速提问',
      showCancel: false,
      confirmText: '知道了'
    })
  },

  // 常见问题
  showFAQ() {
    wx.showModal({
      title: '常见问题',
      content: 'Q: 宁律师免费吗？\nA: 完全免费\n\nQ: 可以用于正式场合吗？\nA: 仅供参考，复杂问题请咨询专业律师\n\nQ: 支持哪些问题？\nA: 民商法、劳动法、婚姻家庭法等',
      showCancel: false,
      confirmText: '知道了'
    })
  },

  // 分享给好友
  shareApp() {
    wx.showShareMenu({
      withShareTicket: true
    })
    wx.showToast({
      title: '请点击右上角分享',
      icon: 'none'
    })
  },

  // 意见反馈
  showFeedback() {
    wx.showModal({
      title: '意见反馈',
      content: '如有建议或问题，请联系：\nfeedback@ninglawyer.com',
      showCancel: false,
      confirmText: '知道了'
    })
  },

  // 清除缓存
  clearCache() {
    wx.showModal({
      title: '确认清除',
      content: '确定要清除所有缓存数据吗？',
      confirmColor: '#FF4D4F',
      success: (res) => {
        if (res.confirm) {
          try {
            wx.clearStorageSync()
            this.setData({ 
              messageCount: 0,
              todayCount: 0,
              cacheSize: 0 
            })
            wx.showToast({
              title: '已清除',
              icon: 'success'
            })
          } catch (e) {
            console.error('清除缓存失败', e)
            wx.showToast({
              title: '清除失败',
              icon: 'none'
            })
          }
        }
      }
    })
  },

  // 分享
  onShareAppMessage() {
    return {
      title: '宁律师 - 智能法律咨询',
      path: '/pages/chat/chat',
      imageUrl: '/images/share.jpg'
    }
  }
})
