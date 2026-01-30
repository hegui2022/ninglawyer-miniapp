// 登录页面
Page({
  data: {
    phone: '',
    code: '',
    countdown: 0,
    isPhoneValid: false,
    isCodeValid: false,
    loading: false
  },

  onLoad() {
    // 检查是否已登录
    const app = getApp();
    if (app.globalData.isLogin) {
      wx.switchTab({
        url: '/pages/index/index'
      });
    }
  },

  // 手机号输入
  onPhoneInput(e) {
    const phone = e.detail.value;
    this.setData({
      phone,
      isPhoneValid: /^1[3-9]\d{9}$/.test(phone)
    });
  },

  // 验证码输入
  onCodeInput(e) {
    const code = e.detail.value;
    this.setData({
      code,
      isCodeValid: /^\d{6}$/.test(code)
    });
  },

  // 获取验证码
  onGetCode() {
    if (!this.data.isPhoneValid) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      });
      return;
    }

    if (this.data.countdown > 0) {
      return;
    }

    // 发送验证码
    wx.showLoading({
      title: '发送中...'
    });

    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '验证码已发送',
        icon: 'success'
      });

      // 开始倒计时
      this.startCountdown();
    }, 1000);
  },

  // 开始倒计时
  startCountdown() {
    let countdown = 60;
    this.setData({ countdown });

    const timer = setInterval(() => {
      countdown--;
      this.setData({ countdown });

      if (countdown <= 0) {
        clearInterval(timer);
      }
    }, 1000);
  },

  // 登录
  onLogin() {
    if (!this.data.isPhoneValid) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      });
      return;
    }

    if (!this.data.isCodeValid) {
      wx.showToast({
        title: '请输入正确的验证码',
        icon: 'none'
      });
      return;
    }

    this.setData({ loading: true });
    wx.showLoading({ title: '登录中...' });

    // 模拟登录
    setTimeout(() => {
      wx.hideLoading();

      // 保存用户信息
      const userInfo = {
        id: '123456',
        name: '用户' + this.data.phone.slice(-4),
        phone: this.data.phone,
        avatar: 'https://via.placeholder.com/100'
      };

      const app = getApp();
      app.login(userInfo);
      app.globalData.token = 'mock_token_' + Date.now();
      wx.setStorageSync('token', app.globalData.token);

      this.setData({ loading: false });

      wx.showToast({
        title: '登录成功',
        icon: 'success'
      });

      setTimeout(() => {
        wx.switchTab({
          url: '/pages/index/index'
        });
      }, 1500);
    }, 1500);
  },

  // 微信登录
  onWechatLogin() {
    wx.showLoading({ title: '登录中...' });

    setTimeout(() => {
      wx.hideLoading();

      // 保存用户信息
      const userInfo = {
        id: '123456',
        name: '微信用户',
        phone: '',
        avatar: 'https://via.placeholder.com/100'
      };

      const app = getApp();
      app.login(userInfo);
      app.globalData.token = 'wechat_token_' + Date.now();
      wx.setStorageSync('token', app.globalData.token);

      wx.showToast({
        title: '登录成功',
        icon: 'success'
      });

      setTimeout(() => {
        wx.switchTab({
          url: '/pages/index/index'
        });
      }, 1500);
    }, 1500);
  },

  // 用户协议
  onAgreement() {
    wx.navigateTo({
      url: '/pages/agreement/agreement'
    });
  },

  // 隐私政策
  onPrivacy() {
    wx.navigateTo({
      url: '/pages/privacy/privacy'
    });
  }
});
