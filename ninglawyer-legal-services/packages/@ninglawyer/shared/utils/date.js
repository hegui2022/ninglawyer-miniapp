/**
 * 日期工具
 * 日期格式化、计算、转换等
 */

/**
 * 格式化日期
 * @param {Date|string|number} date - 日期
 * @param {string} format - 格式
 * @returns {string}
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return ''

  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 格式化为相对时间
 * @param {Date|string|number} date - 日期
 * @returns {string}
 */
export function formatRelativeTime(date) {
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (seconds < 60) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  if (days < 365) return `${Math.floor(days / 30)}个月前`
  return `${Math.floor(days / 365)}年前`
}

/**
 * 获取今天日期
 * @returns {Date}
 */
export function getToday() {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return today
}

/**
 * 获取明天日期
 * @returns {Date}
 */
export function getTomorrow() {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(0, 0, 0, 0)
  return tomorrow
}

/**
 * 获取昨天日期
 * @returns {Date}
 */
export function getYesterday() {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  yesterday.setHours(0, 0, 0, 0)
  return yesterday
}

/**
 * 获取本周开始日期
 * @returns {Date}
 */
export function getWeekStart() {
  const now = new Date()
  const day = now.getDay()
  const diff = now.getDate() - day + (day === 0 ? -6 : 1)
  const weekStart = new Date(now.setDate(diff))
  weekStart.setHours(0, 0, 0, 0)
  return weekStart
}

/**
 * 获取本月开始日期
 * @returns {Date}
 */
export function getMonthStart() {
  const now = new Date()
  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)
  monthStart.setHours(0, 0, 0, 0)
  return monthStart
}

/**
 * 获取本月结束日期
 * @returns {Date}
 */
export function getMonthEnd() {
  const now = new Date()
  const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0)
  monthEnd.setHours(23, 59, 59, 999)
  return monthEnd
}

/**
 * 计算日期差
 * @param {Date|string|number} date1 - 日期1
 * @param {Date|string|number} date2 - 日期2
 * @param {string} unit - 单位（day, hour, minute, second）
 * @returns {number}
 */
export function dateDiff(date1, date2, unit = 'day') {
  const d1 = new Date(date1)
  const d2 = new Date(date2)

  if (isNaN(d1.getTime()) || isNaN(d2.getTime())) return 0

  const diff = d2.getTime() - d1.getTime()

  switch (unit) {
    case 'second':
      return Math.floor(diff / 1000)
    case 'minute':
      return Math.floor(diff / (1000 * 60))
    case 'hour':
      return Math.floor(diff / (1000 * 60 * 60))
    case 'day':
      return Math.floor(diff / (1000 * 60 * 60 * 24))
    default:
      return diff
  }
}

/**
 * 判断是否为今天
 * @param {Date|string|number} date - 日期
 * @returns {boolean}
 */
export function isToday(date) {
  const d = new Date(date)
  if (isNaN(d.getTime())) return false

  const today = getToday()
  return d.toDateString() === today.toDateString()
}

/**
 * 判断是否为昨天
 * @param {Date|string|number} date - 日期
 * @returns {boolean}
 */
export function isYesterday(date) {
  const d = new Date(date)
  if (isNaN(d.getTime())) return false

  const yesterday = getYesterday()
  return d.toDateString() === yesterday.toDateString()
}

/**
 * 判断是否为本周
 * @param {Date|string|number} date - 日期
 * @returns {boolean}
 */
export function isThisWeek(date) {
  const d = new Date(date)
  if (isNaN(d.getTime())) return false

  const now = new Date()
  const weekStart = getWeekStart()
  const weekEnd = new Date(weekStart)
  weekEnd.setDate(weekEnd.getDate() + 6)
  weekEnd.setHours(23, 59, 59, 999)

  return d >= weekStart && d <= weekEnd
}

/**
 * 增加天数
 * @param {Date|string|number} date - 日期
 * @param {number} days - 天数
 * @returns {Date}
 */
export function addDays(date, days) {
  const d = new Date(date)
  d.setDate(d.getDate() + days)
  return d
}

/**
 * 增加月数
 * @param {Date|string|number} date - 日期
 * @param {number} months - 月数
 * @returns {Date}
 */
export function addMonths(date, months) {
  const d = new Date(date)
  d.setMonth(d.getMonth() + months)
  return d
}

/**
 * 获取时间戳
 * @param {Date|string|number} date - 日期
 * @returns {number}
 */
export function getTimestamp(date) {
  const d = new Date(date)
  return isNaN(d.getTime()) ? Date.now() : d.getTime()
}

// 导出
export default {
  formatDate,
  formatRelativeTime,
  getToday,
  getTomorrow,
  getYesterday,
  getWeekStart,
  getMonthStart,
  getMonthEnd,
  dateDiff,
  isToday,
  isYesterday,
  isThisWeek,
  addDays,
  addMonths,
  getTimestamp
}
