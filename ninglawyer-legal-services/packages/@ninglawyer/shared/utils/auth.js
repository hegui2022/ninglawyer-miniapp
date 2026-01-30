/**
 * 认证工具
 * 管理 Token 和用户信息
 */

const TOKEN_KEY = 'ninglawyer_token'
const USER_INFO_KEY = 'ninglawyer_userinfo'
const TOKEN_EXPIRE_KEY = 'ninglawyer_token_expire'

/**
 * 设置 Token
 * @param {string} token - Token
 * @param {number} expireTime - 过期时间（毫秒）
 */
export function setToken(token, expireTime = 7 * 24 * 60 * 60 * 1000) {
  const expireDate = Date.now() + expireTime
  wx.setStorageSync(TOKEN_KEY, token)
  wx.setStorageSync(TOKEN_EXPIRE_KEY, expireDate)

  // 同步到 app.globalData
  const app = getApp()
  if (app) {
    app.globalData.token = token
    app.globalData.isLogin = true
  }
}

/**
 * 获取 Token
 * @returns {string|null}
 */
export function getToken() {
  const token = wx.getStorageSync(TOKEN_KEY)
  const expireTime = wx.getStorageSync(TOKEN_EXPIRE_KEY)

  // 检查是否过期
  if (expireTime && Date.now() > expireTime) {
    clearToken()
    return null
  }

  return token || null
}

/**
 * 清除 Token
 */
export function clearToken() {
  wx.removeStorageSync(TOKEN_KEY)
  wx.removeStorageSync(TOKEN_EXPIRE_KEY)

  // 同步到 app.globalData
  const app = getApp()
  if (app) {
    app.globalData.token = null
    app.globalData.isLogin = false
    app.globalData.userInfo = null
  }
}

/**
 * 检查是否已登录
 * @returns {boolean}
 */
export function isLoggedIn() {
  return !!getToken()
}

/**
 * 设置用户信息
 * @param {object} userInfo - 用户信息
 */
export function setUserInfo(userInfo) {
  wx.setStorageSync(USER_INFO_KEY, userInfo)

  // 同步到 app.globalData
  const app = getApp()
  if (app) {
    app.globalData.userInfo = userInfo
  }
}

/**
 * 获取用户信息
 * @returns {object|null}
 */
export function getUserInfo() {
  return wx.getStorageSync(USER_INFO_KEY) || null
}

/**
 * 清除用户信息
 */
export function clearUserInfo() {
  wx.removeStorageSync(USER_INFO_KEY)

  // 同步到 app.globalData
  const app = getApp()
  if (app) {
    app.globalData.userInfo = null
  }
}

/**
 * 登录
 * @param {object} loginData - 登录数据
 * @returns {Promise}
 */
export async function login(loginData) {
  // 这里应该调用登录 API
  // 示例代码
  return new Promise((resolve, reject) => {
    // 模拟登录
    setTimeout(() => {
      const token = 'mock_token_' + Date.now()
      const userInfo = {
        id: '1',
        name: '张三',
        avatar: '/assets/avatar.png'
      }

      setToken(token)
      setUserInfo(userInfo)

      resolve({ token, userInfo })
    }, 500)
  })
}

/**
 * 退出登录
 */
export function logout() {
  wx.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        clearToken()
        clearUserInfo()
        wx.reLaunch({
          url: '/pages/index/index'
        })
      }
    }
  })
}

/**
 * 刷新 Token
 * @returns {Promise}
 */
export async function refreshToken() {
  // 这里应该调用刷新 Token API
  // 示例代码
  return new Promise((resolve, reject) => {
    const oldToken = getToken()
    if (!oldToken) {
      reject(new Error('未登录'))
      return
    }

    // 模拟刷新
    setTimeout(() => {
      const newToken = 'new_token_' + Date.now()
      setToken(newToken)
      resolve(newToken)
    }, 500)
  })
}

/**
 * 检查 Token 是否即将过期（剩余 1 小时）
 * @returns {boolean}
 */
export function isTokenExpiringSoon() {
  const expireTime = wx.getStorageSync(TOKEN_EXPIRE_KEY)
  if (!expireTime) return false

  const remainingTime = expireTime - Date.now()
  return remainingTime < 60 * 60 * 1000 // 1 小时
}

// 导出
export default {
  setToken,
  getToken,
  clearToken,
  isLoggedIn,
  setUserInfo,
  getUserInfo,
  clearUserInfo,
  login,
  logout,
  refreshToken,
  isTokenExpiringSoon
}
