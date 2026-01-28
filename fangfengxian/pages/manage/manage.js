// pages/manage/manage.js
Page({
  onLoad(options) {
    console.log('Manage page loaded');
  },

  // 一键办公功能
  goToQuickOffice(e) {
    const type = e.currentTarget.dataset.type;
    console.log('Go to quick office:', type);

    const typeNames = {
      meeting: '会议通知',
      agreement: '出资协议',
      declaration: '入股声明',
      upload: '上传文件'
    };

    wx.showToast({
      title: `打开${typeNames[type]}`,
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到对应功能页面
    // wx.navigateTo({
    //   url: `/pages/${type}/${type}`
    // });
  },

  // 跳转到部门页面
  goToDepartment(e) {
    const dept = e.currentTarget.dataset.dept;
    console.log('Go to department:', dept);

    const deptNames = {
      hr: '人力资源部',
      sales: '销售部',
      finance: '财务部'
    };

    // 跳转到部门页面
    wx.navigateTo({
      url: `/pages/department/department?dept=${dept}`
    });
  },

  // 跳转到违规举报
  goToReport() {
    console.log('Go to report');
    wx.showToast({
      title: '违规举报',
      icon: 'none',
      duration: 1500
    });

    // 实际应该跳转到举报页面
    // wx.navigateTo({
    //   url: '/pages/report/report'
    // });
  },

  // 跳转到审批详情
  goToApproval(e) {
    const type = e.currentTarget.dataset.type;
    console.log('Go to approval:', type);

    const typeNames = {
      leave: '事假申请',
      expense: '差旅费报销申请'
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
