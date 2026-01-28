/**
 * 宁律师家族页面
 */
Page({
  data: {
    // 搜索关键词
    searchQuery: '',
    
    // 宁律师列表
    lawyers: [
      {
        id: 'civil',
        name: '民事',
        fullName: '宁律师·民事',
        icon: '👨‍⚖️',
        description: '合同纠纷、侵权责任、婚姻家庭',
        domain: '民事法律',
        helpCount: '12,345',
        rating: 4.9,
        consultCount: '2.3万'
      },
      {
        id: 'criminal',
        name: '刑事',
        fullName: '宁律师·刑事',
        icon: '⚖️',
        description: '刑事辩护、取保候审、减刑假释',
        domain: '刑事法律',
        helpCount: '5,678',
        rating: 5.0,
        consultCount: '8.5千'
      },
      {
        id: 'contract',
        name: '合同',
        fullName: '宁律师·合同',
        icon: '📄',
        description: '合同起草、合同审查、纠纷分析',
        domain: '合同法律',
        helpCount: '18,901',
        rating: 4.8,
        consultCount: '3.5万'
      },
      {
        id: 'labor',
        name: '劳动',
        fullName: '宁律师·劳动',
        icon: '👷',
        description: '劳动合同、工资纠纷、工伤赔偿',
        domain: '劳动法律',
        helpCount: '9,876',
        rating: 4.9,
        consultCount: '1.5万'
      },
      {
        id: 'company',
        name: '公司',
        fullName: '宁律师·公司',
        icon: '🏢',
        description: '公司设立、股权结构、公司治理',
        domain: '公司法',
        helpCount: '6,543',
        rating: 4.8,
        consultCount: '1.2万'
      },
      {
        id: 'ip',
        name: '知产',
        fullName: '宁律师·知识产权',
        icon: '©️',
        description: '专利申请、商标注册、版权保护',
        domain: '知识产权',
        helpCount: '4,321',
        rating: 4.9,
        consultCount: '7.5千'
      },
      {
        id: 'marriage',
        name: '婚姻',
        fullName: '宁律师·婚姻',
        icon: '💑',
        description: '离婚调解、财产分割、抚养权',
        domain: '婚姻家庭',
        helpCount: '7,890',
        rating: 4.9,
        consultCount: '1.1万'
      }
    ],
    
    // 热门咨询
    hotConsultations: [
      {
        icon: '📄',
        question: '劳动合同违约怎么办？',
        count: '2.3w次咨询',
        lawyer: '宁律师·劳动',
        domain: 'labor'
      },
      {
        icon: '💑',
        question: '离婚财产如何分割？',
        count: '1.8w次咨询',
        lawyer: '宁律师·婚姻',
        domain: 'marriage'
      },
      {
        icon: '🏢',
        question: '公司如何设立？',
        count: '1.5w次咨询',
        lawyer: '宁律师·公司',
        domain: 'company'
      }
    ],
    
    // 最近咨询
    recentConsultations: []
  },

  onLoad() {
    console.log('宁律师家族页面加载');
    this.loadRecentConsultations();
  },

  onShow() {
    // 页面显示
  },

  /**
   * 搜索宁律师
   */
  onSearch(e) {
    const query = e.detail.value;
    this.setData({ searchQuery: query });
    
    // 搜索逻辑
    const lawyers = this.data.lawyers;
    const filtered = lawyers.filter(lawyer => 
      lawyer.name.includes(query) || 
      lawyer.fullName.includes(query) ||
      lawyer.description.includes(query)
    );
    this.setData({ lawyers: filtered });
  },

  /**
   * 选择宁律师
   */
  selectLawyer(e) {
    const { domain } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/lawyer-detail/lawyer-detail?domain=${domain}`
    });
  },

  /**
   * 热门咨询
   */
  onHotConsultation(e) {
    const { domain } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/lawyer-detail/lawyer-detail?domain=${domain}`
    });
  },

  /**
   * 加载最近咨询
   */
  loadRecentConsultations() {
    // 从本地存储加载
    const recent = wx.getStorageSync('recentConsultations') || [];
    this.setData({ recentConsultations: recent });
  }
});
