// 案例详情页面
const API_BASE = 'http://localhost:5000/api/v1/legal_instructor'

Page({
  data: {
    caseId: null,
    caseData: null,
    loading: true
  },

  onLoad(options) {
    const { id } = options
    if (id) {
      this.setData({ caseId: id })
      this.loadCaseDetail()
    } else {
      wx.showToast({
        title: '案例ID不存在',
        icon: 'none'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }
  },

  // 加载案例详情
  async loadCaseDetail() {
    this.setData({ loading: true })

    try {
      const res = await wx.request({
        url: `${API_BASE}/cases/${this.data.caseId}`,
        method: 'GET',
        header: {
          'content-type': 'application/json'
        }
      })

      if (res.data.success) {
        this.setData({
          caseData: res.data.data,
          loading: false
        })
      } else {
        throw new Error(res.data.message || '加载失败')
      }
    } catch (err) {
      console.error('加载案例详情失败', err)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
      this.setData({ loading: false })
    }
  },

  // 返回
  onBack() {
    wx.navigateBack()
  },

  // 复制文本
  onCopyText(e) {
    const text = e.currentTarget.dataset.text
    wx.setClipboardData({
      data: text,
      success() {
        wx.showToast({
          title: '已复制',
          icon: 'success'
        })
      }
    })
  },

  // 格式化日期
  formatDate(dateStr) {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
  }
})
