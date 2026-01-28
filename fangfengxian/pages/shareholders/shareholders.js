// pages/shareholders/shareholders.js
Page({
  data: {
    meetingType: 'temporary', // temporary | regular
    meetingMethod: 'phone' // phone | video
  },

  onLoad(options) {
    console.log('Shareholders page loaded', options);
  },

  goBack() {
    wx.navigateBack();
  },

  // 切换会议类型
  switchMeetingType(e) {
    const type = e.currentTarget.dataset.type;
    this.setData({ meetingType: type });

    wx.showToast({
      title: type === 'temporary' ? '临时会议' : '定期会议',
      icon: 'none'
    });
  },

  // 查看股东详情
  viewShareholderDetail() {
    console.log('View shareholder detail');
    wx.showModal({
      title: '股东详情',
      content: '姓名：张三\n持股比例：15%\n联系方式：138****8888',
      showCancel: false
    });
  },

  // 查看会议通知书详情
  viewNoticeDetail() {
    console.log('View notice detail');
    wx.showToast({
      title: '查看会议通知书',
      icon: 'none'
    });

    // 实际应该跳转到通知详情页
    // wx.navigateTo({
    //   url: '/pages/notice/notice'
    // });
  },

  // 选择会议方式
  selectMeetingMethod(e) {
    const method = e.currentTarget.dataset.method;
    this.setData({ meetingMethod: method });

    wx.showToast({
      title: method === 'phone' ? '电话语音会议' : '视频会议',
      icon: 'none'
    });
  },

  // 查看会议记录
  viewMeetingRecord() {
    console.log('View meeting record');
    wx.showToast({
      title: '查看会议记录',
      icon: 'none'
    });

    // 实际应该跳转到会议记录页
    // wx.navigateTo({
    //   url: '/pages/record/record'
    // });
  },

  // 进入投票
  goToVote() {
    console.log('Go to vote');
    wx.showModal({
      title: '会议表决',
      content: '确定进入投票环节吗？',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({
            title: '进入投票',
            icon: 'none'
          });

          // 实际应该跳转到投票页
          // wx.navigateTo({
          //   url: '/pages/vote/vote'
          // });
        }
      }
    });
  },

  onShareAppMessage() {
    return {
      title: '股东会',
      path: '/pages/shareholders/shareholders'
    };
  }
});
