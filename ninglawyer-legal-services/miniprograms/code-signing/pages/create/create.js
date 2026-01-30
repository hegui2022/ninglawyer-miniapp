// 码上签约小程序 - 创建合同页面
Page({
  data: {
    templateList: [],
    selectedTemplate: null,
    contractForm: {
      contractType: '',
      partyA: '',
      partyB: '',
      terms: ''
    },
    loading: false
  },
  
  onLoad() {
    this.loadTemplates();
  },
  
  // 加载合同模板
  loadTemplates() {
    this.setData({ loading: true });
    
    wx.request({
      url: getApp().globalData.config.apiUrl + '/contract/templates',
      method: 'GET',
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            templateList: res.data.data,
            loading: false
          });
        }
      },
      fail: () => {
        this.setData({ loading: false });
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        });
      }
    });
  },
  
  // 选择模板
  onTemplateSelect(e) {
    const template = e.currentTarget.dataset.template;
    this.setData({
      selectedTemplate: template,
      'contractForm.contractType': template.name
    });
    
    // 跳转到表单填写
    wx.navigateTo({
      url: `/pages/create/form?templateId=${template.id}`
    });
  },
  
  // 自定义合同
  onCustomContract() {
    wx.navigateTo({
      url: '/pages/create/form'
    });
  }
});
