// utils/config.js - 统一配置文件

// 获取当前环境
const ENV = process.env.NODE_ENV || 'development';

// 环境配置
const CONFIG = {
  development: {
    // API 地址
    apiUrl: 'http://localhost:5000/api',
    baseUrl: 'http://localhost:5000',

    // 超时时间
    timeout: 30000,

    // 开发环境标识
    isDev: true
  },

  production: {
    // API 地址 - 需要替换为实际的生产环境地址
    apiUrl: 'https://api.ninglawyer.com/api',
    baseUrl: 'https://api.ninglawyer.com',

    // 超时时间
    timeout: 30000,

    // 开发环境标识
    isDev: false
  },

  // Coze 平台配置（如果使用 Coze 一键部署）
  coze: {
    // Coze API 地址
    apiUrl: 'https://api.coze.cn/v1',

    // Coze Bot ID（需要在 Coze 平台创建 Bot 后获取）
    botId: '',

    // Coze API Key（需要在 Coze 平台获取）
    apiKey: '',

    // Coze 平台配置的 URL
    botUrl: ''
  }
};

// 导出当前环境的配置
module.exports = {
  config: CONFIG[ENV],
  isDev: ENV === 'development',
  isProd: ENV === 'production',
  ENV
};
