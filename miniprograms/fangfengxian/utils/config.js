// utils/config.js - 配置文件

// API 基础地址
const BASE_URL = 'https://your-backend-api.com/api'

// 页面路径
const PAGE_PATHS = {
  index: '/pages/index/index',
  scan: '/pages/scan/scan',
  report: '/pages/report/report',
  compliance: '/pages/compliance/compliance',
  alert: '/pages/alert/alert'
}

// 风险等级
const RISK_LEVEL = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high'
}

// 扫描类型
const SCAN_TYPES = {
  CONTRACT: 'contract',
  COMPANY: 'company',
  LEGAL: 'legal',
  COMPLIANCE: 'compliance'
}

// 预警类型
const ALERT_TYPES = {
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low'
}

// 预警状态
const ALERT_STATUS = {
  PENDING: 'pending',
  HANDLED: 'handled'
}

// 网络请求超时时间
const REQUEST_TIMEOUT = 30000

// 分页大小
const PAGE_SIZE = 20

// 最大上传文件大小
const MAX_UPLOAD_SIZE = 10 * 1024 * 1024 // 10MB

module.exports = {
  BASE_URL,
  PAGE_PATHS,
  RISK_LEVEL,
  SCAN_TYPES,
  ALERT_TYPES,
  ALERT_STATUS,
  REQUEST_TIMEOUT,
  PAGE_SIZE,
  MAX_UPLOAD_SIZE
}
