// pages/index/index.js
Page({
  data: {
    motto: '宁律师 - 您的智能法律助手',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    features: [
      {
        icon: '🔒',
        title: '证据脱敏',
        desc: '快速脱敏敏感信息，保护隐私',
        path: '/pages/desensitize/desensitize'
      },
      {
        icon: '⚖️',
        title: '法律咨询',
        desc: '专业法律问题解答',
        path: '/pages/consult/consult'
      },
      {
        icon: '📄',
        title: '合同起草',
        desc: '快速生成各类合同',
        path: '/pages/contract/contract?mode=draft'
      },
      {
        icon: '🔍',
        title: '合同审查',
        desc: '智能审查合同风险',
        path: '/pages/contract/contract?mode=review'
      }
    ]
  },

  onLoad() {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },

  getUserInfo(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },

  navigateToFeature(e) {
    const path = e.currentTarget.dataset.path
    wx.navigateTo({
      url: path,
      fail() {
        wx.showToast({
          title: '功能开发中',
          icon: 'none'
        })
      }
    })
  }
})
