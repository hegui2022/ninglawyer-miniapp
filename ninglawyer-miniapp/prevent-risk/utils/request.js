// utils/request.js - 网络请求工具

const config = require('./config.js')

/**
 * 网络请求
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @param {string} method - 请求方法
 * @param {Object} header - 请求头
 * @returns {Promise} 请求结果
 */
function request(url, data = {}, method = 'GET', header = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: config.BASE_URL + url,
      data: data,
      method: method,
      header: {
        'content-type': 'application/json',
        'Authorization': wx.getStorageSync('token') || '',
        ...header
      },
      timeout: config.REQUEST_TIMEOUT,
      success: (res) => {
        if (res.statusCode === 200) {
          if (res.data.code === 0) {
            resolve(res.data.data)
          } else {
            wx.showToast({
              title: res.data.message || '请求失败',
              icon: 'none'
            })
            reject(res.data)
          }
        } else {
          wx.showToast({
            title: '网络错误',
            icon: 'none'
          })
          reject(res)
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络连接失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

/**
 * GET 请求
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @returns {Promise} 请求结果
 */
function get(url, data = {}) {
  return request(url, data, 'GET')
}

/**
 * POST 请求
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @returns {Promise} 请求结果
 */
function post(url, data = {}) {
  return request(url, data, 'POST')
}

/**
 * PUT 请求
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @returns {Promise} 请求结果
 */
function put(url, data = {}) {
  return request(url, data, 'PUT')
}

/**
 * DELETE 请求
 * @param {string} url - 请求地址
 * @param {Object} data - 请求数据
 * @returns {Promise} 请求结果
 */
function del(url, data = {}) {
  return request(url, data, 'DELETE')
}

/**
 * 上传文件
 * @param {string} url - 上传地址
 * @param {string} filePath - 文件路径
 * @param {Object} data - 额外数据
 * @returns {Promise} 上传结果
 */
function upload(url, filePath, data = {}) {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: config.BASE_URL + url,
      filePath: filePath,
      name: 'file',
      formData: data,
      header: {
        'Authorization': wx.getStorageSync('token') || ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const data = JSON.parse(res.data)
          if (data.code === 0) {
            resolve(data.data)
          } else {
            wx.showToast({
              title: data.message || '上传失败',
              icon: 'none'
            })
            reject(data)
          }
        } else {
          wx.showToast({
            title: '上传失败',
            icon: 'none'
          })
          reject(res)
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '上传失败',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

module.exports = {
  request,
  get,
  post,
  put,
  del,
  upload
}
