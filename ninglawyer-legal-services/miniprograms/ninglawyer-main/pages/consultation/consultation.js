const app = getApp()

Page({
  data: {
    userInfo: {},
    currentDomain: 'civil',
    domains: [],
    inputText: '',
    messages: [],
    loading: false,
    scrollIntoView: '',
    tips: [
      '详细描述您遇到的法律问题',
      '提供相关的时间、地点等信息',
      '如实陈述情况，获得更准确的建议'
    ]
  },

  onLoad(options) {
    this.loadUserInfo()
    this.loadDomains()
    
    // 如果从首页跳转过来，可能携带了 domain
    if (options.domain) {
      this.setData({ currentDomain: options.domain })
    }
    
    // 如果携带了问题，自动发送
    if (options.question) {
      this.setData({ inputText: decodeURIComponent(options.question) })
      setTimeout(() => {
        this.sendMessage()
      }, 500)
    }
  },

  onShow() {
    this.loadUserInfo()
  },

  loadUserInfo() {
    const userInfo = app.globalData.userInfo || wx.getStorageSync('userInfo') || {}
    this.setData({ userInfo })
  },

  loadDomains() {
    const domains = [
      { id: 'civil', name: '民事', icon: '/static/icons/civil.png' },
      { id: 'criminal', name: '刑事', icon: '/static/icons/criminal.png' },
      { id: 'company', name: '公司', icon: '/static/icons/company.png' },
      { id: 'labor', name: '劳动', icon: '/static/icons/labor.png' },
      { id: 'marriage', name: '婚姻', icon: '/static/icons/marriage.png' },
      { id: 'ip', name: '知识产权', icon: '/static/icons/ip.png' },
      { id: 'contract', name: '合同', icon: '/static/icons/contract.png' },
      { id: 'other', name: '其他', icon: '/static/icons/other.png' }
    ]
    this.setData({ domains })
  },

  selectDomain(e) {
    const id = e.currentTarget.dataset.id
    this.setData({ currentDomain: id })
    
    wx.showToast({
      title: '已切换到' + this.data.domains.find(d => d.id === id).name + '领域',
      icon: 'none'
    })
  },

  onInput(e) {
    this.setData({ inputText: e.detail.value })
  },

  async sendMessage() {
    const { inputText, currentDomain, messages } = this.data
    
    if (!inputText.trim()) {
      wx.showToast({
        title: '请输入内容',
        icon: 'none'
      })
      return
    }

    // 添加用户消息
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputText,
      time: this.formatTime(new Date()),
      canCopy: false
    }
    
    this.setData({
      messages: [...messages, userMessage],
      inputText: '',
      loading: true,
      scrollIntoView: 'msg-' + messages.length
    })

    // 发送请求到后端
    try {
      const result = await this.requestConsultation(inputText, currentDomain)
      
      // 添加 AI 回复
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: result.answer || result.content || '抱歉，我暂时无法回答这个问题。',
        time: this.formatTime(new Date()),
        canCopy: true
      }
      
      this.setData({
        messages: [...this.data.messages, aiMessage],
        loading: false,
        scrollIntoView: 'msg-' + (messages.length + 1)
      })
      
      // 保存咨询记录到历史
      this.saveConsultationRecord(userMessage.content, aiMessage.content, currentDomain)
      
    } catch (error) {
      console.error('咨询失败:', error)
      
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: '抱歉，服务暂时不可用，请稍后重试。',
        time: this.formatTime(new Date()),
        canCopy: false
      }
      
      this.setData({
        messages: [...this.data.messages, errorMessage],
        loading: false,
        scrollIntoView: 'msg-' + (messages.length + 1)
      })
      
      wx.showToast({
        title: '咨询失败，请重试',
        icon: 'none'
      })
    }
  },

  requestConsultation(question, domain) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: app.globalData.apiBase + '/api/consultation/consult',
        method: 'POST',
        header: {
          'Authorization': `Bearer ${app.globalData.token || wx.getStorageSync('token')}`,
          'Content-Type': 'application/json'
        },
        data: {
          domain: domain,
          question: question,
          chat_history: this.data.messages.slice(-10).map(m => ({
            role: m.role,
            content: m.content
          }))
        },
        success: (res) => {
          if (res.data.success) {
            resolve(res.data.data)
          } else {
            reject(new Error(res.data.error || '请求失败'))
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },

  copyMessage(e) {
    const content = e.currentTarget.dataset.content
    wx.setClipboardData({
      data: content,
      success: () => {
        wx.showToast({
          title: '复制成功',
          icon: 'success'
        })
      }
    })
  },

  saveConsultationRecord(question, answer, domain) {
    try {
      const records = wx.getStorageSync('consultation_records') || []
      records.unshift({
        id: Date.now(),
        domain: domain,
        question: question,
        answer: answer,
        time: new Date().toISOString()
      })
      // 只保留最近 100 条
      if (records.length > 100) {
        records.splice(100)
      }
      wx.setStorageSync('consultation_records', records)
    } catch (error) {
      console.error('保存记录失败:', error)
    }
  },

  loadMore() {
    // 加载更多历史消息
    console.log('加载更多')
  },

  formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${hours}:${minutes}`
  },

  onPullDownRefresh() {
    // 刷新会话
    wx.stopPullDownRefresh()
  }
})
