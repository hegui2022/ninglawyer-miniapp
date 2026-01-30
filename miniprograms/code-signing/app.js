// 码上签约小程序入口
App({
  globalData: {
    userInfo: null,
    isLogin: false,
    config: {
      apiUrl: 'http://localhost:5000/api',
      baseUrl: 'http://localhost:5000'
    }
  },
  
  onLaunch() {
    console.log('码上签约小程序启动');
    this.checkLogin();
  },
  
  checkLogin() {
    const token = wx.getStorageSync('token');
    if (token) {
      this.globalData.isLogin = true;
      this.getUserInfo();
    }
  },
  
  getUserInfo() {
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
    }
  },
  
  request(options) {
    const { url, method = 'GET', data = {}, header = {} } = options;
    const token = wx.getStorageSync('token');
    
    if (token) {
      header['Authorization'] = token;
    }
    
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.globalData.config.apiUrl + url,
        method,
        data,
        header: {
          'Content-Type': 'application/json',
          ...header
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            wx.showToast({
              title: res.data.message || '请求失败',
              icon: 'none'
            });
            reject(res.data);
          }
        },
        fail: (err) => {
          wx.showToast({
            title: '网络错误',
            icon: 'none'
          });
          reject(err);
        }
      });
    });
  }
});
