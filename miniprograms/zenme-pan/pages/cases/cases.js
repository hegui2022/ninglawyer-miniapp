// 判例查询页面
Page({
  data: {
    keyword: '',
    cases: [
      {
        id: 1,
        title: '未按时支付工资纠纷案',
        court: '北京市朝阳区人民法院',
        caseNo: '(2024) 京0105民初12345号',
        result: '判决支付工资及经济补偿',
        date: '2024-11-15',
        tags: ['劳动纠纷', '工资拖欠']
      },
      {
        id: 2,
        title: '单方面解除劳动合同案',
        court: '上海市浦东新区人民法院',
        caseNo: '(2024) 沪0115民初67890号',
        result: '判决赔偿违约金',
        date: '2024-10-20',
        tags: ['劳动合同', '违约赔偿']
      },
      {
        id: 3,
        title: '货物质量不合格纠纷案',
        court: '广州市天河区人民法院',
        caseNo: '(2024) 粤0106民初11111号',
        result: '判决退货退款并赔偿',
        date: '2024-10-10',
        tags: ['买卖合同', '质量纠纷']
      },
      {
        id: 4,
        title: '房屋租赁违约纠纷案',
        court: '深圳市南山区人民法院',
        caseNo: '(2024) 粤0305民初22222号',
        result: '判决解除合同并赔偿',
        date: '2024-09-25',
        tags: ['租赁合同', '违约']
      }
    ],
    filteredCases: []
  },
  
  onLoad(options) {
    if (options.keyword) {
      this.setData({ keyword: options.keyword });
      this.searchCases();
    } else {
      this.setData({ filteredCases: this.data.cases });
    }
  },
  
  onSearchInput(e) {
    this.setData({ keyword: e.detail.value });
  },
  
  onSearch() {
    this.searchCases();
  },
  
  searchCases() {
    const keyword = this.data.keyword.toLowerCase();
    
    if (!keyword) {
      this.setData({ filteredCases: this.data.cases });
      return;
    }
    
    const filtered = this.data.cases.filter(c => 
      c.title.toLowerCase().includes(keyword) ||
      c.result.toLowerCase().includes(keyword) ||
      c.tags.some(tag => tag.toLowerCase().includes(keyword))
    );
    
    this.setData({ filteredCases: filtered });
  },
  
  onCaseTap(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/case-detail/case-detail?id=${id}`
    });
  },
  
  onTagTap(e) {
    const tag = e.currentTarget.dataset.tag;
    this.setData({ keyword: tag });
    this.searchCases();
  }
});
