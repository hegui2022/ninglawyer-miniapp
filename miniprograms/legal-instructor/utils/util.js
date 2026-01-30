/**
 * 工具函数
 */

/**
 * 格式化日期
 */
function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  if (!date) return '';
  
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}

/**
 * 格式化金额
 */
function formatAmount(amount) {
  if (amount === null || amount === undefined) return '0.00';
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

/**
 * 防抖函数
 */
function debounce(fn, delay = 300) {
  let timer = null;
  return function(...args) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}

/**
 * 节流函数
 */
function throttle(fn, delay = 300) {
  let last = 0;
  return function(...args) {
    const now = Date.now();
    if (now - last > delay) {
      last = now;
      fn.apply(this, args);
    }
  };
}

/**
 * 深拷贝
 */
function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  
  if (obj instanceof Date) {
    return new Date(obj);
  }
  
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item));
  }
  
  if (obj instanceof Object) {
    const cloneObj = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        cloneObj[key] = deepClone(obj[key]);
      }
    }
    return cloneObj;
  }
}

/**
 * 判断是否为空
 */
function isEmpty(value) {
  if (value === null || value === undefined) return true;
  if (typeof value === 'string') return value.trim() === '';
  if (Array.isArray(value)) return value.length === 0;
  if (typeof value === 'object') return Object.keys(value).length === 0;
  return false;
}

/**
 * 获取随机字符串
 */
function randomString(length = 16) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * 显示 Toast
 */
function showToast(title, icon = 'none', duration = 2000) {
  wx.showToast({
    title,
    icon,
    duration
  });
}

/**
 * 显示 Loading
 */
function showLoading(title = '加载中...', mask = true) {
  wx.showLoading({
    title,
    mask
  });
}

/**
 * 隐藏 Loading
 */
function hideLoading() {
  wx.hideLoading();
}

/**
 * 显示模态框
 */
function showModal(options) {
  const { title = '提示', content, confirmText = '确定', cancelText = '取消' } = options;
  return new Promise((resolve) => {
    wx.showModal({
      title,
      content,
      confirmText,
      cancelText,
      success: (res) => {
        resolve(res.confirm);
      },
      fail: () => {
        resolve(false);
      }
    });
  });
}

/**
 * 页面跳转
 */
function navigateTo(url) {
  wx.navigateTo({
    url,
    fail: (err) => {
      console.error('页面跳转失败:', err);
      showToast('页面跳转失败');
    }
  });
}

/**
 * 页面重定向
 */
function redirectTo(url) {
  wx.redirectTo({
    url,
    fail: (err) => {
      console.error('页面重定向失败:', err);
      showToast('页面跳转失败');
    }
  });
}

/**
 * 切换到 TabBar 页面
 */
function switchTab(url) {
  wx.switchTab({
    url,
    fail: (err) => {
      console.error('切换 TabBar 失败:', err);
      showToast('页面切换失败');
    }
  });
}

/**
 * 返回上一页
 */
function navigateBack(delta = 1) {
  wx.navigateBack({
    delta,
    fail: (err) => {
      console.error('返回失败:', err);
    }
  });
}

/**
 * 上传图片
 */
function chooseImage(count = 1, sizeType = ['compressed'], sourceType = ['album', 'camera']) {
  return new Promise((resolve, reject) => {
    wx.chooseImage({
      count,
      sizeType,
      sourceType,
      success: (res) => {
        resolve(res.tempFilePaths);
      },
      fail: (err) => {
        showToast('选择图片失败');
        reject(err);
      }
    });
  });
}

/**
 * 预览图片
 */
function previewImage(urls, current = 0) {
  wx.previewImage({
    urls,
    current: typeof current === 'number' ? urls[current] : current
  });
}

/**
 * 复制到剪贴板
 */
function setClipboardData(data) {
  return new Promise((resolve, reject) => {
    wx.setClipboardData({
      data,
      success: () => {
        showToast('复制成功');
        resolve();
      },
      fail: () => {
        showToast('复制失败');
        reject();
      }
    });
  });
}

/**
 * 拨打电话
 */
function makePhoneCall(phoneNumber) {
  wx.makePhoneCall({
    phoneNumber,
    fail: () => {
      showToast('拨打电话失败');
    }
  });
}

/**
 * 保存图片到相册
 */
function saveImageToPhotosAlbum(filePath) {
  return new Promise((resolve, reject) => {
    wx.saveImageToPhotosAlbum({
      filePath,
      success: () => {
        showToast('保存成功');
        resolve();
      },
      fail: (err) => {
        showToast('保存失败');
        reject(err);
      }
    });
  });
}

module.exports = {
  formatDate,
  formatAmount,
  debounce,
  throttle,
  deepClone,
  isEmpty,
  randomString,
  showToast,
  showLoading,
  hideLoading,
  showModal,
  navigateTo,
  redirectTo,
  switchTab,
  navigateBack,
  chooseImage,
  previewImage,
  setClipboardData,
  makePhoneCall,
  saveImageToPhotosAlbum
};
