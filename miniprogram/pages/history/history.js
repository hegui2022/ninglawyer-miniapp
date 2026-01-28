// pages/history/history.js
const app = getApp()

Page({
  data: {
    messages: [],
    isPlayingAudio: false,
    innerAudioContext: null
  },

  onLoad() {
    console.log('历史记录页面加载')
    
    // 初始化音频播放器
    this.initAudioPlayer()
    
    // 加载消息历史
    this.loadMessages()
  },

  onShow() {
    // 每次显示都重新加载
    this.loadMessages()
  },

  onUnload() {
    // 停止播放
    if (this.data.innerAudioContext) {
      this.data.innerAudioContext.stop()
    }
  },

  // 初始化音频播放器
  initAudioPlayer() {
    const innerAudioContext = wx.createInnerAudioContext()
    
    innerAudioContext.onPlay(() => {
      console.log('开始播放音频')
      this.setData({ isPlayingAudio: true })
    })
    
    innerAudioContext.onEnded(() => {
      console.log('音频播放结束')
      this.setData({ isPlayingAudio: false })
    })
    
    innerAudioContext.onError((err) => {
      console.error('音频播放错误', err)
      this.setData({ isPlayingAudio: false })
    })
    
    this.setData({ innerAudioContext })
  },

  // 加载消息历史
  loadMessages() {
    const messages = app.globalData.messageHistory || []
    this.setData({ messages })
  },

  // 播放音频
  playAudio(e) {
    const url = e.currentTarget.dataset.url
    console.log('播放音频', url)
    
    // 停止当前播放
    if (this.data.innerAudioContext) {
      this.data.innerAudioContext.stop()
    }
    
    // 设置音频源并播放
    this.data.innerAudioContext.src = url
    this.data.innerAudioContext.play()
  },

  // 清空历史记录
  clearHistory() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有历史记录吗？',
      confirmColor: '#FF4D4F',
      success: (res) => {
        if (res.confirm) {
          app.saveMessageHistory([])
          this.setData({ messages: [] })
          wx.showToast({
            title: '已清空',
            icon: 'success'
          })
        }
      }
    })
  },

  // 导出历史记录
  exportHistory() {
    if (this.data.messages.length === 0) {
      wx.showToast({
        title: '暂无记录',
        icon: 'none'
      })
      return
    }
    
    // 生成文本内容
    let content = '宁律师咨询记录\n'
    content += '='.repeat(30) + '\n\n'
    
    this.data.messages.forEach((msg, index) => {
      const role = msg.role === 'user' ? '我' : '宁律师'
      content += `${role}：${msg.content}\n\n`
    })
    
    // 导出到剪贴板
    wx.setClipboardData({
      data: content,
      success: () => {
        wx.showToast({
          title: '已复制到剪贴板',
          icon: 'success'
        })
      }
    })
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadMessages()
    setTimeout(() => {
      wx.stopPullDownRefresh()
    }, 1000)
  }
})
