// components/nav-bar/nav-bar.js
Component({
  options: {
    multipleSlots: true // 启用多个插槽
  },

  properties: {
    // 标题
    title: {
      type: String,
      value: ''
    },
    // 是否显示返回按钮
    showBack: {
      type: Boolean,
      value: false
    }
  },

  methods: {
    // 返回按钮点击
    onBack() {
      this.triggerEvent('back');
    }
  }
});
