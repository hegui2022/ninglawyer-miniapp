// 怎么判 - 智能分析页面（完整版）
Page({
  data: {
    caseType: '',
    caseDescription: '',
    amount: '',
    evidence: '',
    analyzing: false,
    analysisResult: null
  },
  
  onLoad() {
    
  },
  
  onCaseTypeChange(e) {
    this.setData({
      caseType: e.detail.value
    });
  },
  
  onDescriptionInput(e) {
    this.setData({
      caseDescription: e.detail.value
    });
  },
  
  onAmountInput(e) {
    this.setData({
      amount: e.detail.value
    });
  },
  
  onEvidenceInput(e) {
    this.setData({
      evidence: e.detail.value
    });
  },
  
  onAnalyze() {
    if (!this.data.caseType || !this.data.caseDescription) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      });
      return;
    }
    
    this.setData({ analyzing: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/analyze',
      method: 'POST',
      data: {
        dispute_type: this.data.caseType,
        description: this.data.caseDescription,
        amount: this.data.amount,
        evidence: this.data.evidence
      },
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            analysisResult: res.data.data,
            analyzing: false
          });
        }
      },
      fail: () => {
        this.setData({ analyzing: false });
        wx.showToast({
          title: '分析失败',
          icon: 'none'
        });
      }
    });
  },
  
  onSave() {
    if (!this.data.analysisResult) return;
    
    wx.showToast({
      title: '已保存',
      icon: 'success'
    });
  }
});
