/**
 * 首页
 */
Page({
  data: {
    // 轮播图
    banners: [
      {
        image: '/images/banners/banner1.png',
        title: '7x24小时法律咨询',
        subtitle: '宁律师随时为您服务'
      },
      {
        image: '/images/banners/banner2.png',
        title: '智能合同起草',
        subtitle: '专业、快速、高效'
      },
      {
        image: '/images/banners/banner3.png',
        title: '一站式法律服务',
        title: '咨询→起草→签约→履约→维权'
      }
    ],
    
    // 服务入口
    services: [
      {
        id: 'ning-lawyer',
        name: '宁律师家族',
        icon: '⚖️',
        description: '7x24小时法律咨询',
        url: '/pages/lawyer-family/lawyer-family',
        color: '#07C160'
      },
      {
        id: 'mashangqianyue',
        name: '码上签约',
        icon: '📱',
        description: '扫码签约，智能指导',
        url: '/pages/services/services?tab=signing',
        color: '#07C160'
      },
      {
        id: 'liyue',
        name: '理约',
        icon: '📋',
        description: '合同全生命周期管理',
        url: '/pages/services/services?tab=management',
        color: '#07C160'
      },
      {
        id: 'fangfengxian',
        name: '防风险',
        icon: '🛡️',
        description: '企业合规风险防控',
        url: '/pages/services/services?tab=risk',
        color: '#07C160'
      },
      {
        id: 'zenmepan',
        name: '怎么判',
        icon: '⚖️',
        description: '诉讼维权，专业指导',
        url: '/pages/services/services?tab=litigation',
        color: '#07C160'
      }
    ],
    
    // 热门咨询
    hotConsultations: [
      {
        id: 1,
        title: '劳动合同违约怎么办？',
        count: '2.3w',
        lawyer: '宁律师·劳动',
        domain: 'labor'
      },
      {
        id: 2,
        title: '离婚财产如何分割？',
        count: '1.8w',
        lawyer: '宁律师·婚姻',
        domain: 'marriage'
      },
      {
        id: 3,
        title: '公司如何设立？',
        count: '1.5w',
        lawyer: '宁律师·公司',
        domain: 'company'
      }
    ],
    
    // 最新动态
    news: [
      {
        id: 1,
        title: '新《公司法》实施，企业需要注意什么？',
        date: '2024-01-28'
      },
      {
        id: 2,
        title: '劳动合同签订注意事项',
        date: '2024-01-27'
      },
      {
        id: 3,
        title: '离婚财产分割常见问题解答',
        date: '2024-01-26'
      }
    ]
  },

  onLoad() {
    console.log('首页加载');
  },

  onShow() {
    // 页面显示
  },

  /**
   * 跳转服务页面
   */
  goToService(e) {
    const { url } = e.currentTarget.dataset;
    wx.navigateTo({ url });
  },

  /**
   * 跳转热门咨询
   */
  goToHotConsultation(e) {
    const { domain } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/lawyer-detail/lawyer-detail?domain=${domain}`
    });
  },

  /**
   * 跳转新闻详情
   */
  goToNewsDetail(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/news-detail/news-detail?id=${id}`
    });
  }
});
