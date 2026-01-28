// pages/contract-draft/contract-draft.js
const app = getApp();

Page({
  data: {
    step: 0,
    contractType: '',
    contractTypes: [
      { id: 'standard', name: '标准劳动合同', icon: '💼', description: '适用于正式员工，有试用期，缴纳社保' },
      { id: 'parttime', name: '非全日制用工合同', icon: '⏰', description: '适用于兼职，每天不超过4小时' },
      { id: 'intern', name: '实习协议', icon: '🎓', description: '适用于在校学生实习，有实习补贴和意外保险' },
      { id: 'retired', name: '退休返聘协议', icon: '👴', description: '适用于退休人员返聘，不缴纳社保' },
      { id: 'project', name: '项目制合同', icon: '📊', description: '适用于项目制合作，以完成项目为期限' },
      { id: 'dispatch', name: '劳务派遣合同', icon: '🤝', description: '适用于劳务派遣，三方关系' }
    ],
    formData: {
      contract_name: '',
      employer_name: '',
      employee_name: '',
      contract_content: ''
    },
    contractPreview: '',
    loading: false
  },

  onLoad(options) {
    if (options.type) {
      this.setData({ contractType: options.type, step: 1 });
    }
  },

  // 选择合同类型
  selectContractType(type) {
    this.setData({ contractType: type, step: 1 });
  },

  // 输入框变化
  onInputChange(e) {
    const field = e.currentTarget.dataset.field;
    const value = e.detail.value;
    this.setData({
      [`formData.${field}`]: value
    });
  },

  // 下一步
  nextStep() {
    if (this.data.step === 1) {
      // 验证表单
      if (!this.data.formData.contract_name.trim()) {
        wx.showToast({
          title: '请输入合同名称',
          icon: 'none'
        });
        return;
      }
      if (!this.data.formData.employer_name.trim()) {
        wx.showToast({
          title: '请输入用人单位名称',
          icon: 'none'
        });
        return;
      }
      if (!this.data.formData.employee_name.trim()) {
        wx.showToast({
          title: '请输入劳动者姓名',
          icon: 'none'
        });
        return;
      }

      // 生成合同预览
      this.generateContractPreview();
    }

    this.setData({ step: this.data.step + 1 });
  },

  // 上一步
  previousStep() {
    if (this.data.step > 0) {
      this.setData({ step: this.data.step - 1 });
    }
  },

  // 生成合同预览
  generateContractPreview() {
    const type = this.data.contractType;
    const formData = this.data.formData;
    
    let preview = '';
    
    if (formData.contract_content) {
      preview = formData.contract_content;
    } else {
      // 使用模板生成
      const typeName = this.getContractTypeName(type);
      preview = `# ${typeName}\n\n`;
      preview += `**甲方（用人单位）**：${formData.employer_name}\n\n`;
      preview += `**乙方（劳动者）**：${formData.employee_name}\n\n`;
      preview += `---\n\n`;
      preview += `（此处为合同正文内容，请根据实际情况填写）`;
    }
    
    this.setData({ contractPreview: preview });
  },

  // 保存合同
  saveContract() {
    if (!this.data.contractPreview) {
      wx.showToast({
        title: '合同内容不能为空',
        icon: 'none'
      });
      return;
    }

    wx.showLoading({ title: '保存中...' });

    app.request({
      url: '/contract/save',
      method: 'POST',
      data: {
        contract_name: this.data.formData.contract_name,
        contract_type: this.data.contractType,
        employer_name: this.data.formData.employer_name,
        employee_name: this.data.formData.employee_name,
        contract_content: this.data.contractPreview,
        additional_clauses: ''
      },
      success: (res) => {
        wx.hideLoading();
        if (res.code === 0 && res.data) {
          wx.showToast({
            title: '保存成功',
            icon: 'success'
          });
          
          setTimeout(() => {
            wx.switchTab({
              url: '/pages/contract-list/contract-list'
            });
          }, 1500);
        }
      },
      fail: (err) => {
        wx.hideLoading();
        console.error('保存合同失败', err);
        wx.showToast({
          title: '保存失败',
          icon: 'none'
        });
      }
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
  }
});
