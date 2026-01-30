const app = getApp()

Page({
  data: {
    userInfo: {},
    sessionId: null,
    messages: [],
    inputText: '',
    loading: false,
    scrollIntoView: ''
  },

  onLoad(options) {
    const id = options.id
    this.setData({ sessionId: id })
    this.loadUserInfo()
    
    if (id) {
      this.loadMessages(id)
    }
  },

  loadUserInfo() {
    this.setData({ userInfo: app.globalData.userInfo || wx.getStorageSync('userInfo') || {} })
  },

  async loadMessages(sessionId) {
    try {
      const result = await this.request('/api/session/' + sessionId + '/messages')
      if (result.success) {
        this.setData({ 
          messages: result.data.messages.map(m => ({
            id: m.id,
            role: m.role,
            content: m.content,
            time: this.formatTime(m.created_at)
          }))
        })
      }
    } catch (error) {
      console.error('加载消息失败:', error)
    }
  },

  onInput(e) {
    this.setData({ inputText: e.detail.value })
  },

  async sendMessage() {
    if (!this.data.inputText.trim()) return

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: this.data.inputText,
      time: this.formatTime(new Date())
    }

    this.setData({
      messages: [...this.data.messages, userMessage],
      inputText: '',
      loading: true
    })

    try {
      // 如果有会话ID，发送到会话；否则发送到咨询接口
      let url = '/api/consultation/consult'
      if (this.data.sessionId) {
        url = '/api/session/' + this.data.sessionId + '/message'
      }

      const result = await this.request(url, {
        message: this.data.messages[this.data.messages.length - 1].content
      }, 'POST')

      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: result.answer || result.content || '回复内容',
        time: this.formatTime(new Date())
      }

      this.setData({
        messages: [...this.data.messages, aiMessage],
        loading: false
      })
    } catch (error) {
      this.setData({ loading: false })
      wx.showToast({ title: '发送失败', icon: 'none' })
    }
  },

  request(url, data = {}, method = 'GET') {
    return new Promise((resolve, reject) => {
      wx.request({
        url: app.globalData.apiBase + url,
        method: method,
        data: data,
        header: {
          'Authorization': `Bearer ${app.globalData.token || wx.getStorageSync('token')}`,
          'Content-Type': 'application/json'
        },
        success: (res) => resolve(res.data),
        fail: reject
      })
    })
  },

  formatTime(dateStr) {
    const date = new Date(dateStr)
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${hours}:${minutes}`
  }
})
