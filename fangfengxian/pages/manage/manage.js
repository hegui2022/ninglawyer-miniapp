// pages/manage/manage.js
Page({
  data: {
    countdown: '3 天 40:52:00',
    timer: null
  },

  onLoad(options) {
    console.log('Manage page loaded');
    this.startCountdown();
  },

  onUnload() {
    // 页面卸载时清除定时器
    if (this.data.timer) {
      clearInterval(this.data.timer);
    }
  },

  // 开始倒计时
  startCountdown() {
    // 模拟倒计时（实际应该从后端获取会议时间）
    const timer = setInterval(() => {
      // 这里只是示例，实际应该根据会议时间计算
      // const now = new Date();
      // const meetingTime = new Date('2024-01-31 09:00:00');
      // const diff = meetingTime - now;
      // 根据差值计算天、时、分、秒

      // 暂时使用模拟数据
      const randomSecond = Math.floor(Math.random() * 59);
      const randomMinute = Math.floor(Math.random() * 59);
      this.setData({
        countdown: `3 天 40:${randomMinute.toString().padStart(2, '0')}:${randomSecond.toString().padStart(2, '0')}`
      });
    }, 1000);

    this.setData({ timer });
  },

  // 跳转到部门页面
  goToDepartment(e) {
    const dept = e.currentTarget.dataset.dept;
    console.log('Go to department:', dept);

    const deptNames = {
      shareholders: '股东会',
      sales: '销售部',
      finance: '财务部',
      hr: '人事部',
      tech: '技术部'
    };

    wx.showToast({
      title: `进入${deptNames[dept]}`,
      icon: 'none',
      duration: 1500
    });

    // 股东会跳转到专门的页面
    if (dept === 'shareholders') {
      wx.navigateTo({
        url: '/pages/shareholders/shareholders'
      });
    } else {
      // 其他部门暂时使用 toast 提示
      // wx.navigateTo({
      //   url: `/pages/department/department?dept=${dept}`
      // });
    }
  },

  // 跳转到通知详情
  goToNoticeDetail() {
    console.log('Go to notice detail');
    wx.showToast({
      title: '查看会议详情',
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到通知详情页
    // wx.navigateTo({
    //   url: '/pages/notice/notice'
    // });
  },

  // 跳转到审批详情
  goToApproval(e) {
    const type = e.currentTarget.dataset.type;
    console.log('Go to approval:', type);

    const typeNames = {
      leave: '事假申请',
      expense: '差旅费报销申请',
      purchase: '办公设备采购申请',
      reimburse: '日常报销申请'
    };

    wx.showToast({
      title: `查看${typeNames[type]}详情`,
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到审批详情页
    // wx.navigateTo({
    //   url: `/pages/approval/approval?type=${type}`
    // });
  },

  onShareAppMessage() {
    return {
      title: '管理',
      path: '/pages/manage/manage'
    };
  }
});
