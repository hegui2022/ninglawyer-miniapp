// 判例详情页面
Page({
  data: {
    caseId: null,
    caseDetail: null
  },
  
  onLoad(options) {
    if (options.id) {
      this.setData({ caseId: options.id });
      this.loadCaseDetail();
    }
  },
  
  loadCaseDetail() {
    const cases = {
      1: {
        title: '未按时支付工资纠纷案',
        court: '北京市朝阳区人民法院',
        caseNo: '(2024) 京0105民初12345号',
        date: '2024-11-15',
        plaintiff: '张某',
        defendant: 'XX科技有限公司',
        result: '判决支付工资及经济补偿',
        amount: '¥125,000',
        facts: '原告张某与被告XX科技有限公司于2023年1月签订劳动合同，约定月薪15,000元。自2024年6月起，被告未按时支付工资，累计拖欠工资5个月。',
        opinion: '本院认为，用人单位应当按照劳动合同约定，按时足额支付劳动者工资。被告未按时支付原告工资，构成违约，应当承担相应的法律责任。',
        law: '《劳动合同法》第三十条、第八十五条'
      }
    };
    
    const caseDetail = cases[this.data.caseId] || cases[1];
    this.setData({ caseDetail });
  }
});
