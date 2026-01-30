const app = getApp()

Page({
  data: {
    activeTab: 'consultation',
    selectedDomain: '',
    domains: [
      { id: '', name: '全部' },
      { id: 'civil', name: '民事' },
      { id: 'criminal', name: '刑事' },
      { id: 'company', name: '公司' },
      { id: 'labor', name: '劳动' },
      { id: 'marriage', name: '婚姻' },
      { id: 'ip', name: '知识产权' },
      { id: 'contract', name: '合同' },
      { id: 'other', name: '其他' }
    ],
    records: [],
    page: 0,
    pageSize: 20,
    loading: false,
    loadingMore: false,
    hasMore: true
  },

  onLoad() {
    this.loadRecords()
  },

  onShow() {
    // 从其他页面返回时刷新
    if (this.data.records.length > 0) {
      this.refreshRecords()
    }
  },

  switchTab(e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({ 
      activeTab: tab,
      selectedDomain: '',
      records: [],
      page: 0,
      hasMore: true
    })
    this.loadRecords()
  },

  filterByDomain(e) {
    const id = e.currentTarget.dataset.id
    this.setData({ 
      selectedDomain: id,
      records: [],
      page: 0,
      hasMore: true
    })
    this.loadRecords()
  },

  async loadRecords() {
    if (this.data.loading) return
    
    this.setData({ loading: true })

    try {
      const { activeTab, selectedDomain, page, pageSize } = this.data
      let records = []

      if (activeTab === 'consultation') {
        records = await this.loadConsultationRecords(selectedDomain, page, pageSize)
      } else if (activeTab === 'contract') {
        records = await this.loadContractRecords(page, pageSize)
      } else if (activeTab === 'desensitize') {
        records = await this.loadDesensitizeRecords(page, pageSize)
      }

      this.setData({
        records: records,
        loading: false,
        hasMore: records.length >= pageSize
      })
    } catch (error) {
      console.error('加载记录失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
    }
  },

  async loadConsultationRecords(domain, page, pageSize) {
    try {
      const result = await this.request('/api/consultation/records', {
        skip: page * pageSize,
        limit: pageSize,
        domain: domain || undefined
      })

      if (result.success) {
        return result.data.records.map(item => ({
          id: item.record_id,
          domain: item.domain,
          domainName: this.getDomainName(item.domain),
          question: item.question,
          answer: item.analysis || item.suggestions || '',
          time: this.formatTime(item.created_at)
        }))
      }
      return []
    } catch (error) {
      // 降级：从本地缓存读取
      const localRecords = wx.getStorageSync('consultation_records') || []
      return localRecords.map(item => ({
        id: item.id,
        domain: item.domain,
        domainName: this.getDomainName(item.domain),
        question: item.question,
        answer: item.answer,
        time: this.formatTime(item.time)
      }))
    }
  },

  async loadContractRecords(page, pageSize) {
    try {
      const result = await this.request('/api/contract/records', {
        skip: page * pageSize,
        limit: pageSize
      })

      if (result.success) {
        return result.data.records.map(item => ({
          id: item.record_id,
          contractType: item.contract_type,
          title: `${item.contract_type} - ${item.action}`,
          score: item.score || 0,
          riskCount: item.risks ? item.risks.length : 0,
          time: this.formatTime(item.created_at)
        }))
      }
      return []
    } catch (error) {
      return []
    }
  },

  async loadDesensitizeRecords(page, pageSize) {
    try {
      const result = await this.request('/api/desensitize/records', {
        skip: page * pageSize,
        limit: pageSize
      })

      if (result.success) {
        return result.data.records.map(item => ({
          id: item.record_id,
          original: item.original_text.substring(0, 50) + '...',
          desensitized: item.desensitized_text.substring(0, 50) + '...',
          time: this.formatTime(item.created_at)
        }))
      }
      return []
    } catch (error) {
      return []
    }
  },

  loadMore() {
    if (this.data.loadingMore || !this.data.hasMore) return

    this.setData({ loadingMore: true })

    const { activeTab, selectedDomain, page, pageSize } = this.data
    const newPage = page + 1

    let records = []

    if (activeTab === 'consultation') {
      records = this.loadConsultationRecords(selectedDomain, newPage, pageSize)
    } else if (activeTab === 'contract') {
      records = this.loadContractRecords(newPage, pageSize)
    } else if (activeTab === 'desensitize') {
      records = this.loadDesensitizeRecords(newPage, pageSize)
    }

    records.then(newRecords => {
      this.setData({
        records: [...this.data.records, ...newRecords],
        page: newPage,
        loadingMore: false,
        hasMore: newRecords.length >= pageSize
      })
    })
  },

  refreshRecords() {
    this.setData({
      records: [],
      page: 0,
      hasMore: true
    })
    this.loadRecords()
  },

  viewDetail(e) {
    const { id, type } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/record-detail/record-detail?id=${id}&type=${type}`
    })
  },

  goToCreate() {
    wx.switchTab({
      url: '/pages/consultation/consultation'
    })
  },

  request(url, data) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: app.globalData.apiBase + url,
        method: 'GET',
        data: data,
        header: {
          'Authorization': `Bearer ${app.globalData.token || wx.getStorageSync('token')}`
        },
        success: (res) => {
          resolve(res.data)
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },

  getDomainName(domain) {
    const domainMap = {
      'civil': '民事',
      'criminal': '刑事',
      'company': '公司',
      'labor': '劳动',
      'marriage': '婚姻',
      'ip': '知识产权',
      'contract': '合同',
      'other': '其他'
    }
    return domainMap[domain] || '其他'
  },

  formatTime(dateStr) {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    const now = new Date()
    const diff = now - date

    if (diff < 60000) {
      return '刚刚'
    } else if (diff < 3600000) {
      return `${Math.floor(diff / 60000)}分钟前`
    } else if (diff < 86400000) {
      return `${Math.floor(diff / 3600000)}小时前`
    } else if (diff < 604800000) {
      return `${Math.floor(diff / 86400000)}天前`
    } else {
      return `${date.getMonth() + 1}/${date.getDate()}`
    }
  },

  onPullDownRefresh() {
    this.refreshRecords()
    wx.stopPullDownRefresh()
  }
})
