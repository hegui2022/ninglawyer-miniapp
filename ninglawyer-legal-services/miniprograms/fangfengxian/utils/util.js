// utils/util.js - 工具函数

/**
 * 格式化日期
 * @param {Date|string|number} date - 日期
 * @param {string} format - 格式
 * @returns {string} 格式化后的日期
 */
function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return ''

  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hour = String(d.getHours()).padStart(2, '0')
  const minute = String(d.getMinutes()).padStart(2, '0')
  const second = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second)
}

/**
 * 格式化相对时间
 * @param {Date|string|number} date - 日期
 * @returns {string} 相对时间（如：刚刚、5分钟前）
 */
function formatRelativeTime(date) {
  if (!date) return ''

  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const now = new Date()
  const diff = Math.floor((now - d) / 1000) // 秒

  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  if (diff < 2592000) return `${Math.floor(diff / 86400)}天前`
  if (diff < 31536000) return `${Math.floor(diff / 2592000)}个月前`
  return `${Math.floor(diff / 31536000)}年前`
}

/**
 * 深拷贝
 * @param {any} obj - 对象
 * @returns {any} 拷贝后的对象
 */
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj)
  if (obj instanceof Array) return obj.map(item => deepClone(item))

  const cloned = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      cloned[key] = deepClone(obj[key])
    }
  }
  return cloned
}

/**
 * 防抖函数
 * @param {Function} func - 函数
 * @param {number} delay - 延迟时间
 * @returns {Function} 防抖后的函数
 */
function debounce(func, delay = 300) {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      func.apply(this, args)
    }, delay)
  }
}

/**
 * 节流函数
 * @param {Function} func - 函数
 * @param {number} delay - 延迟时间
 * @returns {Function} 节流后的函数
 */
function throttle(func, delay = 300) {
  let timer = null
  return function (...args) {
    if (timer) return
    timer = setTimeout(() => {
      func.apply(this, args)
      timer = null
    }, delay)
  }
}

/**
 * 获取风险等级文本
 * @param {string} level - 风险等级
 * @returns {string} 风险等级文本
 */
function getRiskLevelText(level) {
  const textMap = {
    'low': '低风险',
    'medium': '中风险',
    'high': '高风险'
  }
  return textMap[level] || '未知'
}

/**
 * 获取风险等级颜色
 * @param {string} level - 风险等级
 * @returns {string} 风险等级颜色
 */
function getRiskLevelColor(level) {
  const colorMap = {
    'low': '#07C160',
    'medium': '#FF9800',
    'high': '#F44336'
  }
  return colorMap[level] || '#999999'
}

/**
 * 显示加载
 * @param {string} title - 标题
 */
function showLoading(title = '加载中...') {
  wx.showLoading({
    title: title,
    mask: true
  })
}

/**
 * 隐藏加载
 */
function hideLoading() {
  wx.hideLoading()
}

/**
 * 显示成功提示
 * @param {string} title - 标题
 */
function showSuccess(title = '操作成功') {
  wx.showToast({
    title: title,
    icon: 'success',
    duration: 2000
  })
}

/**
 * 显示错误提示
 * @param {string} title - 标题
 */
function showError(title = '操作失败') {
  wx.showToast({
    title: title,
    icon: 'none',
    duration: 2000
  })
}

/**
 * 显示确认对话框
 * @param {string} content - 内容
 * @param {Function} confirm - 确认回调
 */
function showConfirm(content, confirm) {
  wx.showModal({
    title: '确认',
    content: content,
    success: (res) => {
      if (res.confirm && confirm) {
        confirm()
      }
    }
  })
}

module.exports = {
  formatDate,
  formatRelativeTime,
  deepClone,
  debounce,
  throttle,
  getRiskLevelText,
  getRiskLevelColor,
  showLoading,
  hideLoading,
  showSuccess,
  showError,
  showConfirm
}
