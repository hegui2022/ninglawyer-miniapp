// pages/template-detail/template-detail.js
const app = getApp();

Page({
  data: {
    templateId: null,
    template: {},
    content: {},
    loading: false
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ templateId: options.id });
      this.loadTemplateDetail();
    }
  },

  // 加载模板详情
  loadTemplateDetail() {
    this.setData({ loading: true });

    app.request({
      url: `/template/${this.data.templateId}`,
      method: 'GET',
      success: (res) => {
        if (res.code === 0 && res.data) {
          const template = {
            ...res.data,
            icon: this.getTemplateIcon(res.data.template_type),
            type_name: this.getTemplateTypeName(res.data.template_type)
          };
          
          this.setData({
            template: template,
            content: res.data.template_content
          });
        }
      },
      fail: (err) => {
        console.error('加载模板详情失败', err);
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

  // 使用模板
  useTemplate() {
    wx.showModal({
      title: '使用模板',
      editable: true,
      placeholderText: '请输入合同名称',
      success: (res) => {
        if (res.confirm && res.content) {
          this.createContract(res.content);
        }
      }
    });
  },

  // 创建合同
  createContract(contractName) {
    wx.showLoading({ title: '创建中...' });

    app.request({
      url: `/template/${this.data.templateId}/use`,
      method: 'POST',
      data: {
        contract_name: contractName
      },
      success: (res) => {
        if (res.code === 0 && res.data) {
          wx.hideLoading();
          wx.showToast({
            title: '创建成功',
            icon: 'success'
          });
          
          // 跳转到合同编辑页面
          setTimeout(() => {
            wx.redirectTo({
              url: `/pages/contract-edit/contract-edit?id=${res.data.contract_id}`
            });
          }, 1500);
        }
      },
      fail: (err) => {
        wx.hideLoading();
        console.error('创建合同失败', err);
        wx.showToast({
          title: '创建失败',
          icon: 'none'
        });
      }
    });
  },

  // 返回
  goBack() {
    wx.navigateBack();
  },

  // 获取模板图标
  getTemplateIcon(type) {
    const iconMap = {
      'standard': '📄',
      'parttime': '⏱️',
      'intern': '🎓',
      'retired': '👴',
      'project': '📦',
      'dispatch': '🚚'
    };
    return iconMap[type] || '📋';
  },

  // 获取模板类型名称
  getTemplateTypeName(type) {
    const typeMap = {
      'standard': '劳动合同',
      'parttime': '非全日制',
      'intern': '实习协议',
      'retired': '退休返聘',
      'project': '项目制',
      'dispatch': '劳务派遣'
    };
    return typeMap[type] || type;
  }
});
