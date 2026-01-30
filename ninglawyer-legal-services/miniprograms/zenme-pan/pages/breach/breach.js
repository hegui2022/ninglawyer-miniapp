// 违约判断页面
Page({
  data: {
    contractType: '',
    contractTypes: ['劳动合同', '买卖合同', '服务合同', '租赁合同', '其他'],
    breachType: '',
    breachTypes: ['未按时付款', '未按时交付', '质量不合格', '单方面解除', '其他违约'],
    description: '',
    contractDate: '',
    breachDate: '',
    amount: '',
    result: null,
    analyzing: false
  },
  
  onLoad() {
    this.loadHistory();
  },
  
  loadHistory() {
    // 加载历史判断记录
  },
  
  onContractTypeChange(e) {
    this.setData({
      contractType: this.data.contractTypes[e.detail.value]
    });
  },
  
  onBreachTypeChange(e) {
    this.setData({
      breachType: this.data.breachTypes[e.detail.value]
    });
  },
  
  onDescriptionInput(e) {
    this.setData({ description: e.detail.value });
  },
  
  onDateChange(e) {
    const field = e.currentTarget.dataset.field;
    this.setData({ [field]: e.detail.value });
  },
  
  onAmountInput(e) {
    this.setData({ amount: e.detail.value });
  },
  
  validateForm() {
    if (!this.data.contractType) {
      wx.showToast({ title: '请选择合同类型', icon: 'none' });
      return false;
    }
    if (!this.data.breachType) {
      wx.showToast({ title: '请选择违约类型', icon: 'none' });
      return false;
    }
    if (!this.data.description.trim()) {
      wx.showToast({ title: '请描述违约情况', icon: 'none' });
      return false;
    }
    return true;
  },
  
  onAnalyze() {
    if (!this.validateForm()) return;
    
    this.setData({ analyzing: true });
    
    // 模拟 AI 分析
    setTimeout(() => {
      const result = {
        isBreach: true,
        confidence: 0.92,
        breach: {
          type: this.data.breachType,
          severity: '严重',
          description: '根据您提供的信息，对方行为已构成违约'
        },
        lawBasis: [
          {
            law: '《中华人民共和国民法典》第五百七十七条',
            content: '当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。'
          },
          {
            law: '《中华人民共和国民法典》第五百八十三条',
            content: '当事人一方不履行合同义务或者履行合同义务不符合约定的，在履行义务或者采取补救措施后，对方还有其他损失的，应当赔偿损失。'
          }
        ],
        remedies: [
          '要求对方继续履行合同',
          '要求对方采取补救措施',
          '要求对方赔偿损失',
          '解除合同并要求赔偿'
        ],
        evidence: [
          '合同文本原件',
          '付款凭证或交付证明',
          '沟通记录（微信、邮件等）',
          '违约情况证明（照片、视频等）'
        ],
        recommendations: [
          '及时与对方沟通，要求履行义务',
          '保留相关证据，做好维权准备',
          '可先发送律师函进行催告',
          '如协商不成，可向法院提起诉讼'
        ]
      };
      
      this.setData({ 
        result,
        analyzing: false 
      });
      
      // 保存到历史记录
      this.saveHistory(result);
    }, 2000);
  },
  
  saveHistory(result) {
    const history = wx.getStorageSync('breachHistory') || [];
    history.unshift({
      id: Date.now(),
      contractType: this.data.contractType,
      breachType: this.data.breachType,
      result: result.isBreach ? '构成违约' : '不构成违约',
      date: new Date().toISOString().split('T')[0]
    });
    wx.setStorageSync('breachHistory', history.slice(0, 20)); // 保留最近20条
  },
  
  onReset() {
    this.setData({
      contractType: '',
      breachType: '',
      description: '',
      contractDate: '',
      breachDate: '',
      amount: '',
      result: null
    });
  },
  
  onGoRights() {
    wx.navigateTo({
      url: '/pages/rights/rights'
    });
  },
  
  onGoCases() {
    wx.navigateTo({
      url: '/pages/cases/cases?keyword=' + this.data.breachType
    });
  }
});
