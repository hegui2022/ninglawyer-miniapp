// pages/consult/consult.js
const app = getApp()

Page({
  data: {
    question: '',
    result: null,
    loading: false,
    history: []
  },

  // 输入问题
  onQuestionInput(e) {
    this.setData({ question: e.detail.value })
  },

  // 提交咨询
  async onConsult() {
    if (!this.data.question.trim()) {
      wx.showToast({
        title: '请输入您的问题',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      // 调用后端API
      const res = await wx.request({
        url: `${app.globalData.apiConfig.baseUrl}/api/master/consult`,
        method: 'POST',
        data: {
          question: this.data.question
        },
        timeout: app.globalData.apiConfig.timeout
      })

      if (res.data.success) {
        const content = res.data.content || res.data.data

        // 添加到历史记录
        const historyItem = {
          question: this.data.question,
          answer: content,
          time: new Date().toLocaleString()
        }

        this.setData({
          result: content,
          history: [historyItem, ...this.data.history],
          question: ''
        })
      } else {
        wx.showToast({
          title: res.data.error || '咨询失败',
          icon: 'none'
        })
      }
    } catch (error) {
      console.error('咨询失败:', error)
      wx.showToast({
        title: '网络错误，请检查连接',
        icon: 'none'
      })
    }

    this.setData({ loading: false })
  },

  // 查看历史
  onViewHistory() {
    if (this.data.history.length === 0) {
      wx.showToast({
        title: '暂无历史记录',
        icon: 'none'
      })
      return
    }

    // 显示历史记录（简化版，实际可以使用弹窗或新页面）
    console.log('历史记录:', this.data.history)
  },

  // 复制答案
  onCopyAnswer(e) {
    const answer = e.currentTarget.dataset.answer
    wx.setClipboardData({
      data: answer,
      success() {
        wx.showToast({
          title: '已复制',
          icon: 'success'
        })
      }
    })
  },

  // 清空输入
  onClear() {
    this.setData({ question: '' })
  }
})
