// app.js
App({
  globalData: {
    // 服务器配置 - 需要根据实际情况修改
    baseUrl: 'http://localhost:8000',  // 开发环境
    // baseUrl: 'https://your-domain.com',  // 生产环境
    
    // 用户信息
    userInfo: null,
    
    // 会话ID
    sessionId: '',
    
    // 消息历史
    messageHistory: []
  },

  onLaunch() {
    console.log('宁律师小程序启动')
    
    // 生成会话ID
    this.generateSessionId()
    
    // 加载本地存储的消息历史
    this.loadMessageHistory()
    
    // 获取用户信息
    this.getUserInfo()
  },

  // 生成会话ID
  generateSessionId() {
    const sessionId = 'wx_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
    this.globalData.sessionId = sessionId
    wx.setStorageSync('sessionId', sessionId)
  },

  // 加载消息历史
  loadMessageHistory() {
    try {
      const history = wx.getStorageSync('messageHistory') || []
      this.globalData.messageHistory = history
    } catch (e) {
      console.error('加载消息历史失败', e)
    }
  },

  // 保存消息历史
  saveMessageHistory(messages) {
    try {
      this.globalData.messageHistory = messages
      wx.setStorageSync('messageHistory', messages)
    } catch (e) {
      console.error('保存消息历史失败', e)
    }
  },

  // 获取用户信息
  getUserInfo() {
    try {
      const userInfo = wx.getStorageSync('userInfo')
      if (userInfo) {
        this.globalData.userInfo = userInfo
      }
    } catch (e) {
      console.error('获取用户信息失败', e)
    }
  },

  // 保存用户信息
  setUserInfo(userInfo) {
    this.globalData.userInfo = userInfo
    try {
      wx.setStorageSync('userInfo', userInfo)
    } catch (e) {
      console.error('保存用户信息失败', e)
    }
  }
})
