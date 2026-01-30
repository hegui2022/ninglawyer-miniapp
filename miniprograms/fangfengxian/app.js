// app.js
App({
  globalData: {
    userInfo: null,
    riskLevel: 'low', // low, medium, high
    lastScanTime: null,
    riskCount: 0
  },

  onLaunch() {
    // 小程序启动
    console.log('防风险小程序启动')
    this.loadUserInfo()
  },

  onShow() {
    // 小程序显示
  },

  onHide() {
    // 小程序隐藏
  },

  // 加载用户信息
  loadUserInfo() {
    try {
      const userInfo = wx.getStorageSync('userInfo')
      if (userInfo) {
        this.globalData.userInfo = userInfo
      }
    } catch (e) {
      console.error('加载用户信息失败', e)
    }
  },

  // 保存用户信息
  saveUserInfo(userInfo) {
    this.globalData.userInfo = userInfo
    try {
      wx.setStorageSync('userInfo', userInfo)
    } catch (e) {
      console.error('保存用户信息失败', e)
    }
  },

  // 更新风险等级
  updateRiskLevel(level) {
    this.globalData.riskLevel = level
  },

  // 更新风险数量
  updateRiskCount(count) {
    this.globalData.riskCount = count
  },

  // 更新最后扫描时间
  updateLastScanTime(time) {
    this.globalData.lastScanTime = time
  }
})
