// 合同模板选择页面
Page({
  data: {
    categories: [
      { id: 'all', name: '全部' },
      { id: 'labor', name: '劳动合同' },
      { id: 'service', name: '服务合同' },
      { id: 'purchase', name: '采购合同' },
      { id: 'lease', name: '租赁合同' },
      { id: 'cooperation', name: '合作协议' }
    ],
    currentCategory: 'all',
    templates: [
      {
        id: 1,
        name: '标准劳动合同',
        category: 'labor',
        description: '适用于公司招聘正式员工的劳动合同',
        icon: '👤',
        usage: 12580,
        rating: 4.9
      },
      {
        id: 2,
        name: '兼职劳动合同',
        category: 'labor',
        description: '适用于兼职人员的劳动合同',
        icon: '👥',
        usage: 9680,
        rating: 4.8
      },
      {
        id: 3,
        name: '技术服务合同',
        category: 'service',
        description: '适用于技术服务外包的业务',
        icon: '💼',
        usage: 8900,
        rating: 4.9
      },
      {
        id: 4,
        name: '产品采购合同',
        category: 'purchase',
        description: '适用于产品采购的标准化合同',
        icon: '📦',
        usage: 11200,
        rating: 4.8
      },
      {
        id: 5,
        name: '房屋租赁合同',
        category: 'lease',
        description: '适用于房屋租赁的标准合同',
        icon: '🏠',
        usage: 13500,
        rating: 4.9
      },
      {
        id: 6,
        name: '战略合作协议',
        category: 'cooperation',
        description: '适用于企业间战略合作',
        icon: '🤝',
        usage: 7800,
        rating: 4.7
      },
      {
        id: 7,
        name: '设备租赁合同',
        category: 'lease',
        description: '适用于设备租赁业务',
        icon: '🔧',
        usage: 5600,
        rating: 4.6
      },
      {
        id: 8,
        name: '委托代理合同',
        category: 'service',
        description: '适用于委托代理业务',
        icon: '📋',
        usage: 6800,
        rating: 4.8
      }
    ],
    filteredTemplates: [],
    searchKeyword: ''
  },
  
  onLoad() {
    this.setData({
      filteredTemplates: this.data.templates
    });
  },
  
  onCategoryChange(e) {
    const category = e.currentTarget.dataset.category;
    this.setData({
      currentCategory: category
    });
    this.filterTemplates();
  },
  
  onSearchInput(e) {
    const keyword = e.detail.value;
    this.setData({
      searchKeyword: keyword
    });
    this.filterTemplates();
  },
  
  filterTemplates() {
    const { currentCategory, searchKeyword, templates } = this.data;
    
    let filtered = templates;
    
    // 按类别筛选
    if (currentCategory !== 'all') {
      filtered = filtered.filter(t => t.category === currentCategory);
    }
    
    // 按关键词搜索
    if (searchKeyword) {
      const keyword = searchKeyword.toLowerCase();
      filtered = filtered.filter(t => 
        t.name.toLowerCase().includes(keyword) ||
        t.description.toLowerCase().includes(keyword)
      );
    }
    
    this.setData({
      filteredTemplates: filtered
    });
  },
  
  onTemplateTap(e) {
    const template = e.currentTarget.dataset.template;
    wx.showModal({
      title: '使用模板',
      content: `确定使用"${template.name}"创建合同吗？`,
      success: (res) => {
        if (res.confirm) {
          wx.navigateTo({
            url: '/pages/create/create?templateId=' + template.id
          });
        }
      }
    });
  }
});
