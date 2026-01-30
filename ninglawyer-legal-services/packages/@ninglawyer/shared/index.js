/**
 * @ninglawyer/shared 主入口文件
 * 宁律师小程序共享组件和工具库
 */

// 导出工具函数
export * from './utils/api.js'
export * from './utils/auth.js'
export * from './utils/date.js'
export * from './utils/storage.js'

// 导出技能类
export * from './skills/contract-draft.js'
export * from './skills/contract-review.js'
export * from './skills/legal-consult.js'

// 导出 MCP 服务
export { default as mcp } from './mcp/index.js'

// 版本信息
export const version = '1.0.0'
export const name = '@ninglawyer/shared'
