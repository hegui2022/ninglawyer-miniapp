// pages/contract/contract.js
const app = getApp()

Page({
  data: {
    mode: 'draft', // draft起草, review审查
    contractType: '',
    contractContent: '',
    result: null,
    loading: false,
    types: {
      draft: [
        '房屋租赁合同',
        '借款合同',
        '买卖合同',
        '劳动合同'
      ],
      review: [
        '房屋租赁合同',
        '借款合同',
        '买卖合同',
        '劳动合同'
      ]
    },
    selectedType: ''
  },

  onLoad(options) {
    // 从参数获取模式
    if (options.mode) {
      this.setData({ mode: options.mode })
    }
  },

  // 选择合同类型
  onTypeSelect(e) {
    const type = e.currentTarget.dataset.type
    this.setData({ selectedType: type })
  },

  // 输入合同内容
  onContentInput(e) {
    this.setData({ contractContent: e.detail.value })
  },

  // 起草合同
  async onDraft() {
    if (!this.data.selectedType) {
      wx.showToast({
        title: '请选择合同类型',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      const res = await wx.request({
        url: `${app.globalData.apiBase}/api/contract/draft`,
        method: 'POST',
        data: {
          contract_type: this.data.selectedType
        },
        header: {
          'Authorization': `Bearer ${app.globalData.token || wx.getStorageSync('token')}`
        }
      })

      if (res.data.success) {
        const content = res.data.data.contract_content
        this.setData({
          result: content
        })
      } else {
        wx.showToast({
          title: res.data.error || '起草失败',
          icon: 'none'
        })
      }
    } catch (error) {
      console.error('起草失败:', error)
      wx.showToast({
        title: '网络错误，请检查连接',
        icon: 'none'
      })
    }

    this.setData({ loading: false })
  },

  // 审查合同
  async onReview() {
    if (!this.data.contractContent.trim()) {
      wx.showToast({
        title: '请输入合同内容',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      const res = await wx.request({
        url: `${app.globalData.apiBase}/api/contract/review`,
        method: 'POST',
        data: {
          contract_text: this.data.contractContent
        },
        header: {
          'Authorization': `Bearer ${app.globalData.token || wx.getStorageSync('token')}`
        }
      })

      if (res.data.success) {
        const data = res.data.data
        let result = `风险评分：${data.risk_score}\n\n`

        if (data.risks && data.risks.length > 0) {
          result += '发现的风险点：\n'
          data.risks.forEach((risk, index) => {
            result += `${index + 1}. ${risk.risk_type}：${risk.description}\n`
            result += `   建议：${risk.suggestion}\n\n`
          })
        }

        if (data.suggestions && data.suggestions.length > 0) {
          result += '修改建议：\n'
          data.suggestions.forEach((suggestion, index) => {
            result += `${index + 1}. ${suggestion}\n`
          })
        }

        this.setData({
          result: result
        })
      } else {
        wx.showToast({
          title: res.data.error || '审查失败',
          icon: 'none'
        })
      }
    } catch (error) {
      console.error('审查失败:', error)
      wx.showToast({
        title: '网络错误，请检查连接',
        icon: 'none'
      })
    }

    this.setData({ loading: false })
  },

  // 复制结果
  onCopyResult() {
    if (!this.data.result) return

    wx.setClipboardData({
      data: this.data.result,
      success() {
        wx.showToast({
          title: '已复制',
          icon: 'success'
        })
      }
    })
  },

  // 清空
  onClear() {
    this.setData({
      selectedType: '',
      contractContent: '',
      result: null
    })
  }
})
