// pages/compliance/compliance.js
Page({
  data: {
    selectedType: 'contract',
    checkTypes: [
      { value: 'contract', name: '合同合规', icon: '📄' },
      { value: 'company', name: '企业合规', icon: '🏢' },
      { value: 'labor', name: '劳动合规', icon: '👥' },
      { value: 'tax', name: '税务合规', icon: '💰' }
    ],
    complianceItems: [
      {
        id: 1,
        title: '合同主体资格',
        desc: '检查合同双方是否具备合法的签约资格',
        passed: true
      },
      {
        id: 2,
        title: '合同条款完整性',
        desc: '检查合同是否包含必要的条款内容',
        passed: false
      },
      {
        id: 3,
        title: '违约责任明确性',
        desc: '检查违约责任是否明确具体',
        passed: true
      },
      {
        id: 4,
        title: '争议解决方式',
        desc: '检查是否约定了争议解决方式',
        passed: false
      },
      {
        id: 5,
        title: '保密条款完备性',
        desc: '检查保密条款是否完备',
        passed: true
      }
    ],
    failedItems: []
  },

  onLoad(options) {
    this.loadFailedItems()
  },

  // 计算通过数量
  get passedCount() {
    return this.data.complianceItems.filter(item => item.passed).length
  },

  // 计算总数量
  get totalItems() {
    return this.data.complianceItems.length
  },

  // 加载未通过项
  loadFailedItems() {
    const failed = this.data.complianceItems
      .filter(item => !item.passed)
      .map(item => ({
        ...item,
        reason: '缺少相关条款内容',
        suggestion: '建议补充完整的合同条款，确保合同的完整性和可执行性'
      }))

    this.setData({
      failedItems: failed
    })
  },

  // 选择检查类型
  selectType(e) {
    const value = e.currentTarget.dataset.value
    this.setData({
      selectedType: value
    })
  },

  // 开始检查
  startCheck() {
    wx.showLoading({
      title: '检查中...'
    })

    setTimeout(() => {
      wx.hideLoading()
      wx.showToast({
        title: '检查完成',
        icon: 'success'
      })
    }, 1500)
  },

  // 查看详情
  viewDetails() {
    wx.showToast({
      title: '查看详情',
      icon: 'none'
    })
  }
})
