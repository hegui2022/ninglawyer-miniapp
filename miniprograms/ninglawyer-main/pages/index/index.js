const app = getApp()

Page({
  data: {
    userInfo: {},
    currentTime: '',
    domains: [],
    hotQuestions: [],
    recentSessions: []
  },

  onLoad() {
    this.updateTime()
    this.loadUserInfo()
    this.loadDomains()
    this.loadHotQuestions()
    this.loadRecentSessions()
  },

  onShow() {
    this.updateTime()
  },

  updateTime() {
    const now = new Date()
    const hours = now.getHours()
    let greeting = '早上好'

    if (hours >= 12 && hours < 18) {
      greeting = '下午好'
    } else if (hours >= 18) {
      greeting = '晚上好'
    }

    const timeStr = `${now.getMonth() + 1}月${now.getDate()}日 ${greeting}`

    this.setData({
      currentTime: timeStr
    })
  },

  loadUserInfo() {
    const userInfo = app.globalData.userInfo || wx.getStorageSync('userInfo') || {}
    this.setData({ userInfo })
  },

  loadDomains() {
    const domains = [
      { name: 'civil', label: '民事', icon: '/static/icons/civil.png' },
      { name: 'criminal', label: '刑事', icon: '/static/icons/criminal.png' },
      { name: 'company', label: '公司', icon: '/static/icons/company.png' },
      { name: 'labor', label: '劳动', icon: '/static/icons/labor.png' },
      { name: 'marriage', label: '婚姻', icon: '/static/icons/marriage.png' },
      { name: 'ip', label: '知识产权', icon: '/static/icons/ip.png' },
      { name: 'contract', label: '合同', icon: '/static/icons/contract.png' },
      { name: 'other', label: '其他', icon: '/static/icons/other.png' }
    ]

    this.setData({ domains })
  },

  loadHotQuestions() {
    // 可以从后端获取或使用默认数据
    const hotQuestions = [
      { id: 1, question: '劳动仲裁的流程是什么？' },
      { id: 2, question: '离婚时财产如何分割？' },
      { id: 3, question: '签订合同时需要注意什么？' },
      { id: 4, question: '如何申请法律援助？' },
      { id: 5, question: '工伤如何认定和赔偿？' }
    ]

    this.setData({ hotQuestions })
  },

  loadRecentSessions() {
    // 从后端获取最近会话
    this.requestWithAuth({
      url: app.globalData.apiBase + '/api/session/list',
      method: 'GET',
      success: (res) => {
        const sessions = (res.data.data.sessions || []).slice(0, 5).map(session => ({
          id: session.session_id,
          title: session.title,
          lastMessageTime: this.formatTime(session.updated_at)
        }))

        this.setData({ recentSessions: sessions })
      }
    })
  },

  onSearch(e) {
    const keyword = e.detail.value
    if (!keyword) {
      wx.showToast({
        title: '请输入搜索内容',
        icon: 'none'
      })
      return
    }

    wx.navigateTo({
      url: `/pages/session/session?keyword=${encodeURIComponent(keyword)}`
    })
  },

  goToConsultation() {
    wx.navigateTo({
      url: '/pages/consultation/consultation'
    })
  },

  goToContract() {
    wx.navigateTo({
      url: '/pages/contract/contract'
    })
  },

  goToDesensitize() {
    wx.navigateTo({
      url: '/pages/desensitize/desensitize'
    })
  },

  goToHistory() {
    wx.switchTab({
      url: '/pages/history/history'
    })
  },

  goToProfile() {
    wx.switchTab({
      url: '/pages/profile/profile'
    })
  },

  goToDomains() {
    wx.navigateTo({
      url: '/pages/domains/domains'
    })
  },

  selectDomain(e) {
    const domain = e.currentTarget.dataset.domain
    wx.navigateTo({
      url: `/pages/consultation/consultation?domain=${domain}`
    })
  },

  askQuestion(e) {
    const question = e.currentTarget.dataset.question
    wx.navigateTo({
      url: `/pages/session/session?question=${encodeURIComponent(question)}`
    })
  },

  goToSession(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/session/session?id=${id}`
    })
  },

  goToSessions() {
    wx.navigateTo({
      url: '/pages/sessions/sessions'
    })
  },

  requestWithAuth(options) {
    const token = app.globalData.token || wx.getStorageSync('token')

    return wx.request({
      ...options,
      header: {
        'Authorization': `Bearer ${token}`,
        ...options.header
      }
    })
  },

  formatTime(dateStr) {
    if (!dateStr) return ''

    const date = new Date(dateStr)
    const now = new Date()
    const diff = now - date

    if (diff < 60000) {
      return '刚刚'
    } else if (diff < 3600000) {
      return `${Math.floor(diff / 60000)}分钟前`
    } else if (diff < 86400000) {
      return `${Math.floor(diff / 3600000)}小时前`
    } else if (diff < 604800000) {
      return `${Math.floor(diff / 86400000)}天前`
    } else {
      return `${date.getMonth() + 1}/${date.getDate()}`
    }
  }
})
