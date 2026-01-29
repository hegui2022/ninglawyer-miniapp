// 理约小程序 - app.js
const app = getApp()

App({
  globalData: {
    apiBase: 'http://localhost:5000',
    userInfo: null,
    token: null
  },

  onLaunch() {
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

  request(options) {
    const token = this.globalData.token

    return wx.request({
      ...options,
      header: {
        'Authorization': `Bearer ${token}`,
        ...options.header
      },
      success: (res) => {
        if (res.statusCode === 401) {
          this.handleTokenExpired()
        }
      }
    })
  },

  handleTokenExpired() {
    wx.removeStorageSync('token')
    wx.removeStorageSync('userInfo')
    this.globalData.token = null
    this.globalData.userInfo = null

    wx.reLaunch({
      url: '/pages/index/index'
    })
  }
})
