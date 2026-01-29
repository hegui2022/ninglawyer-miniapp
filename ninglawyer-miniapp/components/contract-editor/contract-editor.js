// 合同编辑器组件
Component({
  properties: {
    // 合同文本
    contractText: {
      type: String,
      value: ''
    },
    // 是否显示模板
    showTemplates: {
      type: Boolean,
      value: false
    },
    // 是否只读
    readonly: {
      type: Boolean,
      value: false
    },
    // 工具栏按钮
    toolbarButtons: {
      type: Array,
      value: [
        { icon: '📝', label: '模板', action: 'template' },
        { icon: '💾', label: '保存', action: 'save' },
        { icon: '🔍', label: '审查', action: 'review' },
        { icon: '📋', label: '复制', action: 'copy' },
        { icon: '🗑️', label: '清空', action: 'clear' }
      ]
    },
    // 模板列表
    templates: {
      type: Array,
      value: [
        {
          id: 'purchase',
          name: '采购合同',
          description: '适用于商品采购'
        },
        {
          id: 'service',
          name: '服务合同',
          description: '适用于服务提供'
        },
        {
          id: 'lease',
          name: '租赁合同',
          description: '适用于房屋租赁'
        },
        {
          id: 'employment',
          name: '劳动合同',
          description: '适用于用工'
        }
      ]
    }
  },

  data: {
    wordCount: 0,
    lastSavedTime: '',
    loading: false
  },

  observers: {
    'contractText': function(text) {
      this.setData({
        wordCount: text.length
      });
    }
  },

  methods: {
    // 输入事件
    onInput(e) {
      const value = e.detail.value;
      this.setData({
        contractText: value,
        wordCount: value.length
      });
      
      this.triggerEvent('input', { value });
    },

    // 聚焦事件
    onFocus(e) {
      this.triggerEvent('focus', e.detail);
    },

    // 失焦事件
    onBlur(e) {
      this.triggerEvent('blur', e.detail);
    },

    // 工具栏点击
    onToolbarClick(e) {
      const action = e.currentTarget.dataset.action;
      
      switch (action) {
        case 'template':
          this.toggleTemplates();
          break;
        case 'save':
          this.saveContract();
          break;
        case 'review':
          this.reviewContract();
          break;
        case 'copy':
          this.copyContract();
          break;
        case 'clear':
          this.clearContract();
          break;
        default:
          this.triggerEvent('toolbarClick', { action });
      }
    },

    // 插入模板
    onInsertTemplate(e) {
      const template = e.currentTarget.dataset.template;
      
      this.triggerEvent('insertTemplate', { template });
      
      // 隐藏模板列表
      this.setData({ showTemplates: false });
    },

    // 切换模板显示
    toggleTemplates() {
      const showTemplates = !this.data.showTemplates;
      this.setData({ showTemplates });
    },

    // 保存合同
    saveContract() {
      this.setData({ loading: true });
      
      this.triggerEvent('save', {
        text: this.data.contractText
      });
      
      // 模拟保存
      setTimeout(() => {
        const now = new Date();
        const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
        
        this.setData({
          loading: false,
          lastSavedTime: timeStr
        });
        
        wx.showToast({
          title: '保存成功',
          icon: 'success'
        });
      }, 1000);
    },

    // 审查合同
    reviewContract() {
      this.triggerEvent('review', {
        text: this.data.contractText
      });
    },

    // 复制合同
    copyContract() {
      wx.setClipboardData({
        data: this.data.contractText,
        success: () => {
          wx.showToast({
            title: '已复制',
            icon: 'success'
          });
        }
      });
    },

    // 清空合同
    clearContract() {
      wx.showModal({
        title: '确认清空',
        content: '确定要清空合同内容吗？',
        success: (res) => {
          if (res.confirm) {
            this.setData({
              contractText: '',
              wordCount: 0
            });
            
            this.triggerEvent('clear');
          }
        }
      });
    },

    // 获取合同文本
    getValue() {
      return this.data.contractText;
    },

    // 设置合同文本
    setValue(value) {
      this.setData({
        contractText: value,
        wordCount: value.length
      });
    }
  }
});
