// pages/report/report.js
Page({
  data: {
    reportDate: '',
    summary: {
      high: 3,
      medium: 8,
      low: 14
    },
    trendData: [
      { month: '1月', value: 20, color: '#07C160' },
      { month: '2月', value: 35, color: '#FF9800' },
      { month: '3月', value: 25, color: '#07C160' },
      { month: '4月', value: 45, color: '#F44336' },
      { month: '5月', value: 30, color: '#FF9800' },
      { month: '6月', value: 25, color: '#07C160' }
    ],
    categories: [
      {
        name: '合同风险',
        desc: '合同条款、履约等风险',
        icon: '📄',
        count: 12,
        color: '#F44336'
      },
      {
        name: '合规风险',
        desc: '法律法规、政策合规',
        icon: '⚖️',
        count: 5,
        color: '#FF9800'
      },
      {
        name: '操作风险',
        desc: '内部流程、操作规范',
        icon: '🔧',
        count: 4,
        color: '#2196F3'
      },
      {
        name: '信用风险',
        desc: '合作方信用状况',
        icon: '📊',
        count: 4,
        color: '#07C160'
      }
    ],
    tabs: [
      { name: '全部', value: 'all' },
      { name: '高风险', value: 'high' },
      { name: '中风险', value: 'medium' },
      { name: '低风险', value: 'low' }
    ],
    activeTab: 'all',
    risks: [
      {
        id: 1,
        title: '合同条款不完整',
        desc: '缺少违约责任条款，建议补充',
        level: 'high',
        levelText: '高风险',
        time: '2025-01-09 10:30',
        source: '自动扫描'
      },
      {
        id: 2,
        title: '履约期限不明确',
        desc: '履约期限描述模糊，可能导致纠纷',
        level: 'high',
        levelText: '高风险',
        time: '2025-01-09 10:30',
        source: '自动扫描'
      },
      {
        id: 3,
        title: '付款方式不规范',
        desc: '付款方式缺少保障条款',
        level: 'medium',
        levelText: '中风险',
        time: '2025-01-09 10:30',
        source: '自动扫描'
      },
      {
        id: 4,
        title: '争议解决方式缺失',
        desc: '未约定争议解决方式',
        level: 'low',
        levelText: '低风险',
        time: '2025-01-09 10:30',
        source: '自动扫描'
      },
      {
        id: 5,
        title: '保密条款不足',
        desc: '保密条款范围过窄',
        level: 'low',
        levelText: '低风险',
        time: '2025-01-09 10:30',
        source: '自动扫描'
      }
    ],
    suggestions: [
      {
        id: 1,
        title: '完善合同条款',
        desc: '补充违约责任、争议解决等关键条款，确保合同完整性和可执行性。'
      },
      {
        id: 2,
        title: '明确履约期限',
        desc: '在合同中明确约定履约期限和关键节点，避免因期限模糊导致纠纷。'
      },
      {
        id: 3,
        title: '加强合规管理',
        desc: '建立合规管理体系，定期进行合规检查，确保业务符合法律法规要求。'
      }
    ]
  },

  onLoad(options) {
    this.loadData()
  },

  // 加载数据
  loadData() {
    const now = new Date()
    const dateStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
    this.setData({
      reportDate: dateStr
    })
  },

  // 切换标签
  switchTab(e) {
    const value = e.currentTarget.dataset.value
    this.setData({
      activeTab: value
    })
  },

  // 计算过滤后的风险
  get filteredRisks() {
    if (this.data.activeTab === 'all') {
      return this.data.risks
    }
    return this.data.risks.filter(risk => risk.level === this.data.activeTab)
  },

  // 查看分类
  viewCategory(e) {
    const name = e.currentTarget.dataset.name
    wx.showToast({
      title: `查看${name}`,
      icon: 'none'
    })
  },

  // 查看风险详情
  viewRiskDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({
      title: '风险详情',
      content: '查看完整的风险详情和改进建议',
      showCancel: false
    })
  },

  // 导出报告
  exportReport() {
    wx.showLoading({
      title: '导出中...'
    })

    setTimeout(() => {
      wx.hideLoading()
      wx.showToast({
        title: '导出成功',
        icon: 'success'
      })
    }, 1500)
  },

  // 分享报告
  shareReport() {
    wx.showShareMenu({
      withShareTicket: true
    })
  }
})
