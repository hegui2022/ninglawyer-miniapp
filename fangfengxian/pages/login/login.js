// pages/login/login.js
Page({
  data: {
    statusBarHeight: 44
  },

  onLoad() {
    // 获取状态栏高度
    const systemInfo = wx.getSystemInfoSync();
    this.setData({
      statusBarHeight: systemInfo.statusBarHeight
    });

    // 设置 CSS 变量
    wx.setPageStyle({
      style: {
        '--status-bar-height': systemInfo.statusBarHeight + 'px'
      }
    });
  },

  // 微信登录
  wechatLogin() {
    wx.showLoading({
      title: '登录中...'
    });

    // 获取用户授权
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        console.log('用户授权成功', res);
        this.doWechatLogin(res);
      },
      fail: (err) => {
        wx.hideLoading();
        console.log('用户授权失败', err);
        wx.showToast({
          title: '授权失败，请重试',
          icon: 'none'
        });
      }
    });
  },

  // 执行微信登录
  doWechatLogin(userInfo) {
    wx.login({
      success: (res) => {
        if (res.code) {
          console.log('微信登录 code:', res.code);
          console.log('用户信息:', userInfo);
          
          // TODO: 调用后端接口进行登录
          // wx.request({
          //   url: 'https://your-api.com/wechat-login',
          //   method: 'POST',
          //   data: {
          //     code: res.code,
          //     userInfo: userInfo.userInfo
          //   },
          //   success: (loginRes) => {
          //     wx.hideLoading();
          //     // 保存登录信息
          //     wx.setStorageSync('token', loginRes.data.token);
          //     // 跳转到首页
          //     wx.redirectTo({
          //       url: '/pages/index/index'
          //     });
          //   }
          // });

          // 模拟登录成功
          setTimeout(() => {
            wx.hideLoading();
            wx.showToast({
              title: '登录成功',
              icon: 'success'
            });

            // 跳转到首页（暂时注释，等待开发）
            // wx.redirectTo({
            //   url: '/pages/index/index'
            // });
          }, 1500);
        } else {
          wx.hideLoading();
          wx.showToast({
            title: '登录失败，请重试',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        wx.hideLoading();
        console.error('微信登录失败', err);
        wx.showToast({
          title: '登录失败，请重试',
          icon: 'none'
        });
      }
    });
  },

  // 手机号登录
  phoneLogin() {
    // 跳转到手机号登录页面（暂时注释，等待开发）
    // wx.navigateTo({
    //   url: '/pages/phone-login/phone-login'
    // });

    wx.showToast({
      title: '手机号登录功能开发中',
      icon: 'none'
    });
  }
});
