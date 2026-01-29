// 加载组件
Component({
  properties: {
    // 加载类型：circular（圆形）、dots（点状）、bar（条状）、text（文本）
    type: {
      type: String,
      value: 'circular'
    },
    // 尺寸：small（小）、medium（中）、large（大）
    size: {
      type: String,
      value: 'medium'
    },
    // 加载文本
    text: {
      type: String,
      value: ''
    },
    // 是否显示遮罩层
    mask: {
      type: Boolean,
      value: false
    }
  },

  data: {},

  methods: {}
});
