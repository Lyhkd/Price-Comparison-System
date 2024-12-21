import axios from 'axios'
import type { AxiosResponse, AxiosError, AxiosRequestConfig } from 'axios'
import { getToken } from '@/libs/token'


const UUID = 'aa973966-c323-42a1-9ae1-0f0dba690fa5'

// axios.defaults.withCredentials = true

const request = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  // baseURL: 'http://10.162.29.65:8000',
  // baseURL: "http://flask:5000",
  timeout: 5000,
})


//请求拦截器
request.interceptors.request.use((config) => {
  window.$message.info("get request");
  // Add the userTempID to headers if it exists
  // if (config.headers) {
  //   config.headers.userTempID = 'aa973966-c323-42a1-9ae1-0f0dba690fa5';
  // }
  let token = getToken();
  if (token && config.headers) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

//响应拦截器
// request.interceptors.response.use(
//   res => {
//     return res.data
//   },
//   err => {
//     return Promise.reject(new Error('response failed!'))
//   }
// )

request.interceptors.response.use((response: AxiosResponse) => {
  const { code, message, data } = response.data

  // 根据自定义错误码判断请求是否成功
  if (code === 0) {
    // 将组件用的数据返回
    return data
  } else {
    // 处理业务错误。
    window.$message.error(message)
    return Promise.reject(new Error(message))
  }
}, (error: AxiosError) => {
  // 处理 HTTP 网络错误
  let message = ''
  // HTTP 状态码
  const status = error.response?.status
  switch (status) {
    case 401:
      message = 'token 失效，请重新登录'
      // 这里可以触发退出的 action
      break;
    case 403:
      message = '拒绝访问'
      break;
    case 404:
      message = '请求地址错误'
      break;
    case 500:
      message = '服务器故障'
      break;
    default:
      message = '网络连接故障'
  }

  window.$message.error(message)
  return Promise.reject(error)
})

/* 导出封装的请求方法 */
export const http = {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return request.get(url, config)
  },

  post<T = any>(url: string, data?: object, config?: AxiosRequestConfig): Promise<T> {
    return request.post(url, data, config)
  },

  put<T = any>(url: string, data?: object, config?: AxiosRequestConfig): Promise<T> {
    return request.put(url, data, config)
  },

  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return request.delete(url, config)
  }
}


export default request