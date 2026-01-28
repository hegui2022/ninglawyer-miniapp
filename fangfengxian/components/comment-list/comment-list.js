// components/comment-list/comment-list.js
Component({
  properties: {
    // 标题
    title: {
      type: String,
      value: '精选留言'
    },
    // 是否显示按钮
    showButton: {
      type: Boolean,
      value: true
    },
    // 按钮文字
    buttonText: {
      type: String,
      value: '留言'
    },
    // 留言列表
    comments: {
      type: Array,
      value: []
    }
  },

  methods: {
    // 留言按钮点击
    onComment() {
      this.triggerEvent('comment');
    }
  }
});
