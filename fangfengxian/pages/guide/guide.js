// pages/guide/guide.js
Page({
  data: {
    statusBarHeight: 44,
    // 展开状态数组，索引0对应第一组卡片，索引1对应第二组卡片
    expandState: [false, false]
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

  // 切换展开/收起状态
  toggleExpand(e) {
    const index = parseInt(e.currentTarget.dataset.index);
    const expandState = this.data.expandState;
    
    // 切换对应卡片的展开状态
    expandState[index] = !expandState[index];
    
    this.setData({
      expandState: expandState
    });

    // 添加触觉反馈
    wx.vibrateShort({
      type: 'light'
    });
  },

  // 点击卡片（预留功能，可跳转到详情页）
  onCardTap(e) {
    const type = e.currentTarget.dataset.type;
    console.log('点击了卡片：', type);

    // 预留：跳转到详情页
    // wx.navigateTo({
    //   url: `/pages/detail/detail?type=${type}`
    // });
  },

  // 点击条目（预留功能，可跳转到文章详情）
  onItemTap(e) {
    const itemId = e.currentTarget.dataset.id;
    console.log('点击了条目：', itemId);

    // 预留：跳转到文章详情
    // wx.navigateTo({
    //   url: `/pages/article/article?id=${itemId}`
    // });
  }
});
