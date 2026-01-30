// pages/desensitize/desensitize.js
const app = getApp()

Page({
  data: {
    name: '',
    idCard: '',
    phone: '',
    address: '',
    result: null,
    loading: false
  },

  // 输入处理
  onNameInput(e) {
    this.setData({ name: e.detail.value })
  },

  onIdCardInput(e) {
    this.setData({ idCard: e.detail.value })
  },

  onPhoneInput(e) {
    this.setData({ phone: e.detail.value })
  },

  onAddressInput(e) {
    this.setData({ address: e.detail.value })
  },

  // 脱敏
  async onDesensitize() {
    if (!this.data.name && !this.data.idCard && !this.data.phone && !this.data.address) {
      wx.showToast({
        title: '请输入需要脱敏的信息',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      // 构建查询语句
      const parts = []
      if (this.data.name) parts.push(`姓名${this.data.name}`)
      if (this.data.idCard) parts.push(`身份证${this.data.idCard}`)
      if (this.data.phone) parts.push(`手机${this.data.phone}`)
      if (this.data.address) parts.push(`地址${this.data.address}`)

      const query = `帮我脱敏：${parts.join('，')}`

      // 调用后端API
      const res = await wx.request({
        url: `${app.globalData.apiConfig.baseUrl}/api/master/desensitize`,
        method: 'POST',
        data: {
          name: this.data.name,
          id_card: this.data.idCard,
          phone: this.data.phone,
          address: this.data.address
        },
        timeout: app.globalData.apiConfig.timeout
      })

      if (res.data.success) {
        const content = res.data.content || res.data.data
        let result = null

        // 尝试解析JSON
        try {
          if (typeof content === 'string') {
            result = JSON.parse(content)
          } else {
            result = content
          }
        } catch (e) {
          wx.showToast({
            title: '解析失败，请重试',
            icon: 'none'
          })
          this.setData({ loading: false })
          return
        }

        this.setData({ result })
      } else {
        wx.showToast({
          title: res.data.error || '脱敏失败',
          icon: 'none'
        })
      }
    } catch (error) {
      console.error('脱敏失败:', error)
      wx.showToast({
        title: '网络错误，请检查连接',
        icon: 'none'
      })
    }

    this.setData({ loading: false })
  },

  // 清空
  onClear() {
    this.setData({
      name: '',
      idCard: '',
      phone: '',
      address: '',
      result: null
    })
  },

  // 复制结果
  onCopyResult() {
    if (!this.data.result) return

    const text = JSON.stringify(this.data.result, null, 2)
    wx.setClipboardData({
      data: text,
      success() {
        wx.showToast({
          title: '已复制',
          icon: 'success'
        })
      }
    })
  }
})
