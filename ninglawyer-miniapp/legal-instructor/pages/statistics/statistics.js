// 数据统计页面
Page({
  data: {
    overview: {
      totalConsults: 12,
      totalContracts: 8,
      satisfaction: 98,
      savings: '¥12,500'
    },
    consultStats: [
      { name: '民事咨询', count: 5, percentage: 42 },
      { name: '合同咨询', count: 3, percentage: 25 },
      { name: '劳动咨询', count: 2, percentage: 16 },
      { name: '其他咨询', count: 2, percentage: 17 }
    ],
    contractStats: [
      { name: '已签署', count: 6, color: '#07C160' },
      { name: '待签署', count: 1, color: '#FF9800' },
      { name: '已过期', count: 1, color: '#F44336' }
    ],
    monthlyTrend: [
      { month: '8月', consults: 3, contracts: 2 },
      { month: '9月', consults: 5, contracts: 3 },
      { month: '10月', consults: 4, contracts: 2 },
      { month: '11月', consults: 6, contracts: 3 },
      { month: '12月', consults: 8, contracts: 4 },
      { month: '1月', consults: 12, contracts: 8 }
    ],
    timeRange: '本月'
  },
  
  onLoad() {
    this.loadStats();
  },
  
  loadStats() {
    // 加载统计数据
  },
  
  onTimeRangeChange() {
    const ranges = ['本周', '本月', '本季', '本年'];
    const currentIndex = ranges.indexOf(this.data.timeRange);
    const nextIndex = (currentIndex + 1) % ranges.length;
    
    this.setData({
      timeRange: ranges[nextIndex]
    });
    
    wx.showToast({
      title: `已切换至${ranges[nextIndex]}`,
      icon: 'none'
    });
  },
  
  onConsultDetail() {
    wx.navigateTo({
      url: '/pages/consult/consult'
    });
  },
  
  onContractDetail() {
    wx.switchTab({
      url: '/pages/list/list'
    });
  }
});
