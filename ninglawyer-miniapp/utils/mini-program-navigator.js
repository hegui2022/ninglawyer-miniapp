/**
 * 小程序跳转管理器
 * 提供小程序之间的跳转功能
 */

const { MINI_PROGRAM_CONFIG, NAVIGATION_SCENES } = require('./mini-program-config');

/**
 * 跳转到指定小程序
 * @param {string} programKey - 小程序 key
 * @param {string} path - 目标页面路径
 * @param {object} params - 传递参数
 * @returns {Promise}
 */
function navigateToMiniProgram(programKey, path = '', params = {}) {
  return new Promise((resolve, reject) => {
    const program = MINI_PROGRAM_CONFIG[programKey];

    if (!program) {
      reject(new Error(`小程序 ${programKey} 不存在`));
      return;
    }

    // 构建完整路径
    let fullPath = path || program.path;
    
    // 添加参数
    if (Object.keys(params).length > 0) {
      const queryString = Object.keys(params)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
        .join('&');
      fullPath += `?${queryString}`;
    }

    console.log(`跳转到 ${program.name}，路径: ${fullPath}`);

    wx.navigateToMiniProgram({
      appId: program.appId,
      path: fullPath,
      envVersion: 'release', // 正式版
      success(res) {
        console.log(`跳转到 ${program.name} 成功`, res);
        resolve(res);
      },
      fail(err) {
        console.error(`跳转到 ${program.name} 失败`, err);
        wx.showToast({
          title: `跳转失败: ${err.errMsg}`,
          icon: 'none',
          duration: 2000
        });
        reject(err);
      }
    });
  });
}

/**
 * 从法律教官跳转到码上签约
 * @param {object} contractData - 合同数据
 */
function navigateToCodeSigning(contractData = {}) {
  const params = {
    scene: NAVIGATION_SCENES.FROM_LEGAL_INSTRUCTOR.toCodeSigning.scene,
    ...contractData
  };

  return navigateToMiniProgram('codeSigning', 'pages/create/create', params);
}

/**
 * 从法律教官跳转到理约
 * @param {object} contractData - 合同数据
 */
function navigateToLyue(contractData = {}) {
  const params = {
    scene: NAVIGATION_SCENES.FROM_LEGAL_INSTRUCTOR.toLyue.scene,
    ...contractData
  };

  return navigateToMiniProgram('lyue', 'pages/contract/contract', params);
}

/**
 * 从法律教官跳转到怎么判
 * @param {object} disputeData - 争议数据
 */
function navigateToZenmePan(disputeData = {}) {
  const params = {
    scene: NAVIGATION_SCENES.FROM_LEGAL_INSTRUCTOR.toZenmePan.scene,
    ...disputeData
  };

  return navigateToMiniProgram('zenmePan', 'pages/breach/breach', params);
}

/**
 * 从法律教官跳转到防风险
 * @param {object} riskData - 风险数据
 */
function navigateToPreventRisk(riskData = {}) {
  const params = {
    scene: NAVIGATION_SCENES.FROM_LEGAL_INSTRUCTOR.toPreventRisk.scene,
    ...riskData
  };

  return navigateToMiniProgram('preventRisk', 'pages/scan/scan', params);
}

/**
 * 从码上签约跳转到理约
 * @param {string} contractId - 合同 ID
 */
function navigateToLyueFromSigning(contractId) {
  const params = {
    scene: NAVIGATION_SCENES.FROM_CODE_SIGNING.toLyue.scene,
    contractId: contractId
  };

  return navigateToMiniProgram('lyue', 'pages/contract/contract', params);
}

/**
 * 从码上签约跳转到怎么判
 * @param {string} contractId - 合同 ID
 */
function navigateToZenmePanFromSigning(contractId) {
  const params = {
    scene: NAVIGATION_SCENES.FROM_CODE_SIGNING.toZenmePan.scene,
    contractId: contractId
  };

  return navigateToMiniProgram('zenmePan', 'pages/breach/breach', params);
}

/**
 * 从理约跳转到怎么判
 * @param {string} contractId - 合同 ID
 * @param {object} breachData - 违约数据
 */
function navigateToZenmePanFromLyue(contractId, breachData = {}) {
  const params = {
    scene: NAVIGATION_SCENES.FROM_LYUE.toZenmePan.scene,
    contractId: contractId,
    ...breachData
  };

  return navigateToMiniProgram('zenmePan', 'pages/breach/breach', params);
}

/**
 * 检查小程序是否安装
 * @param {string} programKey - 小程序 key
 */
function checkMiniProgramInstalled(programKey) {
  return new Promise((resolve) => {
    const program = MINI_PROGRAM_CONFIG[programKey];

    if (!program) {
      resolve(false);
      return;
    }

    // 注意：微信小程序没有直接检查其他小程序是否安装的 API
    // 这里返回 true，如果实际跳转失败会触发 fail 回调
    resolve(true);
  });
}

/**
 * 获取小程序信息
 * @param {string} programKey - 小程序 key
 */
function getMiniProgramInfo(programKey) {
  return MINI_PROGRAM_CONFIG[programKey];
}

/**
 * 获取所有小程序列表
 */
function getAllMiniPrograms() {
  return Object.keys(MINI_PROGRAM_CONFIG).map(key => ({
    key,
    ...MINI_PROGRAM_CONFIG[key]
  }));
}

module.exports = {
  navigateToMiniProgram,
  navigateToCodeSigning,
  navigateToLyue,
  navigateToZenmePan,
  navigateToPreventRisk,
  navigateToLyueFromSigning,
  navigateToZenmePanFromSigning,
  navigateToZenmePanFromLyue,
  checkMiniProgramInstalled,
  getMiniProgramInfo,
  getAllMiniPrograms
};
