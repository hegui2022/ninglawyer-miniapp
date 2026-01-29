/**
 * 数据交互管理器
 * 提供小程序之间的数据交互功能
 */

const { DATA_INTERACTION_TYPES } = require('./mini-program-config');
const { request } = require('./request');

/**
 * 保存数据到服务器（供其他小程序使用）
 * @param {string} type - 数据类型
 * @param {object} data - 数据对象
 * @returns {Promise}
 */
function saveSharedData(type, data) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/shared-data',
      method: 'POST',
      data: {
        type,
        data
      }
    }).then(res => {
      console.log('保存共享数据成功', res);
      resolve(res);
    }).catch(err => {
      console.error('保存共享数据失败', err);
      reject(err);
    });
  });
}

/**
 * 获取共享数据
 * @param {string} type - 数据类型
 * @param {string} dataId - 数据 ID
 * @returns {Promise}
 */
function getSharedData(type, dataId) {
  return new Promise((resolve, reject) => {
    request({
      url: `/api/shared-data/${type}/${dataId}`,
      method: 'GET'
    }).then(res => {
      console.log('获取共享数据成功', res);
      resolve(res);
    }).catch(err => {
      console.error('获取共享数据失败', err);
      reject(err);
    });
  });
}

/**
 * 删除共享数据
 * @param {string} type - 数据类型
 * @param {string} dataId - 数据 ID
 * @returns {Promise}
 */
function deleteSharedData(type, dataId) {
  return new Promise((resolve, reject) => {
    request({
      url: `/api/shared-data/${type}/${dataId}`,
      method: 'DELETE'
    }).then(res => {
      console.log('删除共享数据成功', res);
      resolve(res);
    }).catch(err => {
      console.error('删除共享数据失败', err);
      reject(err);
    });
  });
}

/**
 * 保存咨询数据
 * @param {object} consultationData - 咨询数据
 */
function saveConsultationData(consultationData) {
  return saveSharedData(DATA_INTERACTION_TYPES.CONSULTATION.type, consultationData);
}

/**
 * 获取咨询数据
 * @param {string} consultationId - 咨询 ID
 */
function getConsultationData(consultationId) {
  return getSharedData(DATA_INTERACTION_TYPES.CONSULTATION.type, consultationId);
}

/**
 * 保存合同数据
 * @param {object} contractData - 合同数据
 */
function saveContractData(contractData) {
  return saveSharedData(DATA_INTERACTION_TYPES.CONTRACT.type, contractData);
}

/**
 * 获取合同数据
 * @param {string} contractId - 合同 ID
 */
function getContractData(contractId) {
  return getSharedData(DATA_INTERACTION_TYPES.CONTRACT.type, contractId);
}

/**
 * 保存履约数据
 * @param {object} performanceData - 履约数据
 */
function savePerformanceData(performanceData) {
  return saveSharedData(DATA_INTERACTION_TYPES.PERFORMANCE.type, performanceData);
}

/**
 * 获取履约数据
 * @param {string} performanceId - 履约 ID
 */
function getPerformanceData(performanceId) {
  return getSharedData(DATA_INTERACTION_TYPES.PERFORMANCE.type, performanceId);
}

/**
 * 保存违约数据
 * @param {object} breachData - 违约数据
 */
function saveBreachData(breachData) {
  return saveSharedData(DATA_INTERACTION_TYPES.BREACH.type, breachData);
}

/**
 * 获取违约数据
 * @param {string} breachId - 违约 ID
 */
function getBreachData(breachId) {
  return getSharedData(DATA_INTERACTION_TYPES.BREACH.type, breachId);
}

/**
 * 保存风险数据
 * @param {object} riskData - 风险数据
 */
function saveRiskData(riskData) {
  return saveSharedData(DATA_INTERACTION_TYPES.RISK.type, riskData);
}

/**
 * 获取风险数据
 * @param {string} riskId - 风险 ID
 */
function getRiskData(riskId) {
  return getSharedData(DATA_INTERACTION_TYPES.RISK.type, riskId);
}

/**
 * 保存用户数据
 * @param {object} userData - 用户数据
 */
function saveUserData(userData) {
  return saveSharedData(DATA_INTERACTION_TYPES.USER.type, userData);
}

/**
 * 获取用户数据
 * @param {string} userId - 用户 ID
 */
function getUserData(userId) {
  return getSharedData(DATA_INTERACTION_TYPES.USER.type, userId);
}

/**
 * 通过场景获取数据（用于小程序跳转后获取数据）
 * @param {string} scene - 场景值
 * @returns {Promise}
 */
function getDataByScene(scene) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/shared-data/scene',
      method: 'GET',
      data: { scene }
    }).then(res => {
      console.log('通过场景获取数据成功', res);
      resolve(res);
    }).catch(err => {
      console.error('通过场景获取数据失败', err);
      reject(err);
    });
  });
}

/**
 * 设置场景数据（用于小程序跳转前设置数据）
 * @param {string} scene - 场景值
 * @param {object} data - 数据对象
 * @param {number} expireTime - 过期时间（秒，默认 1 小时）
 */
function setSceneData(scene, data, expireTime = 3600) {
  return new Promise((resolve, reject) => {
    request({
      url: '/api/shared-data/scene',
      method: 'POST',
      data: {
        scene,
        data,
        expireTime
      }
    }).then(res => {
      console.log('设置场景数据成功', res);
      resolve(res);
    }).catch(err => {
      console.error('设置场景数据失败', err);
      reject(err);
    });
  });
}

module.exports = {
  saveSharedData,
  getSharedData,
  deleteSharedData,
  saveConsultationData,
  getConsultationData,
  saveContractData,
  getContractData,
  savePerformanceData,
  getPerformanceData,
  saveBreachData,
  getBreachData,
  saveRiskData,
  getRiskData,
  saveUserData,
  getUserData,
  getDataByScene,
  setSceneData
};
