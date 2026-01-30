const app = getApp()

Page({
  data: {
    userInfo: {},
    stats: {
      consultation_count: 0,
      contract_count: 0,
      desensitize_count: 0
    },
    unreadCount: 0
  },

  onLoad() {
    this.loadUserInfo()
    this.loadStats()
  },

  onShow() {
    this.loadUserInfo()
    this.loadStats()
  },

  loadUserInfo() {
    const userInfo = app.globalData.userInfo || wx.getStorageSync('userInfo') || {}
    this.setData({ userInfo })
  },

  async loadStats() {
    try {
      const result = await this.request('/api/records/stats')
      if (result.success) {
        this.setData({ stats: result.data })
      }
    } catch (error) {
      console.error('加载统计数据失败:', error)
    }
  },

  editProfile() {
    wx.navigateTo({
      url: '/pages/profile-edit/profile-edit'
    })
  },

  goToProfileDetail() {
    wx.navigateTo({
      url: '/pages/profile-detail/profile-detail'
    })
  },

  goToProfile() {
    wx.navigateTo({
      url: '/pages/profile-userfile/profile-userfile'
    })
  },

  bindPhone() {
    wx.navigateTo({
      url: '/pages/bind-phone/bind-phone'
    })
  },

  goToNotification() {
    wx.navigateTo({
      url: '/pages/notification/notification'
    })
  },

  goToSettings() {
    wx.navigateTo({
      url: '/pages/settings/settings'
    })
  },

  goToAbout() {
    wx.navigateTo({
      url: '/pages/about/about'
    })
  },

  goToFeedback() {
    wx.navigateTo({
      url: '/pages/feedback/feedback'
    })
  },

  goToHistory(e) {
    const tab = e.currentTarget.dataset.tab || 'consultation'
    wx.switchTab({
      url: '/pages/history/history'
    })
  },

  logout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      confirmColor: '#1890ff',
      success: (res) => {
        if (res.confirm) {
          this.doLogout()
        }
      }
    })
  },

  doLogout() {
    // 清除本地存储
    wx.removeStorageSync('token')
    wx.removeStorageSync('userInfo')
    app.globalData.token = null
    app.globalData.userInfo = null

    wx.showToast({
      title: '已退出登录',
      icon: 'success'
    })

    // 跳转到登录页
    setTimeout(() => {
      wx.reLaunch({
        url: '/pages/login/login'
      })
    }, 1500)
  },

  changeAvatar() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePath = res.tempFiles[0].tempFilePath
        this.uploadAvatar(tempFilePath)
      }
    })
  },

  async uploadAvatar(filePath) {
    wx.showLoading({ title: '上传中...' })

    try {
      const token = app.globalData.token || wx.getStorageSync('token')

      wx.uploadFile({
        url: app.globalData.apiBase + '/api/files/upload',
        filePath: filePath,
        name: 'file',
        formData: {
          category: 'avatar'
        },
        header: {
          'Authorization': `Bearer ${token}`
        },
        success: (uploadRes) => {
          const data = JSON.parse(uploadRes.data)
          if (data.success) {
            this.updateAvatar(data.data.file_id)
          } else {
            wx.showToast({
              title: '上传失败',
              icon: 'none'
            })
          }
        },
        fail: (err) => {
          wx.showToast({
            title: '上传失败',
            icon: 'none'
          })
        },
        complete: () => {
          wx.hideLoading()
        }
      })
    } catch (error) {
      wx.hideLoading()
      wx.showToast({
        title: '上传失败',
        icon: 'none'
      })
    }
  },

  async updateAvatar(fileId) {
    try {
      const result = await this.request('/api/user/profile', {
        avatar: fileId
      }, 'PUT')

      if (result.success) {
        // 更新本地用户信息
        const userInfo = { ...this.data.userInfo, avatar: fileId }
        this.setData({ userInfo })
        wx.setStorageSync('userInfo', userInfo)
        app.globalData.userInfo = userInfo

        wx.showToast({
          title: '更新成功',
          icon: 'success'
        })
      }
    } catch (error) {
      console.error('更新头像失败:', error)
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
        success: (res) => {
          resolve(res.data)
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  }
})
