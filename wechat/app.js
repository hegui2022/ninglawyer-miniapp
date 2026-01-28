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
    const { url, method = 'GET', data = {}, responseType = 'json', success, fail } = options;
    const fullUrl = `${this.globalData.apiBase}${url}`;
    
    const header = {
      'content-type': 'application/json',
      'Authorization': `Bearer ${this.globalData.token}`
    };
    
    // 如果不是 json 格式，移除 content-type
    if (responseType !== 'json') {
      delete header['content-type'];
    }
    
    wx.request({
      url: fullUrl,
      method: method,
      data: data,
      header: header,
      responseType: responseType,
      success: (res) => {
        if (res.statusCode === 200) {
          if (responseType === 'json') {
            if (success) success(res.data);
          } else {
            // arraybuffer 等其他类型直接返回数据
            if (success) success(res.data);
          }
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
