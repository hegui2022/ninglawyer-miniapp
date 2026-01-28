// 码上签约小程序 - app.js
App({
  onLaunch() {
    // 初始化小程序
    console.log('码上签约小程序启动');
    
    // 检查登录状态
    this.checkLogin();
    
    // 初始化配置
    this.initConfig();
  },
  
  globalData: {
    userInfo: null,
    isLogin: false,
    config: {
      apiUrl: 'https://api.example.com',
      uploadUrl: 'https://upload.example.com'
    }
  },
  
  checkLogin() {
    const token = wx.getStorageSync('token');
    if (token) {
      this.globalData.isLogin = true;
      // 获取用户信息
      this.getUserInfo();
    }
  },
  
  initConfig() {
    // 从服务器获取配置
    wx.request({
      url: this.globalData.config.apiUrl + '/config',
      method: 'GET',
      success: (res) => {
        if (res.data.code === 200) {
          this.globalData.config = {
            ...this.globalData.config,
            ...res.data.data
          };
        }
      }
    });
  },
  
  getUserInfo() {
    wx.request({
      url: this.globalData.config.apiUrl + '/user/info',
      method: 'GET',
      header: {
        'Authorization': wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.globalData.userInfo = res.data.data;
        }
      }
    });
  }
});
