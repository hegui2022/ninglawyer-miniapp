// pages/scan/scan.js
const app = getApp()

Page({
  data: {
    selectedType: 'contract',
    scanTypes: [
      {
        value: 'contract',
        name: '合同合规检查',
        desc: '检查合同条款的合法性和合规性',
        icon: '/images/type-contract.png'
      },
      {
        value: 'company',
        name: '企业资质审查',
        desc: '审查企业资质和信用状况',
        icon: '/images/type-company.png'
      },
      {
        value: 'legal',
        name: '法律风险评估',
        desc: '评估法律风险和潜在问题',
        icon: '/images/type-legal.png'
      },
      {
        value: 'compliance',
        name: '合规性检查',
        desc: '全面检查业务合规性',
        icon: '/images/type-compliance.png'
      }
    ],
    scope: 'all',
    scopeOptions: [
      { value: 'all', name: '全部' },
      { value: 'current', name: '当前项目' },
      { value: 'recent', name: '最近7天' },
      { value: 'custom', name: '自定义' }
    ],
    scanOptions: [
      { key: 'deep', name: '深度扫描', desc: '进行更详细的分析', checked: false },
      { key: 'history', name: '历史对比', desc: '与历史数据对比', checked: true },
      { key: 'suggestion', name: '提供建议', desc: '提供改进建议', checked: true }
    ],
    scanning: false,
    progress: 0,
    currentTask: '',
    scanResult: null,
    risks: []
  },

  onLoad(options) {
    const id = options.id
    if (id) {
      // 加载历史扫描记录
      this.loadHistoryScan(id)
    }
  },

  // 选择扫描类型
  selectType(e) {
    const value = e.currentTarget.dataset.value
    this.setData({
      selectedType: value
    })
  },

  // 选择扫描范围
  selectScope(e) {
    const value = e.currentTarget.dataset.value
    this.setData({
      scope: value
    })
  },

  // 切换扫描选项
  toggleOption(e) {
    const key = e.currentTarget.dataset.key
    const options = this.data.scanOptions.map(item => {
      if (item.key === key) {
        return { ...item, checked: !item.checked }
      }
      return item
    })
    this.setData({
      scanOptions: options
    })
  },

  // 开始扫描
  startScan() {
    if (!this.data.selectedType) {
      wx.showToast({
        title: '请选择扫描类型',
        icon: 'none'
      })
      return
    }

    this.setData({
      scanning: true,
      progress: 0,
      currentTask: '正在初始化...',
      scanResult: null,
      risks: []
    })

    this.simulateScan()
  },

  // 模拟扫描过程
  simulateScan() {
    const tasks = [
      '正在收集数据...',
      '正在分析合同条款...',
      '正在检查合规性...',
      '正在评估风险...',
      '正在生成报告...'
    ]

    let index = 0
    const interval = setInterval(() => {
      if (index < tasks.length) {
        this.setData({
          progress: Math.floor((index + 1) / tasks.length * 100),
          currentTask: tasks[index]
        })
        index++
      } else {
        clearInterval(interval)
        this.showScanResult()
      }
    }, 800)
  },

  // 显示扫描结果
  showScanResult() {
    // 模拟扫描结果
    const result = {
      level: 'medium',
      levelText: '中风险',
      total: 25,
      high: 3,
      medium: 8,
      low: 14
    }

    // 模拟风险列表
    const risks = [
      {
        id: 1,
        title: '合同条款不完整',
        desc: '缺少违约责任条款，建议补充',
        level: 'high',
        levelText: '高风险'
      },
      {
        id: 2,
        title: '履约期限不明确',
        desc: '履约期限描述模糊，可能导致纠纷',
        level: 'medium',
        levelText: '中风险'
      },
      {
        id: 3,
        title: '付款方式不规范',
        desc: '付款方式缺少保障条款',
        level: 'medium',
        levelText: '中风险'
      },
      {
        id: 4,
        title: '争议解决方式缺失',
        desc: '未约定争议解决方式',
        level: 'low',
        levelText: '低风险'
      },
      {
        id: 5,
        title: '保密条款不足',
        desc: '保密条款范围过窄',
        level: 'low',
        levelText: '低风险'
      }
    ]

    // 更新全局数据
    app.updateRiskLevel(result.level)
    app.updateRiskCount({
      high: result.high,
      medium: result.medium,
      low: result.low
    })
    app.updateLastScanTime(new Date().toISOString())

    this.setData({
      scanning: false,
      scanResult: result,
      risks: risks
    })

    wx.showToast({
      title: '扫描完成',
      icon: 'success'
    })
  },

  // 重新扫描
  rescan() {
    this.setData({
      scanResult: null,
      risks: []
    })
  },

  // 查看报告
  viewReport() {
    wx.navigateTo({
      url: '/pages/report/report'
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

  // 加载历史扫描记录
  loadHistoryScan(id) {
    console.log('加载历史扫描记录', id)
    // 这里可以从后端加载历史扫描记录
  }
})
