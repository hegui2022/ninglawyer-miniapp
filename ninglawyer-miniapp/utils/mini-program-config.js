/**
 * 小程序矩阵配置
 * 包含所有小程序的 AppID 和路径信息
 */

// 小程序配置
const MINI_PROGRAM_CONFIG = {
  // 法律教官（主小程序）
  legalInstructor: {
    appId: 'wx1234567890abcdef', // 实际部署时需要替换为真实的 AppID
    name: '法律教官',
    path: 'pages/index/index',
    description: '法律咨询入口，提供导航和综合服务'
  },

  // 码上签约
  codeSigning: {
    appId: 'wx1234567890abcde0', // 实际部署时需要替换为真实的 AppID
    name: '码上签约',
    path: 'pages/index/index',
    description: '合同起草、签署管理'
  },

  // 理约
  lyue: {
    appId: 'wx1234567890abcde1', // 实际部署时需要替换为真实的 AppID
    name: '理约',
    path: 'pages/index/index',
    description: '合同履约管理'
  },

  // 怎么判
  zenmePan: {
    appId: 'wx1234567890abcde2', // 实际部署时需要替换为真实的 AppID
    name: '怎么判',
    path: 'pages/index/index',
    description: '违约判断、维权指导'
  },

  // 防风险
  preventRisk: {
    appId: 'wx1234567890abcde3', // 实际部署时需要替换为真实的 AppID
    name: '防风险',
    path: 'pages/index/index',
    description: '企业风险扫描、预警'
  }
};

// 小程序跳转场景
const NAVIGATION_SCENES = {
  // 从法律教官跳转到其他小程序
  FROM_LEGAL_INSTRUCTOR: {
    toCodeSigning: {
      scene: 'contract_draft',
      description: '从法律咨询跳转到合同起草'
    },
    toLyue: {
      scene: 'contract_management',
      description: '从法律咨询跳转到合同履约'
    },
    toZenmePan: {
      scene: 'breach_judgment',
      description: '从法律咨询跳转到违约判断'
    },
    toPreventRisk: {
      scene: 'risk_prevention',
      description: '从法律咨询跳转到风险防控'
    }
  },

  // 从码上签约跳转到其他小程序
  FROM_CODE_SIGNING: {
    toLyue: {
      scene: 'contract_signed',
      description: '从合同签署跳转到履约管理'
    },
    toZenmePan: {
      scene: 'contract_dispute',
      description: '从合同签署跳转到违约判断'
    }
  },

  // 从理约跳转到其他小程序
  FROM_LYUE: {
    toZenmePan: {
      scene: 'breach_occurred',
      description: '从履约管理跳转到违约判断'
    }
  }
};

// 数据交互类型
const DATA_INTERACTION_TYPES = {
  // 咨询相关
  CONSULTATION: {
    type: 'consultation',
    description: '法律咨询数据'
  },

  // 合同相关
  CONTRACT: {
    type: 'contract',
    description: '合同数据'
  },

  // 履约相关
  PERFORMANCE: {
    type: 'performance',
    description: '履约数据'
  },

  // 违约相关
  BREACH: {
    type: 'breach',
    description: '违约数据'
  },

  // 风险相关
  RISK: {
    type: 'risk',
    description: '风险数据'
  },

  // 用户相关
  USER: {
    type: 'user',
    description: '用户数据'
  }
};

module.exports = {
  MINI_PROGRAM_CONFIG,
  NAVIGATION_SCENES,
  DATA_INTERACTION_TYPES
};
