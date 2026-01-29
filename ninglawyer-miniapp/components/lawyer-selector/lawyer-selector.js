// 律师选择组件
Component({
  properties: {
    // 显示模式：list（列表）、grid（网格）、tabs（选项卡）
    mode: {
      type: String,
      value: 'list'
    },
    // 标题
    title: {
      type: String,
      value: ''
    },
    // 律师列表
    lawyers: {
      type: Array,
      value: []
    },
    // 选中的领域
    selectedDomain: {
      type: String,
      value: ''
    }
  },

  data: {},

  methods: {
    // 选择律师
    onSelectLawyer(e) {
      const domain = e.currentTarget.dataset.domain;
      
      this.setData({
        selectedDomain: domain
      });
      
      // 触发选择事件
      this.triggerEvent('select', {
        domain,
        lawyer: this.data.lawyers.find(l => l.domain === domain)
      });
    },

    // 获取选中的律师
    getSelectedLawyer() {
      const { lawyers, selectedDomain } = this.data;
      return lawyers.find(l => l.domain === selectedDomain);
    },

    // 设置选中的领域
    setSelectedDomain(domain) {
      this.setData({
        selectedDomain: domain
      });
    },

    // 获取选中的领域
    getSelectedDomain() {
      return this.data.selectedDomain;
    }
  }
});
