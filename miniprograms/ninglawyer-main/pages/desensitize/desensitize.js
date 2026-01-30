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
      // 调用后端API
      const res = await wx.request({
        url: `${app.globalData.apiBase}/api/desensitize/`,
        method: 'POST',
        data: {
          name: this.data.name,
          id_card: this.data.idCard,
          phone: this.data.phone,
          address: this.data.address
        },
        header: {
          'Authorization': `Bearer ${app.globalData.token || wx.getStorageSync('token')}`
        }
      })

      if (res.data.success) {
        const data = res.data.data
        this.setData({ result: data })
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
