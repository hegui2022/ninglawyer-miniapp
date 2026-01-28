// pages/template-list/template-list.js
const app = getApp();

Page({
  data: {
    templates: [],
    filterType: 'all',
    loading: false
  },

  onLoad() {
    this.loadTemplates();
  },

  onShow() {
    // 页面显示时刷新列表
    this.loadTemplates();
  },

  // 加载模板列表
  loadTemplates() {
    this.setData({ loading: true });

    app.request({
      url: '/template/list',
      method: 'GET',
      data: {
        template_type: this.data.filterType === 'all' ? '' : this.data.filterType,
        is_active: true,
        limit: 100
      },
      success: (res) => {
        if (res.code === 0 && res.data) {
          // 格式化模板数据
          const templates = res.data.map(template => ({
            ...template,
            icon: this.getTemplateIcon(template.template_type),
            type_name: this.getTemplateTypeName(template.template_type),
            created_at: this.formatDate(template.created_at)
          }));

          this.setData({ templates });
        }
      },
      fail: (err) => {
        console.error('加载模板列表失败', err);
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

  // 设置筛选条件
  setFilter(type) {
    if (this.data.filterType === type) return;
    
    this.setData({ filterType: type });
    this.loadTemplates();
  },

  // 跳转到模板详情
  goToDetail(id) {
    wx.navigateTo({
      url: `/pages/template-detail/template-detail?id=${id}`
    });
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
