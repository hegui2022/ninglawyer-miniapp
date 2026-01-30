/**
 * 存储工具
 * 封装微信存储 API，提供更友好的接口
 */

/**
 * 设置数据
 * @param {string} key - 键
 * @param {*} value - 值
 */
export function set(key, value) {
  try {
    wx.setStorageSync(key, JSON.stringify(value))
    return true
  } catch (error) {
    console.error('[Storage] Set failed:', error)
    return false
  }
}

/**
 * 获取数据
 * @param {string} key - 键
 * @param {*} defaultValue - 默认值
 * @returns {*}
 */
export function get(key, defaultValue = null) {
  try {
    const value = wx.getStorageSync(key)
    if (value === '') return defaultValue

    try {
      return JSON.parse(value)
    } catch {
      return value
    }
  } catch (error) {
    console.error('[Storage] Get failed:', error)
    return defaultValue
  }
}

/**
 * 删除数据
 * @param {string} key - 键
 */
export function remove(key) {
  try {
    wx.removeStorageSync(key)
    return true
  } catch (error) {
    console.error('[Storage] Remove failed:', error)
    return false
  }
}

/**
 * 清空所有数据
 */
export function clear() {
  try {
    wx.clearStorageSync()
    return true
  } catch (error) {
    console.error('[Storage] Clear failed:', error)
    return false
  }
}

/**
 * 获取所有数据
 * @returns {object}
 */
export function getAll() {
  try {
    const info = wx.getStorageInfoSync()
    const result = {}

    info.keys.forEach(key => {
      result[key] = get(key)
    })

    return result
  } catch (error) {
    console.error('[Storage] GetAll failed:', error)
    return {}
  }
}

/**
 * 获取存储信息
 * @returns {object}
 */
export function getInfo() {
  try {
    return wx.getStorageInfoSync()
  } catch (error) {
    console.error('[Storage] GetInfo failed:', error)
    return {
      keys: [],
      currentSize: 0,
      limitSize: 10 * 1024 * 1024 // 10MB
    }
  }
}

/**
 * 检查存储是否已满
 * @returns {boolean}
 */
export function isFull() {
  const info = getInfo()
  return info.currentSize >= info.limitSize * 0.9 // 超过 90% 视为已满
}

/**
 * 批量设置数据
 * @param {object} data - 数据对象
 */
export function setBatch(data) {
  const result = {}
  Object.keys(data).forEach(key => {
    result[key] = set(key, data[key])
  })
  return result
}

/**
 * 批量获取数据
 * @param {string[]} keys - 键数组
 * @returns {object}
 */
export function getBatch(keys) {
  const result = {}
  keys.forEach(key => {
    result[key] = get(key)
  })
  return result
}

/**
 * 批量删除数据
 * @param {string[]} keys - 键数组
 */
export function removeBatch(keys) {
  const result = {}
  keys.forEach(key => {
    result[key] = remove(key)
  })
  return result
}

/**
 * 创建命名空间
 * @param {string} namespace - 命名空间
 * @returns {object}
 */
export function createNamespace(namespace) {
  const prefix = `${namespace}_`

  return {
    set(key, value) {
      return set(prefix + key, value)
    },
    get(key, defaultValue) {
      return get(prefix + key, defaultValue)
    },
    remove(key) {
      return remove(prefix + key)
    },
    clear() {
      const info = getInfo()
      info.keys.forEach(key => {
        if (key.startsWith(prefix)) {
          remove(key)
        }
      })
    },
    getAll() {
      const info = getInfo()
      const result = {}
      info.keys.forEach(key => {
        if (key.startsWith(prefix)) {
          const shortKey = key.substring(prefix.length)
          result[shortKey] = get(key)
        }
      })
      return result
    }
  }
}

// 预定义的命名空间
export const userStorage = createNamespace('user')
export const appStorage = createNamespace('app')
export const cacheStorage = createNamespace('cache')

// 导出
export default {
  set,
  get,
  remove,
  clear,
  getAll,
  getInfo,
  isFull,
  setBatch,
  getBatch,
  removeBatch,
  createNamespace,
  userStorage,
  appStorage,
  cacheStorage
}
