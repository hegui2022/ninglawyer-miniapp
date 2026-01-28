// pages/department/department.js
Page({
  data: {
    currentTab: 'recruit', // recruit | onboarding | working | resignation
    inputMode: 'text', // text | voice
    inputText: '',
    showPanel: false
  },

  onLoad(options) {
    console.log('Department page loaded', options);
    const dept = options.dept || 'hr';

    const deptNames = {
      hr: '人力资源部',
      sales: '销售部',
      finance: '财务部'
    };

    // 根据部门设置不同的内容
    console.log('当前部门:', deptNames[dept]);
  },

  goBack() {
    wx.navigateBack();
  },

  // 切换标签
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({ currentTab: tab });

    const tabNames = {
      recruit: '招聘',
      onboarding: '入职',
      working: '在职',
      resignation: '离职'
    };

    wx.showToast({
      title: `切换到${tabNames[tab]}`,
      icon: 'none'
    });
  },

  // 查看岗位详情
  viewPosition(e) {
    const position = e.currentTarget.dataset.position;
    console.log('View position:', position);

    const positionNames = {
      director: '总监',
      accountant: '会计',
      cashier: '出纳',
      specialist: '人事专员'
    };

    wx.showToast({
      title: `查看${positionNames[position]}岗位详情`,
      icon: 'none',
      duration: 1500
    });
  },

  // 切换输入模式
  toggleInputMode() {
    const newMode = this.data.inputMode === 'text' ? 'voice' : 'text';
    this.setData({ inputMode: newMode });
  },

  // 文字输入
  onInput(e) {
    this.setData({ inputText: e.detail.value });
  },

  // 开始录音
  startRecord() {
    wx.showToast({
      title: '开始录音',
      icon: 'none'
    });
  },

  // 结束录音
  endRecord() {
    wx.showToast({
      title: '录音结束',
      icon: 'none'
    });
  },

  // 显示功能面板
  showFunctionPanel() {
    this.setData({ showPanel: true });
  },

  // 隐藏功能面板
  hideFunctionPanel() {
    this.setData({ showPanel: false });
  },

  // 阻止面板滚动
  preventMove() {
    return false;
  },

  // 跳转到功能
  goToFunction(e) {
    const func = e.currentTarget.dataset.func;
    console.log('Go to function:', func);

    const funcNames = {
      plan: '招聘计划',
      announcement: '招聘公告',
      declaration: '入股声明',
      upload: '上传文件',
      rules: '规则制度',
      employee: '员工'
    };

    wx.showToast({
      title: `打开${funcNames[func]}`,
      icon: 'none',
      duration: 1500
    });

    this.hideFunctionPanel();

    // 实际应该跳转到对应功能页面
    // wx.navigateTo({
    //   url: `/pages/${func}/${func}`
    // });
  },

  onShareAppMessage() {
    return {
      title: '人力资源',
      path: '/pages/department/department'
    };
  }
});
