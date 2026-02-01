// 怎么判页面逻辑
const API_BASE = 'http://localhost:5000/api/v1/how_to_judge'

Page({
  data: {
    activeTab: 0,  // 当前选中的tab
    tabs: [
      { name: '裁判观点', icon: '/assets/icon-opinion.png' },
      { name: '判例检索', icon: '/assets/icon-case.png' },
      { name: '类案查询', icon: '/assets/icon-similar.png' },
      { name: '胜诉率', icon: '/assets/icon-win-rate.png' }
    ],
    loading: false,
    
    // 裁判观点
    opinionQuery: '',
    opinionResult: null,
    
    // 判例检索
    caseKeywords: '',
    cases: [],
    searched: false,
    showFilters: true,
    courtLevel: '',
    courtLevels: ['基层法院', '中级法院', '高级法院', '最高人民法院'],
    caseType: '',
    caseTypes: ['民事', '刑事', '行政'],
    
    // 类案查询
    caseDescription: '',
    similarCases: [],
    judgmentPatterns: '',
    winRate: '',
    recommendations: '',
    
    // 胜诉率分析
    selectedCaseType: '',
    caseTypeOptions: ['房屋买卖合同纠纷', '离婚纠纷', '劳动争议', '借款合同纠纷', '交通事故纠纷'],
    winRateAnalysis: null
  },

  onLoad() {
    console.log('怎么判页面加载')
  },

  // 返回
  onBack() {
    wx.navigateBack()
  },

  // 切换tab
  onTabChange(e) {
    const index = e.currentTarget.dataset.index
    this.setData({
      activeTab: index
    })
  },

  // ========================================
  // 裁判观点查询
  // ========================================
  onOpinionInput(e) {
    this.setData({
      opinionQuery: e.detail.value
    })
  },

  async onOpinionSearch() {
    if (!this.data.opinionQuery.trim()) {
      wx.showToast({
        title: '请输入查询内容',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      const res = await wx.request({
        url: `${API_BASE}/judge/opinion`,
        method: 'POST',
        data: {
          query: this.data.opinionQuery,
          user_id: `user_${Date.now()}`
        },
        header: {
          'content-type': 'application/json'
        }
      })

      if (res.data.success) {
        this.setData({
          opinionResult: res.data.data
        })
      } else {
        throw new Error(res.data.message || '查询失败')
      }
    } catch (err) {
      console.error('裁判观点查询失败', err)
      wx.showToast({
        title: '查询失败',
        icon: 'none'
      })
    } finally {
      this.setData({ loading: false })
    }
  },

  // ========================================
  // 判例检索
  // ========================================
  onCaseInput(e) {
    this.setData({
      caseKeywords: e.detail.value
    })
  },

  onCourtLevelChange(e) {
    this.setData({
      courtLevel: this.data.courtLevels[e.detail.value]
    })
  },

  onCaseTypeChange(e) {
    this.setData({
      caseType: this.data.caseTypes[e.detail.value]
    })
  },

  async onCaseSearch() {
    if (!this.data.caseKeywords.trim()) {
      wx.showToast({
        title: '请输入关键词',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      const res = await wx.request({
        url: `${API_BASE}/judge/cases`,
        method: 'POST',
        data: {
          keywords: this.data.caseKeywords,
          user_id: `user_${Date.now()}`,
          filters: {
            court: this.data.courtLevel,
            case_type: this.data.caseType
          }
        },
        header: {
          'content-type': 'application/json'
        }
      })

      if (res.data.success) {
        this.setData({
          cases: res.data.data.cases,
          searched: true
        })
      } else {
        throw new Error(res.data.message || '检索失败')
      }
    } catch (err) {
      console.error('判例检索失败', err)
      wx.showToast({
        title: '检索失败',
        icon: 'none'
      })
    } finally {
      this.setData({ loading: false })
    }
  },

  onCaseDetail(e) {
    const caseData = e.currentTarget.dataset.case
    wx.showModal({
      title: caseData.case_title,
      content: `案号: ${caseData.case_number}\n法院: ${caseData.court}\n裁判结果: ${caseData.result}`,
      showCancel: false
    })
  },

  // ========================================
  // 类案查询
  // ========================================
  onCaseDescriptionInput(e) {
    this.setData({
      caseDescription: e.detail.value
    })
  },

  async onSimilarCaseSearch() {
    if (!this.data.caseDescription.trim()) {
      wx.showToast({
        title: '请描述案件情况',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      const res = await wx.request({
        url: `${API_BASE}/judge/similar_cases`,
        method: 'POST',
        data: {
          case_description: this.data.caseDescription,
          user_id: `user_${Date.now()}`
        },
        header: {
          'content-type': 'application/json'
        }
      })

      if (res.data.success) {
        this.setData({
          similarCases: res.data.data.similar_cases,
          judgmentPatterns: res.data.data.judgment_patterns,
          winRate: res.data.data.win_rate,
          recommendations: res.data.data.recommendations
        })
      } else {
        throw new Error(res.data.message || '查询失败')
      }
    } catch (err) {
      console.error('类案查询失败', err)
      wx.showToast({
        title: '查询失败',
        icon: 'none'
      })
    } finally {
      this.setData({ loading: false })
    }
  },

  onSimilarCaseDetail(e) {
    const caseData = e.currentTarget.dataset.case
    wx.showModal({
      title: caseData.case_title,
      content: `法院: ${caseData.court}\n裁判结果: ${caseData.result}`,
      showCancel: false
    })
  },

  // ========================================
  // 胜诉率分析
  // ========================================
  onCaseTypeSelect(e) {
    this.setData({
      selectedCaseType: this.data.caseTypeOptions[e.detail.value]
    })
  },

  async onWinRateAnalyze() {
    if (!this.data.selectedCaseType) {
      wx.showToast({
        title: '请选择案件类型',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      const res = await wx.request({
        url: `${API_BASE}/judge/win_rate`,
        method: 'POST',
        data: {
          case_type: this.data.selectedCaseType,
          user_id: `user_${Date.now()}`
        },
        header: {
          'content-type': 'application/json'
        }
      })

      if (res.data.success) {
        const winRateAnalysis = res.data.data
        // 处理by_court数据，转换为数组格式
        const courtArray = Object.entries(winRateAnalysis.by_court).map(([court, rate]) => ({
          court,
          rate
        }))
        
        this.setData({
          winRateAnalysis: {
            ...winRateAnalysis,
            by_court: courtArray
          }
        })
      } else {
        throw new Error(res.data.message || '分析失败')
      }
    } catch (err) {
      console.error('胜诉率分析失败', err)
      wx.showToast({
        title: '分析失败',
        icon: 'none'
      })
    } finally {
      this.setData({ loading: false })
    }
  }
})
