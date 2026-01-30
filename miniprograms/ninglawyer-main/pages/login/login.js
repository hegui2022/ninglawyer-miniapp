const app = getApp()

Page({
  data: {
    phone: '',
    code: '',
    sending: false,
    countDown: 0
  },

  onLoad() {
    // 检查是否已登录
    if (app.globalData.token) {
      wx.redirectTo({
        url: '/pages/index/index'
      })
    }
  },

  onPhoneInput(e) {
    this.setData({
      phone: e.detail.value
    })
  },

  onCodeInput(e) {
    this.setData({
      code: e.detail.value
    })
  },

  sendCode() {
    if (!this.validatePhone(this.data.phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      })
      return
    }

    this.setData({ sending: true })

    // 调用后端发送验证码
    wx.request({
      url: app.globalData.apiBase + '/api/auth/send-code',
      method: 'POST',
      data: {
        phone: this.data.phone
      },
      success: () => {
        wx.showToast({
          title: '验证码已发送',
          icon: 'success'
        })

        // 开始倒计时
        this.startCountDown()
      },
      fail: (err) => {
        wx.showToast({
          title: err.errMsg || '发送失败',
          icon: 'none'
        })
      },
      complete: () => {
        this.setData({ sending: false })
      }
    })
  },

  startCountDown() {
    let countDown = 60
    this.setData({ countDown })

    const timer = setInterval(() => {
      countDown--
      this.setData({ countDown })

      if (countDown <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  },

  handleWechatLogin() {
    wx.showLoading({
      title: '登录中...'
    })

    wx.login({
      success: (res) => {
        if (res.code) {
          // 发送 code 到后端
          wx.request({
            url: app.globalData.apiBase + '/api/auth/wechat-login',
            method: 'POST',
            data: {
              code: res.code
            },
            success: (loginRes) => {
              const { data } = loginRes.data

              // 保存用户信息和 token
              app.globalData.token = data.token
              app.globalData.userInfo = data.user_info

              wx.setStorageSync('token', data.token)
              wx.setStorageSync('userInfo', data.user_info)

              wx.hideLoading()

              wx.showToast({
                title: '登录成功',
                icon: 'success'
              })

              // 跳转到首页
              setTimeout(() => {
                wx.switchTab({
                  url: '/pages/index/index'
                })
              }, 1500)
            },
            fail: (err) => {
              wx.hideLoading()
              wx.showToast({
                title: err.errMsg || '登录失败',
                icon: 'none'
              })
            }
          })
        } else {
          wx.hideLoading()
          wx.showToast({
            title: '获取用户信息失败',
            icon: 'none'
          })
        }
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({
          title: '微信登录失败',
          icon: 'none'
        })
      }
    })
  },

  handlePhoneLogin() {
    if (!this.validatePhone(this.data.phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      })
      return
    }

    if (!this.data.code || this.data.code.length !== 6) {
      wx.showToast({
        title: '请输入正确的验证码',
        icon: 'none'
      })
      return
    }

    wx.showLoading({
      title: '登录中...'
    })

    wx.request({
      url: app.globalData.apiBase + '/api/auth/phone-login',
      method: 'POST',
      data: {
        phone: this.data.phone,
        code: this.data.code
      },
      success: (res) => {
        const { data } = res.data

        // 保存用户信息和 token
        app.globalData.token = data.token
        app.globalData.userInfo = data.user_info

        wx.setStorageSync('token', data.token)
        wx.setStorageSync('userInfo', data.user_info)

        wx.hideLoading()

        wx.showToast({
          title: '登录成功',
          icon: 'success'
        })

        // 跳转到首页
        setTimeout(() => {
          wx.switchTab({
            url: '/pages/index/index'
          })
        }, 1500)
      },
      fail: (err) => {
        wx.hideLoading()
        wx.showToast({
          title: err.errMsg || '登录失败',
          icon: 'none'
        })
      }
    })
  },

  validatePhone(phone) {
    const reg = /^1[3-9]\d{9}$/
    return reg.test(phone)
  },

  showAgreement() {
    wx.navigateTo({
      url: '/pages/webview/webview?url=/static/agreement.html'
    })
  },

  showPrivacy() {
    wx.navigateTo({
      url: '/pages/webview/webview?url=/static/privacy.html'
    })
  }
})
