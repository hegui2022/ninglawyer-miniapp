/**
 * AI 交互模块
 * 提供与大模型的交互功能
 */

const { request } = require('./request');

/**
 * AI 聊天
 * @param {object} params - 聊天参数
 * @returns {Promise}
 */
function aiChat(params) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/consultation/consult',
      method: 'POST',
      data: params
    }).then(res => {
      console.log('AI 聊天成功', res);
      resolve(res);
    }).catch(err => {
      console.error('AI 聊天失败', err);
      reject(err);
    });
  });
}

/**
 * AI 路由咨询
 * @param {string} input - 用户输入
 * @param {object} context - 上下文信息
 * @returns {Promise}
 */
function aiRouteConsult(input, context = {}) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/consultation/route',
      method: 'POST',
      data: {
        input,
        context
      }
    }).then(res => {
      console.log('AI 路由咨询成功', res);
      resolve(res);
    }).catch(err => {
      console.error('AI 路由咨询失败', err);
      reject(err);
    });
  });
}

/**
 * AI 起草合同
 * @param {object} contractInfo - 合同信息
 * @returns {Promise}
 */
function aiDraftContract(contractInfo) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/contract/draft',
      method: 'POST',
      data: contractInfo
    }).then(res => {
      console.log('AI 起草合同成功', res);
      resolve(res);
    }).catch(err => {
      console.error('AI 起草合同失败', err);
      reject(err);
    });
  });
}

/**
 * AI 审查合同
 * @param {string} contractText - 合同文本
 * @param {string} domain - 法律领域
 * @returns {Promise}
 */
function aiReviewContract(contractText, domain = 'contract') {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/contract/review',
      method: 'POST',
      data: {
        contract_text: contractText,
        domain
      }
    }).then(res => {
      console.log('AI 审查合同成功', res);
      resolve(res);
    }).catch(err => {
      console.error('AI 审查合同失败', err);
      reject(err);
    });
  });
}

/**
 * AI 分析违约
 * @param {object} breachInfo - 违约信息
 * @returns {Promise}
 */
function aiAnalyzeBreach(breachInfo) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/breach/analyze',
      method: 'POST',
      data: breachInfo
    }).then(res => {
      console.log('AI 分析违约成功', res);
      resolve(res);
    }).catch(err => {
      console.error('AI 分析违约失败', err);
      reject(err);
    });
  });
}

/**
 * AI 扫描风险
 * @param {object} riskInfo - 风险信息
 * @returns {Promise}
 */
function aiScanRisk(riskInfo) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/risk/scan',
      method: 'POST',
      data: riskInfo
    }).then(res => {
      console.log('AI 扫描风险成功', res);
      resolve(res);
    }).catch(err => {
      console.error('AI 扫描风险失败', err);
      reject(err);
    });
  });
}

/**
 * AI 生成维权方案
 * @param {object} disputeInfo - 争议信息
 * @returns {Promise}
 */
function aiGenerateRightsPlan(disputeInfo) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/rights/generate',
      method: 'POST',
      data: disputeInfo
    }).then(res => {
      console.log('AI 生成维权方案成功', res);
      resolve(res);
    }).catch(err => {
      console.error('AI 生成维权方案失败', err);
      reject(err);
    });
  });
}

/**
 * AI 流式聊天（支持实时响应）
 * @param {object} params - 聊天参数
 * @param {function} onMessage - 消息回调
 * @param {function} onError - 错误回调
 * @param {function} onComplete - 完成回调
 */
function aiStreamChat(params, onMessage, onError, onComplete) {
  // 注意：微信小程序的 wx.request 不支持流式传输
  // 这里使用轮询方式模拟流式效果
  let fullResponse = '';
  
  aiChat(params)
    .then(res => {
      const answer = res.data.answer || '';
      
      // 模拟流式效果
      const chunkSize = 10;
      const chunks = [];
      for (let i = 0; i < answer.length; i += chunkSize) {
        chunks.push(answer.slice(i, i + chunkSize));
      }
      
      let index = 0;
      const interval = setInterval(() => {
        if (index < chunks.length) {
          fullResponse += chunks[index];
          onMessage(chunks[index], fullResponse);
          index++;
        } else {
          clearInterval(interval);
          if (onComplete) onComplete(fullResponse);
        }
      }, 50);
      
    })
    .catch(err => {
      if (onError) onError(err);
    });
}

module.exports = {
  aiChat,
  aiRouteConsult,
  aiDraftContract,
  aiReviewContract,
  aiAnalyzeBreach,
  aiScanRisk,
  aiGenerateRightsPlan,
  aiStreamChat
};
