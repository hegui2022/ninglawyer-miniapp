// 码上签约 - 合同起草页面
Page({
  data: {
    template: null,
    contractTitle: '',
    partyA: {
      name: '',
      address: '',
      contact: '',
      phone: ''
    },
    partyB: {
      name: '',
      idCard: '',
      phone: '',
      address: ''
    },
    contractTerm: {
      startDate: '',
      endDate: '',
      type: 'fixed' // fixed, indefinite, project
    },
    salary: {
      amount: '',
      payMethod: 'month', // month, day, project
      payDate: '10'
    },
    workContent: '',
    workPlace: '',
    workingHours: 'standard', // standard, flexible, shift
    socialInsurance: true,
    otherTerms: ''
  },
  
  onLoad(options) {
    if (options.template) {
      const template = JSON.parse(decodeURIComponent(options.template));
      this.setData({ template, contractTitle: template.name });
    }
  },
  
  // 输入框变化处理
  onInputChange(e) {
    const { field } = e.currentTarget.dataset;
    const { value } = e.detail;
    
    // 处理嵌套字段
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      this.setData({
        [parent]: {
          ...this.data[parent],
          [child]: value
        }
      });
    } else {
      this.setData({ [field]: value });
    }
  },
  
  // 日期选择
  onDateChange(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({ [field]: e.detail.value });
  },
  
  // 选择器变化
  onPickerChange(e) {
    const { field } = e.currentTarget.dataset;
    const { value } = e.detail;
    
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      this.setData({
        [parent]: {
          ...this.data[parent],
          [child]: e.currentTarget.dataset.options[value]
        }
      });
    } else {
      this.setData({ [field]: e.currentTarget.dataset.options[value] });
    }
  },
  
  // 开关变化
  onSwitchChange(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({ [field]: e.detail.value });
  },
  
  // 验证表单
  validateForm() {
    const { contractTitle, partyA, partyB, contractTerm, salary, workContent, workPlace } = this.data;
    
    if (!contractTitle.trim()) {
      wx.showToast({ title: '请输入合同标题', icon: 'none' });
      return false;
    }
    
    if (!partyA.name.trim()) {
      wx.showToast({ title: '请输入甲方名称', icon: 'none' });
      return false;
    }
    
    if (!partyB.name.trim()) {
      wx.showToast({ title: '请输入乙方姓名', icon: 'none' });
      return false;
    }
    
    if (!partyB.idCard.trim()) {
      wx.showToast({ title: '请输入乙方身份证号', icon: 'none' });
      return false;
    }
    
    if (!contractTerm.startDate) {
      wx.showToast({ title: '请选择合同开始日期', icon: 'none' });
      return false;
    }
    
    if (!salary.amount.trim()) {
      wx.showToast({ title: '请输入薪资金额', icon: 'none' });
      return false;
    }
    
    if (!workContent.trim()) {
      wx.showToast({ title: '请输入工作内容', icon: 'none' });
      return false;
    }
    
    if (!workPlace.trim()) {
      wx.showToast({ title: '请输入工作地点', icon: 'none' });
      return false;
    }
    
    return true;
  },
  
  // 保存草稿
  onSaveDraft() {
    const contract = this.getContractData();
    contract.status = 'draft';
    
    // 保存到本地
    const drafts = wx.getStorageSync('contractDrafts') || [];
    drafts.push(contract);
    wx.setStorageSync('contractDrafts', drafts);
    
    wx.showToast({
      title: '草稿已保存',
      icon: 'success'
    });
  },
  
  // 预览合同
  onPreview() {
    if (!this.validateForm()) return;
    
    const contract = this.getContractData();
    const content = encodeURIComponent(JSON.stringify(contract));
    
    wx.navigateTo({
      url: `/pages/preview/preview?content=${content}`
    });
  },
  
  // 下一步（签署）
  onNext() {
    if (!this.validateForm()) return;
    
    const contract = this.getContractData();
    const content = encodeURIComponent(JSON.stringify(contract));
    
    wx.navigateTo({
      url: `/pages/sign/sign?content=${content}`
    });
  },
  
  // 获取合同数据
  getContractData() {
    return {
      id: Date.now().toString(),
      templateId: this.data.template?.id,
      title: this.data.contractTitle,
      partyA: this.data.partyA,
      partyB: this.data.partyB,
      contractTerm: this.data.contractTerm,
      salary: this.data.salary,
      workContent: this.data.workContent,
      workPlace: this.data.workPlace,
      workingHours: this.data.workingHours,
      socialInsurance: this.data.socialInsurance,
      otherTerms: this.data.otherTerms,
      createdAt: new Date().toISOString()
    };
  }
});
