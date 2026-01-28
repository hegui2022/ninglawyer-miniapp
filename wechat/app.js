// app.js
App({
  globalData: {
    userInfo: null,
    apiBase: 'http://localhost:5001/api', // 后端 API 地址
    token: '', // 用户令牌
  },

  onLaunch() {
    // 小程序启动
    console.log('宁律师小程序启动');
    
    // 检查登录状态
    this.checkLogin();
  },

  onShow() {
    // 小程序显示
  },

  onHide() {
    // 小程序隐藏
  },

  // 检查登录状态
  checkLogin() {
    const token = wx.getStorageSync('token');
    if (token) {
      this.globalData.token = token;
    }
  },

  // 统一请求方法
  request(options) {
    const { url, method = 'GET', data = {}, success, fail } = options;
    const fullUrl = `${this.globalData.apiBase}${url}`;
    
    wx.request({
      url: fullUrl,
      method: method,
      data: data,
      header: {
        'content-type': 'application/json',
        'Authorization': `Bearer ${this.globalData.token}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          if (success) success(res.data);
        } else {
          wx.showToast({
            title: res.data.message || '请求失败',
            icon: 'none'
          });
          if (fail) fail(res);
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
        if (fail) fail(err);
      }
    });
  },

  // 显示加载提示
  showLoading(title = '加载中...') {
    wx.showLoading({
      title: title,
      mask: true
    });
  },

  // 隐藏加载提示
  hideLoading() {
    wx.hideLoading();
  }
});
