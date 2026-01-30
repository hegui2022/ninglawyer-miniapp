/**
 * 法律教官小程序入口
 */

// 导入配置
const config = require('./utils/config.js');

App({
  globalData: {
    // API 基础地址（开发环境）
    config: config.config,

    // 用户信息
    userInfo: null,

    // 登录状态
    isLogin: false,

    // Token
    token: null,

    // 系统信息
    systemInfo: null
  },

  onLaunch() {
    console.log('法律教官小程序启动');
    console.log('当前环境:', config.ENV);
    console.log('API 地址:', config.config.apiUrl);

    // 检查登录状态
    this.checkLoginStatus();

    // 获取系统信息
    this.getSystemInfo();

    // 初始化错误监听
    this.initErrorMonitor();
  },

  onShow() {
    // 小程序显示
    console.log('小程序显示');
  },

  onHide() {
    // 小程序隐藏
  },

  onError(error) {
    // 错误处理
    console.error('小程序错误:', error);
    wx.showToast({
      title: '程序出现错误',
      icon: 'none'
    });
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
    } else {
      // 如果没有本地用户信息，从服务器获取
      this.fetchUserInfo();
    }
  },

  /**
   * 从服务器获取用户信息
   */
  fetchUserInfo() {
    if (!this.globalData.isLogin) return;

    this.request({
      url: '/user/info',
      method: 'GET'
    }).then(res => {
      if (res.code === 200) {
        this.globalData.userInfo = res.data;
        wx.setStorageSync('userInfo', res.data);
      }
    }).catch(err => {
      console.error('获取用户信息失败:', err);
    });
  },

  /**
   * 获取系统信息
   */
  getSystemInfo() {
    const systemInfo = wx.getSystemInfoSync();
    this.globalData.systemInfo = systemInfo;
    console.log('系统信息:', systemInfo);
  },

  /**
   * 初始化错误监听
   */
  initErrorMonitor() {
    // 监听小程序错误
    wx.onError((error) => {
      console.error('小程序错误:', error);
      // TODO: 上报错误到服务器
    });

    // 监听小程序未处理的 Promise reject
    wx.onUnhandledRejection((res) => {
      console.error('未处理的 Promise reject:', res);
      // TODO: 上报错误到服务器
    });
  },

  /**
   * 统一的请求方法
   */
  request(options) {
    const { url, method = 'GET', data = {}, header = {} } = options;
    const fullUrl = this.globalData.config.apiUrl + url;

    return new Promise((resolve, reject) => {
      wx.request({
        url: fullUrl,
        method: method,
        data: data,
        header: {
          'Content-Type': 'application/json',
          'Authorization': this.globalData.token || '',
          ...header
        },
        timeout: this.globalData.config.timeout,
        success: (res) => {
          if (res.statusCode === 200) {
            if (res.data.code === 0 || res.data.code === 200) {
              resolve(res.data);
            } else {
              wx.showToast({
                title: res.data.message || '请求失败',
                icon: 'none'
              });
              reject(res.data);
            }
          } else {
            wx.showToast({
              title: '网络错误',
              icon: 'none'
            });
            reject({ message: '网络错误' });
          }
        },
        fail: (err) => {
          console.error('请求失败:', err);
          wx.showToast({
            title: '网络连接失败',
            icon: 'none'
          });
          reject(err);
        }
      });
    });
  },

  /**
   * 上传文件
   */
  uploadFile(options) {
    const { filePath, name = 'file', formData = {} } = options;
    const fullUrl = this.globalData.config.baseUrl + '/upload';

    return new Promise((resolve, reject) => {
      wx.uploadFile({
        url: fullUrl,
        filePath: filePath,
        name: name,
        formData: formData,
        header: {
          'Authorization': this.globalData.token || ''
        },
        success: (res) => {
          try {
            const data = JSON.parse(res.data);
            if (data.code === 0) {
              resolve(data.data);
            } else {
              reject(new Error(data.message || '上传失败'));
            }
          } catch (error) {
            reject(error);
          }
        },
        fail: (err) => {
          console.error('上传失败:', err);
          reject(err);
        }
      });
    });
  }

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
   * 初始化错误监听
   */
  initErrorMonitor() {
    // 可以在这里接入错误监控平台
  },

  /**
   * 统一请求封装
   */
  request(options) {
    const { url, method = 'GET', data = {}, header = {} } = options;
    
    // 添加 token
    if (this.globalData.token) {
      header['Authorization'] = this.globalData.token;
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
          } else if (res.statusCode === 401) {
            // Token 过期，重新登录
            wx.showToast({
              title: '登录已过期',
              icon: 'none'
            });
            this.clearLogin();
            setTimeout(() => {
              wx.navigateTo({
                url: '/pages/login/login'
              });
            }, 1500);
            reject(res.data);
          } else {
            wx.showToast({
              title: res.data.message || '请求失败',
              icon: 'none'
            });
            reject(res.data);
          }
        },
        fail: (err) => {
          console.error('请求失败:', err);
          wx.showToast({
            title: '网络错误，请检查网络',
            icon: 'none'
          });
          reject(err);
        }
      });
    });
  },

  /**
   * 清除登录状态
   */
  clearLogin() {
    this.globalData.token = null;
    this.globalData.isLogin = false;
    this.globalData.userInfo = null;
    wx.removeStorageSync('token');
    wx.removeStorageSync('userInfo');
  },

  /**
   * 登录
   */
  login(userInfo) {
    this.globalData.isLogin = true;
    this.globalData.userInfo = userInfo;
    wx.setStorageSync('userInfo', userInfo);
    // 这里应该调用登录接口获取token
    // this.globalData.token = token;
    // wx.setStorageSync('token', token);
  },

  /**
   * 退出登录
   */
  logout() {
    wx.showModal({
      title: '提示',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          this.clearLogin();
          wx.reLaunch({
            url: '/pages/index/index'
          });
        }
      }
    });
  }
});
