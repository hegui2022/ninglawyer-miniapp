// app.js
App({
  globalData: {
    userInfo: null,
    // API配置
    apiConfig: {
      baseUrl: 'http://localhost:5000',  // 本地开发地址
      timeout: 30000
    }
  },

  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
  }
})
