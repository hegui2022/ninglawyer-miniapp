import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1/legal_instructor',
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

/**
 * 创建案例
 */
export function createCase(data) {
  return api.post('/cases', data)
}

/**
 * 获取案例列表
 */
export function getCases(params) {
  return api.get('/cases', { params })
}

/**
 * 获取案例详情
 */
export function getCaseDetail(caseId) {
  return api.get(`/cases/${caseId}`)
}

/**
 * 删除案例
 */
export function deleteCase(caseId) {
  return api.delete(`/cases/${caseId}`)
}

/**
 * 搜索案例
 */
export function searchCases(data) {
  return api.post('/cases/search', data)
}
