// 首页逻辑
Page({
  data: {},

  onLoad() {
    console.log('首页加载')
  },

  // 跳转到宁律师页面
  goToNinglawyer() {
    wx.navigateTo({
      url: '/pages/ninglawyer/ninglawyer'
    })
  },

  // 跳转到怎么判页面
  goToHowToJudge() {
    wx.navigateTo({
      url: '/pages/how_to_judge/how_to_judge'
    })
  }
})
