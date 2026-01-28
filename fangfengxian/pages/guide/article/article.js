// pages/guide/article/article.js
Page({
  data: {
    hasPaid: false,
    partialContent: '点击下方付费按钮，查看完整内容。',
    fullContent: '公司严格按照网络安全等级保护要求，对系统进行分级管理，定期开展安全评估和漏洞扫描，确保网络安全防护措施有效到位。公司建立了完善的数据备份机制，对重要数据进行定期备份和异地存储，保障数据安全和业务连续性。',
    comments: [
      { name: '张律师', time: '2023-11-20', content: '技术措施写得比较全面。' },
      { name: '李助理', time: '2023-11-20', content: '希望能多一些实战案例。' }
    ]
  },

  onLoad(options) {
    console.log('Article page loaded with options:', options);
    // 可以在这里获取文章ID，然后加载文章详情
  },

  goBack() {
    wx.navigateBack();
  },

  handlePay() {
    wx.showModal({
      title: '付费阅读',
      content: '确定支付20元查看完整内容吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({ hasPaid: true });
          wx.showToast({
            title: '支付成功',
            icon: 'success'
          });
        }
      }
    });
  },

  handleComment(e) {
    console.log('User wants to comment:', e.detail);
    wx.showModal({
      title: '留言',
      content: '请输入您的留言',
      editable: true,
      success: (res) => {
        if (res.confirm && res.content) {
          const newComment = {
            name: '用户' + Math.floor(Math.random() * 1000),
            time: new Date().toISOString().split('T')[0],
            content: res.content
          };
          this.setData({
            comments: [...this.data.comments, newComment]
          });
          wx.showToast({
            title: '留言成功',
            icon: 'success'
          });
        }
      }
    });
  },

  onShareAppMessage() {
    return {
      title: '网络及数据安全技术措施',
      path: '/pages/guide/article/article'
    };
  }
});
