// 法律教官 - 首页（使用网络图片）
Page({
  data: {
    banners: [
      {
        id: 1,
        image: 'https://via.placeholder.com/750x360/07C160/ffffff?text=宁律师-您的专属法律顾问',
        title: '宁律师 - 您的专属法律顾问'
      },
      {
        id: 2,
        image: 'https://via.placeholder.com/750x360/06AD56/ffffff?text=专业法律服务-随时随地',
        title: '专业法律服务，随时随地'
      },
      {
        id: 3,
        image: 'https://via.placeholder.com/750x360/05A848/ffffff?text=7大领域-全方位保障',
        title: '7大领域，全方位保障'
      }
    ],
    services: [
      {
        id: 1,
        icon: '⚖️',
        title: '法律咨询',
        description: '在线咨询专业律师',
        url: '/pages/consult/consult'
      },
      {
        id: 2,
        icon: '📝',
        title: '合同服务',
        description: '起草、审查、管理',
        url: '/pages/contract/contract'
      },
      {
        id: 3,
        icon: '✍️',
        title: '电子签约',
        description: '便捷高效的签署',
        url: '/pages/sign/sign'
      },
      {
        id: 4,
        icon: '🔍',
        title: '案例查询',
        description: '海量案例库',
        url: '/pages/case/case'
      }
    ],
    lawyers: [
      {
        id: 'civil',
        name: '宁律师·民事',
        avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=民事',
        description: '民事纠纷专家'
      },
      {
        id: 'criminal',
        name: '宁律师·刑事',
        avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=刑事',
        description: '刑事辩护专家'
      },
      {
        id: 'labor',
        name: '宁律师·劳动',
        avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=劳动',
        description: '劳动纠纷专家'
      },
      {
        id: 'company',
        name: '宁律师·公司',
        avatar: 'https://via.placeholder.com/100/07C160/ffffff?text=公司',
        description: '公司法律专家'
      }
    ],
    stats: {
      users: '12.8万',
      consultations: '89.6万',
      satisfaction: '99.2%'
    },
    currentBanner: 0
  },
  
  onLoad() {
    // 检查登录状态
    const app = getApp();
    if (!app.globalData.isLogin) {
      wx.redirectTo({
        url: '/pages/login/login'
      });
    }
  },
  
  onBannerChange(e) {
    this.setData({
      currentBanner: e.detail.current
    });
  },
  
  onServiceTap(e) {
    const url = e.currentTarget.dataset.url;
    if (url && url !== '/pages/consult/consult') {
      wx.showToast({
        title: '功能开发中',
        icon: 'none'
      });
    } else if (url === '/pages/consult/consult') {
      wx.navigateTo({
        url: url + '?lawyerId=civil'
      });
    }
  },
  
  onGoLawyerFamily() {
    wx.switchTab({
      url: '/pages/lawyer-family/lawyer-family'
    });
  },
  
  onLawyerTap(e) {
    const lawyerId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/consult/consult?lawyerId=' + lawyerId
    });
  }
});
