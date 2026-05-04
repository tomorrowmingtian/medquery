import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 30000
})

// 响应拦截
request.interceptors.response.use(
  res => res.data,
  err => {
    ElMessage.error('请求失败，请检查后端服务')
    return Promise.reject(err)
  }
)

export default request