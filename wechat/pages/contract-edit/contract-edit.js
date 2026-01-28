// pages/contract-edit/contract-edit.js
const app = getApp();

Page({
  data: {
    contractId: null,
    contractData: {
      name: '',
      contract_type: '',
      party_a: '',
      party_b: '',
      start_date: '',
      end_date: '',
      probation_months: '',
      job_content: '',
      workplace: '',
      salary: '',
      payment_method: '',
      work_hours: '',
      has_insurance: true,
      has_housing_fund: true,
      has_confidentiality: false,
      has_non_compete: false,
      has_ip_clause: false,
      custom_clause: '',
      notes: ''
    },
    loading: false
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ contractId: options.id });
      this.loadContractDetail();
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
          const data = res.data;
          // 解析 contract_content 获取详细信息
          const content = data.contract_content || {};
          this.setData({
            contractData: {
              name: data.name || '',
              contract_type: data.contract_type || '',
              party_a: content.party_a || '',
              party_b: content.party_b || '',
              start_date: content.start_date || '',
              end_date: content.end_date || '',
              probation_months: content.probation_months || '',
              job_content: content.job_content || '',
              workplace: content.workplace || '',
              salary: content.salary || '',
              payment_method: content.payment_method || '',
              work_hours: content.work_hours || '',
              has_insurance: content.has_insurance !== false,
              has_housing_fund: content.has_housing_fund !== false,
              has_confidentiality: content.has_confidentiality || false,
              has_non_compete: content.has_non_compete || false,
              has_ip_clause: content.has_ip_clause || false,
              custom_clause: content.custom_clause || '',
              notes: data.notes || ''
            }
          });
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

  // 表单输入处理
  onNameChange(e) { this.setData({ 'contractData.name': e.detail.value }); },
  onPartyAChange(e) { this.setData({ 'contractData.party_a': e.detail.value }); },
  onPartyBChange(e) { this.setData({ 'contractData.party_b': e.detail.value }); },
  onStartDateChange(e) { this.setData({ 'contractData.start_date': e.detail.value }); },
  onEndDateChange(e) { this.setData({ 'contractData.end_date': e.detail.value }); },
  onProbationChange(e) { this.setData({ 'contractData.probation_months': e.detail.value }); },
  onJobContentChange(e) { this.setData({ 'contractData.job_content': e.detail.value }); },
  onWorkplaceChange(e) { this.setData({ 'contractData.workplace': e.detail.value }); },
  onSalaryChange(e) { this.setData({ 'contractData.salary': e.detail.value }); },
  onPaymentMethodChange(e) { this.setData({ 'contractData.payment_method': e.detail.value }); },
  onWorkHoursChange(e) { this.setData({ 'contractData.work_hours': e.detail.value }); },
  onNotesChange(e) { this.setData({ 'contractData.notes': e.detail.value }); },
  onCustomClauseChange(e) { this.setData({ 'contractData.custom_clause': e.detail.value }); },

  // 开关处理
  onInsuranceChange(e) { this.setData({ 'contractData.has_insurance': e.detail.value }); },
  onHousingFundChange(e) { this.setData({ 'contractData.has_housing_fund': e.detail.value }); },
  onConfidentialityChange(e) { this.setData({ 'contractData.has_confidentiality': e.detail.value }); },
  onNonCompeteChange(e) { this.setData({ 'contractData.has_non_compete': e.detail.value }); },
  onIpClauseChange(e) { this.setData({ 'contractData.has_ip_clause': e.detail.value }); },

  // 保存合同
  saveContract() {
    const { contractData, contractId } = this.data;

    // 基础验证
    if (!contractData.name) {
      wx.showToast({ title: '请输入合同名称', icon: 'none' });
      return;
    }
    if (!contractData.party_a) {
      wx.showToast({ title: '请输入甲方名称', icon: 'none' });
      return;
    }
    if (!contractData.party_b) {
      wx.showToast({ title: '请输入乙方姓名', icon: 'none' });
      return;
    }

    this.setData({ loading: true });

    app.request({
      url: `/contract/${contractId}`,
      method: 'PUT',
      data: {
        name: contractData.name,
        contract_content: {
          party_a: contractData.party_a,
          party_b: contractData.party_b,
          start_date: contractData.start_date,
          end_date: contractData.end_date,
          probation_months: contractData.probation_months,
          job_content: contractData.job_content,
          workplace: contractData.workplace,
          salary: contractData.salary,
          payment_method: contractData.payment_method,
          work_hours: contractData.work_hours,
          has_insurance: contractData.has_insurance,
          has_housing_fund: contractData.has_housing_fund,
          has_confidentiality: contractData.has_confidentiality,
          has_non_compete: contractData.has_non_compete,
          has_ip_clause: contractData.has_ip_clause,
          custom_clause: contractData.custom_clause
        },
        notes: contractData.notes
      },
      success: (res) => {
        if (res.code === 0) {
          wx.showToast({
            title: '保存成功',
            icon: 'success'
          });
          // 延迟返回
          setTimeout(() => {
            wx.navigateBack();
          }, 1500);
        } else {
          wx.showToast({
            title: res.message || '保存失败',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        console.error('保存失败', err);
        wx.showToast({
          title: '保存失败',
          icon: 'none'
        });
      },
      complete: () => {
        this.setData({ loading: false });
      }
    });
  },

  // 返回
  goBack() {
    wx.navigateBack();
  }
});
