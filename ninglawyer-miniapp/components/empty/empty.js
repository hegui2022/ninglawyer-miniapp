// 空状态组件
Component({
  properties: {
    icon: {
      type: String,
      value: '/assets/images/empty.png'
    },
    text: {
      type: String,
      value: '暂无数据'
    },
    showButton: {
      type: Boolean,
      value: false
    },
    buttonText: {
      type: String,
      value: '去添加'
    }
  },
  
  methods: {
    // 点击按钮
    onButtonClick() {
      this.triggerEvent('buttonClick');
    },
    
    // 重新加载
    onReload() {
      this.triggerEvent('reload');
    }
  }
});
