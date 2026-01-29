// app.js
const apiBase = 'http://localhost:5000' // 修改为实际的服务器地址

App({
  globalData: {
    apiBase: apiBase,
    userInfo: null,
    token: null
  },

  onLaunch() {
    // 初始化
    this.checkLogin()
  },

  checkLogin() {
    const token = wx.getStorageSync('token')
    const userInfo = wx.getStorageSync('userInfo')

    if (token && userInfo) {
      this.globalData.token = token
      this.globalData.userInfo = userInfo
    }
  },

  // 带认证的请求
  request(options) {
    const token = this.globalData.token

    return wx.request({
      ...options,
      header: {
        'Authorization': `Bearer ${token}`,
        ...options.header
      },
      success: (res) => {
        // Token过期处理
        if (res.statusCode === 401) {
          this.handleTokenExpired()
        }
      }
    })
  },

  handleTokenExpired() {
    // 清除本地存储
    wx.removeStorageSync('token')
    wx.removeStorageSync('userInfo')
    this.globalData.token = null
    this.globalData.userInfo = null

    // 跳转到登录页
    wx.reLaunch({
      url: '/pages/login/login'
    })
  }
})
