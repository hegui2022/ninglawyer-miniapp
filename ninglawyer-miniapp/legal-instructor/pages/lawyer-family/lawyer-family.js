// 法律教官 - 宁律师家族
Page({
  data: {
    searchKeyword: '',
    lawyers: [
      {
        id: 'civil',
        name: '宁律师·民事',
        domain: '民事',
        avatar: '/assets/images/lawyers/civil.png',
        description: '合同纠纷、侵权责任、婚姻家庭',
        helpCount: 12580,
        rating: 4.9
      },
      {
        id: 'criminal',
        name: '宁律师·刑事',
        domain: '刑事',
        avatar: '/assets/images/lawyers/criminal.png',
        description: '刑事辩护、取保候审、减刑假释',
        helpCount: 9680,
        rating: 4.8
      },
      {
        id: 'labor',
        name: '宁律师·劳动',
        domain: '劳动',
        avatar: '/assets/images/lawyers/labor.png',
        description: '劳动合同、工资纠纷、工伤赔偿',
        helpCount: 11200,
        rating: 4.9
      },
      {
        id: 'company',
        name: '宁律师·公司',
        domain: '公司',
        avatar: '/assets/images/lawyers/company.png',
        description: '公司设立、股权设计、公司并购',
        helpCount: 8900,
        rating: 4.8
      },
      {
        id: 'ip',
        name: '宁律师·知识产权',
        domain: '知识产权',
        avatar: '/assets/images/lawyers/ip.png',
        description: '专利申请、商标注册、侵权维权',
        helpCount: 7800,
        rating: 4.9
      },
      {
        id: 'marriage',
        name: '宁律师·婚姻',
        domain: '婚姻',
        avatar: '/assets/images/lawyers/marriage.png',
        description: '离婚诉讼、抚养权、财产分割',
        helpCount: 13500,
        rating: 4.9
      },
      {
        id: 'contract',
        name: '宁律师·合同',
        domain: '合同',
        avatar: '/assets/images/lawyers/contract.png',
        description: '合同起草、审查、风险分析',
        helpCount: 8650,
        rating: 4.8
      }
    ],
    filteredLawyers: []
  },
  
  onLoad() {
    this.setData({
      filteredLawyers: this.data.lawyers
    });
  },
  
  // 搜索输入
  onSearchInput(e) {
    const keyword = e.detail.value.toLowerCase();
    const filtered = this.data.lawyers.filter(lawyer => 
      lawyer.name.toLowerCase().includes(keyword) ||
      lawyer.domain.toLowerCase().includes(keyword) ||
      lawyer.description.toLowerCase().includes(keyword)
    );
    
    this.setData({
      searchKeyword: e.detail.value,
      filteredLawyers: filtered
    });
  },
  
  // 点击律师
  onLawyerTap(e) {
    const lawyer = e.currentTarget.dataset.lawyer;
    wx.navigateTo({
      url: `/pages/consult/consult?lawyer=${lawyer.id}`
    });
  },
  
  // 立即咨询
  onConsultNow(e) {
    const lawyer = e.currentTarget.dataset.lawyer;
    wx.navigateTo({
      url: `/pages/consult/consult?lawyer=${lawyer.id}`
    });
  }
});
