// 套餐管理页面
Page({
  data: {
    currentPlan: {
      subscription_type: 'basic',
      subscription_name: '基础版',
      subscription_price: 0,
      subscription_end_at: null,
      is_expired: false,
      features: [],
      modules: [],
      limits: {},
      usage_stats: {}
    },
    availablePlans: [
      {
        id: 'basic',
        name: '基础版',
        price: 0,
        duration: 30,
        description: '适合个人用户的基础法律咨询服务',
        features: [
          '法律咨询服务',
          '隐私脱敏功能',
          '10次/月咨询次数',
          '历史记录查询'
        ]
      },
      {
        id: 'premium',
        name: '专业版',
        price: 99,
        duration: 30,
        description: '适合专业人士和企业用户，提供全面的合同服务',
        features: [
          '无限次法律咨询',
          '隐私脱敏功能',
          '合同起草功能',
          '合同审查功能',
          '历史记录查询',
          '优先技术支持'
        ]
      },
      {
        id: 'enterprise',
        name: '企业版',
        price: 999,
        duration: 30,
        description: '适合企业用户，提供全方位的风险管理和签约服务',
        features: [
          '无限次法律咨询',
          '隐私脱敏功能',
          '合同起草功能',
          '合同审查功能',
          '风险扫描功能',
          '合规检查功能',
          '电子签约功能',
          '合同管理功能',
          '历史记录查询',
          '专属客服支持',
          '数据导出功能',
          '团队协作功能'
        ]
      }
    ],
    selectedPlan: null,
    loading: false
  },

  async onLoad(options) {
    console.log('套餐管理页面加载')
    
    // 如果从其他页面跳转过来，可能有预选的套餐
    if (options.plan) {
      this.setData({
        selectedPlan: options.plan
      })
    }
    
    await this.loadCurrentPlan()
    await this.loadAvailablePlans()
  },

  async onShow() {
    // 页面显示时刷新数据
    await this.loadCurrentPlan()
  },

  // 加载当前套餐
  async loadCurrentPlan() {
    this.setData({ loading: true })

    try {
      const userId = wx.getStorageSync('user_id')
      if (!userId) {
        wx.navigateTo({
          url: '/pages/login/login'
        })
        return
      }

      const res = await wx.request({
        url: `${getApp().globalData.apiBaseUrl}/api/user/subscription`,
        method: 'GET',
        data: { user_id: userId }
      })

      if (res.data.success) {
        const plan = res.data.data
        // 格式化到期时间
        if (plan.subscription_end_at) {
          const endDate = new Date(plan.subscription_end_at)
          plan.formatted_end_date = this.formatDate(endDate)
          plan.days_remaining = this.calculateDaysRemaining(endDate)
        }

        this.setData({
          currentPlan: plan
        })
      } else {
        wx.showToast({
          title: res.data.error || '加载失败',
          icon: 'none'
        })
      }
    } catch (err) {
      console.error('加载当前套餐失败:', err)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
    } finally {
      this.setData({ loading: false })
    }
  },

  // 加载可用套餐
  async loadAvailablePlans() {
    try {
      const res = await wx.request({
        url: `${getApp().globalData.apiBaseUrl}/api/subscription/plans`,
        method: 'GET'
      })

      if (res.data.success) {
        this.setData({
          availablePlans: res.data.data
        })
      }
    } catch (err) {
      console.error('加载可用套餐失败:', err)
    }
  },

  // 选择套餐
  handleSelectPlan(e) {
    const planId = e.currentTarget.dataset.plan
    this.setData({
      selectedPlan: planId
    })
  },

  // 升级套餐
  async handleUpgrade() {
    if (!this.data.selectedPlan) {
      wx.showToast({
        title: '请选择套餐',
        icon: 'none'
      })
      return
    }

    const userId = wx.getStorageSync('user_id')
    const plan = this.data.availablePlans.find(p => p.id === this.data.selectedPlan)

    if (!plan) {
      wx.showToast({
        title: '套餐不存在',
        icon: 'none'
      })
      return
    }

    // 检查是否是当前套餐
    if (plan.id === this.data.currentPlan.subscription_type) {
      wx.showToast({
        title: '您已经是此套餐',
        icon: 'none'
      })
      return
    }

    // 检查是否是降级
    const planLevels = { basic: 1, premium: 2, enterprise: 3 }
    if (planLevels[plan.id] < planLevels[this.data.currentPlan.subscription_type]) {
      wx.showModal({
        title: '确认降级',
        content: `确定要从${this.data.currentPlan.subscription_name}降级到${plan.name}吗？降级后部分功能将不可用。`,
        success: (res) => {
          if (res.confirm) {
            this.doDowngrade(plan.id)
          }
        }
      })
      return
    }

    // 升级确认
    wx.showModal({
      title: '确认升级',
      content: `确定要升级到${plan.name}吗？费用为¥${plan.price}/${plan.duration}天`,
      confirmText: '确认升级',
      success: (res) => {
        if (res.confirm) {
          this.doUpgrade(plan.id)
        }
      }
    })
  },

  // 执行升级
  async doUpgrade(planId) {
    wx.showLoading({
      title: '升级中...'
    })

    try {
      const userId = wx.getStorageSync('user_id')
      const res = await wx.request({
        url: `${getApp().globalData.apiBaseUrl}/api/subscription/upgrade`,
        method: 'POST',
        data: {
          user_id: userId,
          plan: planId
        }
      })

      wx.hideLoading()

      if (res.data.success) {
        wx.showToast({
          title: '升级成功',
          icon: 'success'
        })
        
        // 刷新数据
        await this.loadCurrentPlan()
        
        // 清除选择
        this.setData({
          selectedPlan: null
        })
      } else {
        wx.showToast({
          title: res.data.error || '升级失败',
          icon: 'none'
        })
      }
    } catch (err) {
      wx.hideLoading()
      console.error('升级失败:', err)
      wx.showToast({
        title: '升级失败',
        icon: 'none'
      })
    }
  },

  // 执行降级
  async doDowngrade(planId) {
    wx.showLoading({
      title: '降级中...'
    })

    try {
      const userId = wx.getStorageSync('user_id')
      const res = await wx.request({
        url: `${getApp().globalData.apiBaseUrl}/api/subscription/downgrade`,
        method: 'POST',
        data: {
          user_id: userId,
          plan: planId
        }
      })

      wx.hideLoading()

      if (res.data.success) {
        wx.showToast({
          title: '降级成功',
          icon: 'success'
        })
        
        // 刷新数据
        await this.loadCurrentPlan()
        
        // 清除选择
        this.setData({
          selectedPlan: null
        })
      } else {
        wx.showToast({
          title: res.data.error || '降级失败',
          icon: 'none'
        })
      }
    } catch (err) {
      wx.hideLoading()
      console.error('降级失败:', err)
      wx.showToast({
        title: '降级失败',
        icon: 'none'
      })
    }
  },

  // 查看使用统计
  handleViewUsage() {
    wx.navigateTo({
      url: '/pages/subscription/usage/usage'
    })
  },

  // 查看可用功能
  handleViewFeatures() {
    wx.navigateTo({
      url: '/pages/subscription/features/features'
    })
  },

  // 格式化日期
  formatDate(date) {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  },

  // 计算剩余天数
  calculateDaysRemaining(endDate) {
    const now = new Date()
    const diff = endDate - now
    return Math.ceil(diff / (1000 * 60 * 60 * 24))
  },

  // 查看套餐详情
  handleViewDetail(e) {
    const planId = e.currentTarget.dataset.plan
    const plan = this.data.availablePlans.find(p => p.id === planId)
    
    wx.showModal({
      title: plan.name,
      content: plan.features.join('\n'),
      showCancel: false
    })
  }
})
