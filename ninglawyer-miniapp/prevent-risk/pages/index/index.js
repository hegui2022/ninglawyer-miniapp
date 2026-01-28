// pages/index/index.js
const app = getApp()

Page({
  data: {
    userInfo: {},
    riskLevel: 'low',
    riskLevelText: '低风险',
    riskCount: {
      high: 0,
      medium: 0,
      low: 0
    },
    recentScans: [],
    riskTips: []
  },

  onLoad(options) {
    this.loadData()
  },

  onShow() {
    this.loadRiskData()
  },

  onPullDownRefresh() {
    this.loadData()
    setTimeout(() => {
      wx.stopPullDownRefresh()
    }, 1000)
  },

  // 加载数据
  loadData() {
    this.loadUserInfo()
    this.loadRiskData()
    this.loadRecentScans()
    this.loadRiskTips()
  },

  // 加载用户信息
  loadUserInfo() {
    this.setData({
      userInfo: app.globalData.userInfo || {}
    })
  },

  // 加载风险数据
  loadRiskData() {
    // 模拟数据
    this.setData({
      riskLevel: app.globalData.riskLevel || 'low',
      riskLevelText: this.getRiskLevelText(app.globalData.riskLevel || 'low'),
      riskCount: app.globalData.riskCount || { high: 0, medium: 0, low: 0 }
    })
  },

  // 加载最近扫描
  loadRecentScans() {
    // 模拟数据
    const scans = [
      {
        id: 1,
        name: '合同合规性检查',
        time: '2025-01-09 10:30',
        level: 'low',
        levelText: '低风险'
      },
      {
        id: 2,
        name: '企业资质审查',
        time: '2025-01-08 15:20',
        level: 'medium',
        levelText: '中风险'
      }
    ]
    this.setData({
      recentScans: scans
    })
  },

  // 加载风险提示
  loadRiskTips() {
    // 模拟数据
    const tips = [
      {
        id: 1,
        title: '合同即将到期',
        desc: '您有 3 份合同将在 7 天内到期，请及时续签或处理。'
      },
      {
        id: 2,
        title: '信用风险预警',
        desc: '某合作方信用评级下降，建议加强风险管控。'
      }
    ]
    this.setData({
      riskTips: tips
    })
  },

  // 获取风险等级文本
  getRiskLevelText(level) {
    const textMap = {
      'low': '低风险',
      'medium': '中风险',
      'high': '高风险'
    }
    return textMap[level] || '未知'
  },

  // 开始扫描
  startScan() {
    wx.navigateTo({
      url: '/pages/scan/scan'
    })
  },

  // 跳转到扫描页面
  goToScan() {
    wx.navigateTo({
      url: '/pages/scan/scan'
    })
  },

  // 跳转到合规检查
  goToCompliance() {
    wx.navigateTo({
      url: '/pages/compliance/compliance'
    })
  },

  // 跳转到报告页面
  goToReport() {
    wx.navigateTo({
      url: '/pages/report/report'
    })
  },

  // 跳转到预警页面
  goToAlert() {
    wx.navigateTo({
      url: '/pages/alert/alert'
    })
  },

  // 查看扫描详情
  viewScanDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/scan/scan?id=${id}`
    })
  },

  // 查看提示详情
  viewTipDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({
      title: '风险提示',
      content: '查看完整的风险提示详情',
      showCancel: false
    })
  }
})
