// pages/article/article.js
Page({
  data: {
    statusBarHeight: 44,
    hasPaid: false,
    fullContent: '根据我们对公司提供的资料的核查和访谈，公司业务经营所使用的信息系统均实施第三级信息安全管理，符合《网络安全法》和《网络安全等级保护管理办法》的要求。公司定期进行安全评估和渗透测试，及时发现并修复安全漏洞。'
  },

  onLoad(options) {
    // 获取状态栏高度
    const systemInfo = wx.getSystemInfoSync();
    this.setData({
      statusBarHeight: systemInfo.statusBarHeight
    });

    // 获取文章ID（预留）
    const articleId = options.id || '';
    console.log('文章ID:', articleId);

    // 设置 CSS 变量
    wx.setPageStyle({
      style: {
        '--status-bar-height': systemInfo.statusBarHeight + 'px'
      }
    });
  },

  // 返回上一页
  goBack() {
    wx.navigateBack();
  },

  // 处理付费
  handlePay() {
    // 如果已经付费，提示用户
    if (this.data.hasPaid) {
      wx.showToast({
        title: '已付费，无需重复支付',
        icon: 'none'
      });
      return;
    }

    wx.showModal({
      title: '付费阅读',
      content: '支付20元解锁完整文章内容',
      confirmText: '支付',
      cancelText: '取消',
      success: (res) => {
        if (res.confirm) {
          this.doPayment();
        }
      }
    });
  },

  // 执行支付流程
  doPayment() {
    wx.showLoading({
      title: '支付中...'
    });

    // 模拟支付流程
    setTimeout(() => {
      wx.hideLoading();

      // TODO: 调用微信支付接口
      // wx.requestPayment({
      //   timeStamp: '',
      //   nonceStr: '',
      //   package: '',
      //   signType: 'MD5',
      //   paySign: '',
      //   success: (res) => {
      //     this.setData({ hasPaid: true });
      //     wx.showToast({
      //       title: '支付成功',
      //       icon: 'success'
      //     });
      //   }
      // });

      // 模拟支付成功
      this.setData({ hasPaid: true });
      wx.showToast({
        title: '支付成功',
        icon: 'success'
      });
    }, 1500);
  },

  // 处理留言
  handleComment() {
    // 弹出输入框
    wx.showModal({
      title: '发表留言',
      editable: true,
      placeholderText: '请输入您的留言',
      success: (res) => {
        if (res.confirm && res.content) {
          this.submitComment(res.content);
        }
      }
    });
  },

  // 提交留言
  submitComment(content) {
    wx.showLoading({
      title: '提交中...'
    });

    // TODO: 调用后端接口提交留言
    // wx.request({
    //   url: 'https://your-api.com/comment',
    //   method: 'POST',
    //   data: {
    //     articleId: this.articleId,
    //     content: content
    //   },
    //   success: (res) => {
    //     wx.hideLoading();
    //     wx.showToast({
    //       title: '留言成功',
    //       icon: 'success'
    //     });
    //     // 刷新留言列表
    //   }
    // });

    // 模拟提交成功
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '留言成功',
        icon: 'success'
      });
    }, 1000);
  },

  // 分享文章
  onShareAppMessage() {
    return {
      title: '网络及数据安全技术措施',
      path: '/pages/article/article'
    };
  }
});
