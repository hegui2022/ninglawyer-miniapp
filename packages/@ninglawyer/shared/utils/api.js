/**
 * API 请求封装
 * 统一的请求方法，支持认证、错误处理、超时等
 */

import { auth } from './auth.js'

// API 基础地址
const BASE_URL = getApp()?.globalData?.config?.apiUrl || 'https://api.ninglawyer.com'

// 默认配置
const DEFAULT_CONFIG = {
  method: 'GET',
  timeout: 30000,
  header: {
    'Content-Type': 'application/json'
  }
}

/**
 * API 请求函数
 * @param {string} url - 请求路径
 * @param {object} data - 请求数据
 * @param {string} method - 请求方法
 * @param {object} config - 额外配置
 * @returns {Promise}
 */
export function request(url, data = {}, method = 'GET', config = {}) {
  return new Promise((resolve, reject) => {
    // 合并配置
    const finalConfig = {
      ...DEFAULT_CONFIG,
      ...config,
      method,
      header: {
        ...DEFAULT_CONFIG.header,
        ...config.header,
        // 添加认证 token
        'Authorization': auth.getToken() || ''
      }
    }

    // 处理请求参数
    const requestData = method.toUpperCase() === 'GET' ? data : JSON.stringify(data)
    const requestUrl = url.startsWith('http') ? url : `${BASE_URL}${url}`

    console.log(`[API] ${method} ${requestUrl}`, data)

    // 发送请求
    wx.request({
      url: requestUrl,
      method,
      data: requestData,
      header: finalConfig.header,
      timeout: finalConfig.timeout,
      success: (res) => {
        console.log(`[API] Response:`, res.data)

        if (res.statusCode === 200) {
          if (res.data.code === 0 || res.data.code === 200) {
            resolve(res.data)
          } else {
            // 业务错误
            handleError(res.data.message || '请求失败')
            reject(res.data)
          }
        } else if (res.statusCode === 401) {
          // Token 过期
          handleTokenExpired()
          reject(new Error('登录已过期'))
        } else {
          // HTTP 错误
          handleError(`网络错误: ${res.statusCode}`)
          reject(new Error(`网络错误: ${res.statusCode}`))
        }
      },
      fail: (err) => {
        console.error('[API] Request failed:', err)
        handleError('网络连接失败，请检查网络')
        reject(err)
      }
    })
  })
}

/**
 * GET 请求
 */
export function get(url, data = {}, config = {}) {
  return request(url, data, 'GET', config)
}

/**
 * POST 请求
 */
export function post(url, data = {}, config = {}) {
  return request(url, data, 'POST', config)
}

/**
 * PUT 请求
 */
export function put(url, data = {}, config = {}) {
  return request(url, data, 'PUT', config)
}

/**
 * DELETE 请求
 */
export function del(url, data = {}, config = {}) {
  return request(url, data, 'DELETE', config)
}

/**
 * 上传文件
 * @param {string} filePath - 文件路径
 * @param {string} name - 文件字段名
 * @param {object} formData - 额外表单数据
 */
export function uploadFile(filePath, name = 'file', formData = {}) {
  return new Promise((resolve, reject) => {
    const uploadUrl = getApp()?.globalData?.config?.uploadUrl || `${BASE_URL}/upload`

    wx.uploadFile({
      url: uploadUrl,
      filePath,
      name,
      formData,
      header: {
        'Authorization': auth.getToken() || ''
      },
      success: (res) => {
        try {
          const data = JSON.parse(res.data)
          if (data.code === 0 || data.code === 200) {
            resolve(data.data)
          } else {
            reject(new Error(data.message || '上传失败'))
          }
        } catch (error) {
          reject(error)
        }
      },
      fail: (err) => {
        console.error('[API] Upload failed:', err)
        reject(err)
      }
    })
  })
}

/**
 * 错误处理
 * @param {string} message - 错误信息
 */
function handleError(message) {
  wx.showToast({
    title: message,
    icon: 'none',
    duration: 2000
  })
}

/**
 * Token 过期处理
 */
function handleTokenExpired() {
  wx.showToast({
    title: '登录已过期，请重新登录',
    icon: 'none',
    duration: 2000
  })

  // 清除登录信息
  auth.clearToken()

  // 跳转到登录页
  setTimeout(() => {
    wx.reLaunch({
      url: '/pages/login/login'
    })
  }, 1500)
}

// 导出
export default {
  request,
  get,
  post,
  put,
  delete: del,
  uploadFile
}
