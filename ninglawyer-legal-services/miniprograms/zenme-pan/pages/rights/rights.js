// 维权指导页面
Page({
  data: {
    activeTab: 'process',
    tabs: [
      { id: 'process', name: '维权流程' },
      { id: 'law', name: '法律条款' },
      { id: 'cases', name: '案例参考' }
    ],
    steps: [
      {
        id: 1,
        title: '收集证据',
        description: '收集合同文本、付款凭证、沟通记录等证据',
        tips: '建议保留原件，做好备份'
      },
      {
        id: 2,
        title: '协商沟通',
        description: '与对方协商，要求履行合同或赔偿损失',
        tips: '建议书面沟通，保留沟通记录'
      },
      {
        id: 3,
        title: '发送律师函',
        description: '委托律师发送律师函，正式催告对方',
        tips: '律师函具有法律效力，可作为证据'
      },
      {
        id: 4,
        title: '申请仲裁',
        description: '如协商不成，可向仲裁机构申请仲裁',
        tips: '仲裁需双方约定或事后达成一致'
      },
      {
        id: 5,
        title: '提起诉讼',
        description: '向法院提起诉讼，通过司法途径解决',
        tips: '注意诉讼时效，一般为3年'
      }
    ],
    laws: [
      {
        title: '《民法典》第五百七十七条',
        content: '当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。'
      },
      {
        title: '《民法典》第五百七十八条',
        content: '当事人一方明确表示或者以自己的行为表明不履行合同义务的，对方可以在履行期限届满前请求其承担违约责任。'
      },
      {
        title: '《民法典》第五百七十九条',
        content: '当事人一方未支付价款、报酬、租金、利息，或者不履行其他金钱债务的，对方可以请求其支付。'
      }
    ],
    referenceCases: [
      {
        id: 1,
        title: '未按时支付工资案',
        court: '北京市朝阳区人民法院',
        result: '判决支付工资及经济补偿',
        date: '2024-11-15'
      },
      {
        id: 2,
        title: '单方面解除合同案',
        court: '上海市浦东新区人民法院',
        result: '判决赔偿违约金',
        date: '2024-10-20'
      }
    ]
  },
  
  onLoad() {
    
  },
  
  onTabChange(e) {
    const tabId = e.currentTarget.dataset.id;
    this.setData({ activeTab: tabId });
  },
  
  onStepTap(e) {
    const step = e.currentTarget.dataset.step;
    wx.showModal({
      title: step.title,
      content: `${step.description}\n\n建议：${step.tips}`,
      showCancel: false
    });
  },
  
  onLawTap(e) {
    const law = e.currentTarget.dataset.law;
    wx.showModal({
      title: law.title,
      content: law.content,
      showCancel: false
    });
  },
  
  onCaseTap(e) {
    const caseId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/case-detail/case-detail?id=${caseId}`
    });
  },
  
  onConsult() {
    wx.showModal({
      title: '法律咨询',
      content: '是否需要专业律师提供一对一咨询？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({
            title: '跳转中...',
            icon: 'loading'
          });
        }
      }
    });
  }
});
