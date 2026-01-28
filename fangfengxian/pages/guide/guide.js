// pages/guide/guide.js
Page({
  data: {
    selectedTab: 0,
    tabs: ['全部', '网络安', '数据安', '个人信'],
    item1Expanded: false,
    item2Expanded: false,
    item3Expanded: false
  },

  onLoad() {
    console.log('Guide page loaded');
  },

  toggleItem1() {
    this.setData({
      item1Expanded: !this.data.item1Expanded,
      item2Expanded: false,
      item3Expanded: false
    });
  },

  toggleItem2() {
    this.setData({
      item1Expanded: false,
      item2Expanded: !this.data.item2Expanded,
      item3Expanded: false
    });
  },

  toggleItem3() {
    this.setData({
      item1Expanded: false,
      item2Expanded: false,
      item3Expanded: !this.data.item3Expanded
    });
  },

  selectTab(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({ selectedTab: index });
  },

  goToArticle() {
    wx.navigateTo({
      url: '/pages/guide/article/article'
    });
  }
});
