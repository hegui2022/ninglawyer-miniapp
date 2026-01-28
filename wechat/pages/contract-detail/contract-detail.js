// pages/contract-detail/contract-detail.js
const app = getApp();

Page({
  data: {
    contractId: null,
    contract: {},
    reviewData: {
      has_review: false
    },
    loading: false
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ contractId: options.id });
      this.loadContractDetail();
      this.loadContractReview();
    }
  },

  // 加载合同详情
  loadContractDetail() {
    this.setData({ loading: true });

    app.request({
      url: `/contract/${this.data.contractId}`,
      method: 'GET',
      success: (res) => {
        if (res.code === 0 && res.data) {
          const contract = {
            ...res.data,
            contract_type_name: this.getContractTypeName(res.data.contract_type),
            created_at: this.formatDate(res.data.created_at)
          };
          this.setData({ contract });
        }
      },
      fail: (err) => {
        console.error('加载合同详情失败', err);
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

  // 加载审查记录
  loadContractReview() {
    app.request({
      url: `/contract/${this.data.contractId}/review`,
      method: 'GET',
      success: (res) => {
        if (res.code === 0 && res.data) {
          const reviewData = {
            has_review: res.data.has_review,
            overall_risk: res.data.overall_risk,
            high_risks: res.data.high_risks,
            medium_risks: res.data.medium_risks,
            low_risks: res.data.low_risks,
            risk_level: this.getRiskLevel(res.data.overall_risk),
            review_id: res.data.review_id
          };
          this.setData({ reviewData });
        }
      },
      fail: (err) => {
        console.error('加载审查记录失败', err);
      }
    });
  },

  // 审查合同
  reviewContract() {
    wx.showLoading({ title: '审查中...' });

    app.request({
      url: `/contract/${this.data.contractId}/review`,
      method: 'POST',
      success: (res) => {
        if (res.code === 0 && res.data) {
          wx.hideLoading();
          wx.showToast({
            title: '审查完成',
            icon: 'success'
          });
          
          // 刷新审查记录
          this.loadContractReview();
        }
      },
      fail: (err) => {
        wx.hideLoading();
        console.error('审查失败', err);
        wx.showToast({
          title: '审查失败',
          icon: 'none'
        });
      }
    });
  },

  // 编辑合同
  editContract() {
    wx.navigateTo({
      url: `/pages/contract-edit/contract-edit?id=${this.data.contractId}`
    });
  },

  // 跳转到审查详情页面
  goToReview() {
    wx.navigateTo({
      url: `/pages/contract-review/contract-review?id=${this.data.contractId}`
    });
  },

  // 获取合同类型名称
  getContractTypeName(type) {
    const typeMap = {
      'standard': '标准劳动合同',
      'parttime': '非全日制用工合同',
      'intern': '实习协议',
      'retired': '退休返聘协议',
      'project': '项目制合同',
      'dispatch': '劳务派遣合同'
    };
    return typeMap[type] || type;
  },

  // 获取风险等级
  getRiskLevel(risk) {
    if (risk === '高风险') return 'high';
    if (risk === '中风险' || risk === '中高风险') return 'medium';
    return 'low';
  },

  // 格式化日期
  formatDate(dateStr) {
    const date = new Date(dateStr);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
});
