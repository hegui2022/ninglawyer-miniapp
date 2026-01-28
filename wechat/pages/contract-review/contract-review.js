// pages/contract-review/contract-review.js
const app = getApp();

Page({
  data: {
    contractId: null,
    reviewData: {
      has_review: false,
      overall_risk: '',
      high_risks: 0,
      medium_risks: 0,
      low_risks: 0,
      risk_level: 'low',
      risk_icon: '✅',
      risk_desc: '暂无风险',
      risks: []
    },
    loading: false
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ contractId: options.id });
      this.loadContractReview();
    }
  },

  // 加载审查记录
  loadContractReview() {
    this.setData({ loading: true });

    app.request({
      url: `/contract/${this.data.contractId}/review`,
      method: 'GET',
      success: (res) => {
        if (res.code === 0 && res.data && res.data.has_review) {
          const data = res.data;
          const reviewData = {
            has_review: true,
            overall_risk: data.overall_risk,
            high_risks: data.high_risks,
            medium_risks: data.medium_risks,
            low_risks: data.low_risks,
            risk_level: this.getRiskLevel(data.overall_risk),
            risk_icon: this.getRiskIcon(data.overall_risk),
            risk_desc: this.getRiskDesc(data.overall_risk),
            risks: data.review_result?.risks || []
          };
          this.setData({ reviewData });
        }
      },
      fail: (err) => {
        console.error('加载审查记录失败', err);
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        });
      },
      complete: () => {
        this.setData({ loading: false });
      }
    });
  },

  // 获取风险等级
  getRiskLevel(risk) {
    if (risk === '高风险') return 'high';
    if (risk === '中风险' || risk === '中高风险') return 'medium';
    return 'low';
  },

  // 获取风险图标
  getRiskIcon(risk) {
    if (risk === '高风险') return '🔴';
    if (risk === '中风险' || risk === '中高风险') return '🟡';
    return '🟢';
  },

  // 获取风险描述
  getRiskDesc(risk) {
    if (risk === '高风险') return '存在严重法律风险，必须立即修改';
    if (risk === '中风险' || risk === '中高风险') return '存在一定法律风险，建议修改';
    return '风险较低，可考虑优化';
  },

  // 返回上一页
  goBack() {
    wx.navigateBack();
  },

  // 编辑合同
  editContract() {
    wx.navigateTo({
      url: `/pages/contract-edit/contract-edit?id=${this.data.contractId}`
    });
  }
});
