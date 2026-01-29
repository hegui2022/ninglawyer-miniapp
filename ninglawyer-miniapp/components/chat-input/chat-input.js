// 输入框组件
Component({
  properties: {
    // 占位符
    placeholder: {
      type: String,
      value: '请输入您的问题...'
    },
    // 最大长度
    maxlength: {
      type: Number,
      value: 1000
    },
    // 是否禁用
    disabled: {
      type: Boolean,
      value: false
    }
  },

  data: {
    inputValue: '',
    imagePreview: '',
    canSend: false
  },

  methods: {
    // 输入事件
    onInput(e) {
      const value = e.detail.value;
      this.setData({
        inputValue: value,
        canSend: value.trim().length > 0 || this.data.imagePreview
      });
    },

    // 聚焦事件
    onFocus(e) {
      this.triggerEvent('focus', e.detail);
    },

    // 失焦事件
    onBlur(e) {
      this.triggerEvent('blur', e.detail);
    },

    // 选择图片
    onChooseImage() {
      if (this.data.disabled) return;

      wx.chooseMedia({
        count: 1,
        mediaType: ['image'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          const tempFilePath = res.tempFiles[0].tempFilePath;
          this.setData({
            imagePreview: tempFilePath,
            canSend: true
          });
        },
        fail: (err) => {
          console.error('选择图片失败', err);
        }
      });
    },

    // 移除图片
    onRemoveImage() {
      this.setData({
        imagePreview: '',
        canSend: this.data.inputValue.trim().length > 0
      });
    },

    // 发送消息
    onSend() {
      if (this.data.disabled) return;

      const { inputValue, imagePreview } = this.data;

      if (!inputValue.trim() && !imagePreview) {
        return;
      }

      // 触发发送事件
      this.triggerEvent('send', {
        text: inputValue.trim(),
        image: imagePreview
      });

      // 清空输入
      this.setData({
        inputValue: '',
        imagePreview: '',
        canSend: false
      });
    },

    // 清空输入
    clear() {
      this.setData({
        inputValue: '',
        imagePreview: '',
        canSend: false
      });
    },

    // 设置输入值
    setValue(value) {
      this.setData({
        inputValue: value,
        canSend: value.trim().length > 0 || this.data.imagePreview
      });
    },

    // 获取输入值
    getValue() {
      return this.data.inputValue;
    },

    // 设置禁用状态
    setDisabled(disabled) {
      this.setData({ disabled });
    },

    // 聚焦输入框
    focus() {
      // 微信小程序的 textarea 没有直接的 focus 方法
      // 这里可以通过数据绑定控制
      this.triggerEvent('focus');
    }
  }
});
