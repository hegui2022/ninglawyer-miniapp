/**
 * 法律教官小程序入口
 */

App({
  globalData: {
    // API 基础地址
    baseUrl: 'https://api.example.com',
    
    // 用户信息
    userInfo: null,
    
    // 登录状态
    isLogin: false,
    
    // Token
    token: null
  },

  onLaunch() {
    // 小程序启动
    console.log('法律教官小程序启动');
    
    // 检查登录状态
    this.checkLoginStatus();
    
    // 获取系统信息
    this.getSystemInfo();
  },

  onShow() {
    // 小程序显示
  },

  onHide() {
    // 小程序隐藏
  },

  onError(error) {
    // 错误处理
    console.error('小程序错误:', error);
  },

  /**
   * 检查登录状态
   */
  checkLoginStatus() {
    const token = wx.getStorageSync('token');
    if (token) {
      this.globalData.token = token;
      this.globalData.isLogin = true;
      
      // 获取用户信息
      this.getUserInfo();
    }
  },

  /**
   * 获取用户信息
   */
  getUserInfo() {
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
    }
  },

  /**
   * 获取系统信息
   */
  getSystemInfo() {
    wx.getSystemInfo({
      success: (res) => {
        this.globalData.systemInfo = res;
      }
    });
  },

  /**
   * 请求封装
   */
  request(options) {
    const { url, method = 'GET', data = {}, header = {} } = options;
    
    // 添加 token
    if (this.globalData.token) {
      header['Authorization'] = `Bearer ${this.globalData.token}`;
    }
    
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.globalData.baseUrl + url,
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
