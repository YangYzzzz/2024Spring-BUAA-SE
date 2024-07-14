// api.js
import Vue from 'vue'
import axios from 'axios'
import router from '../router'
import message from 'element-ui'
// import { cat } from 'shelljs'
axios.defaults.withCredentials = true

Vue.prototype.$axios = axios
const baseURL = 'https://epp.buaase.cn/api/'

const api = axios.create({
  baseURL,
  timeout: 5000 // 设置超时时间
})

api.interceptors.response.use(
  response => {
    let res = response
    return res
  },
  error => {
    // 对于登录接口，直接返回错误
    const skipUrls = ['login', 'sign', 'logout']
    if (error.response.config.url && skipUrls.some(url => error.response.config.url.includes(url))) {
      return Promise.reject(error)
    }
    if (error.response && error.response.status === 400) {
      return api.get('/testLogin').then(testLoginResponse => {
        return Promise.reject(error)
      }).catch(testLoginError => {
        if (testLoginError.response.status === 403) {
          document.cookie = 'userlogin=; expires=Thu, 01 Jan 1970 00:00:00 UTC'
          router.push('/dashboard')
          message.Message({
            type: 'error',
            message: '未登录或登录过期，请重新登录！'
          })
        }
        return Promise.reject(error)
      })
    }
    return Promise.reject(error)
  }
)

export const login = async (params) => {
  try {
    const response = await api.post('login', params)
    localStorage.clear() // 清除所有缓存
    var expiredTime = response.data.expired_time
    if (expiredTime) {
      expiredTime = 'expires=' + new Date(expiredTime).toUTCString()
      document.cookie = 'userlogin=' + response.data.username + '; ' + expiredTime
    }
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}

export const logout = async () => {
  try {
    const response = api.get('logout')
    document.cookie = 'userlogin=; expires=Thu, 01 Jan 1970 00:00:00 UTC'
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}

export const register = async (params) => {
  try {
    console.log(params)
    const response = api.post('sign', params)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
    // throw new Error(error.response.data.message)
  }
}

export const fetchCollectedPapers = async () => {
  console.log('fetchCollectPapers')
  return api.get('userInfo/collectedPapers')
    .then(response => {
      console.log(response)
      return response
    })
    .catch(error => {
      throw new Error(error.response.data.message)
    })
}

export const deleteCollectedPapers = async (data) => {
  try {
    console.log('deleteCollectPapers')
    const response = api.delete('userInfo/delCollectedPapers', data)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}

export const deleteReport = async (data) => {
  try {
    console.log('deleteReport')
    const response = api.delete('userInfo/delSummaryReports', data)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}

export const fetchSearchHistory = async () => {
  try {
    console.log('fetchSearchHistory')
    const response = api.get('userInfo/searchHistory')
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const deleteSearchHistory = async (params) => {
  try {
    console.log('deleteReport')
    const response = api.delete('userInfo/delSearchHistory', params)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}

export const fetchReports = async () => {
  try {
    console.log('fetchReports')
    const response = api.get('userInfo/summaryReports')
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}

export const fetchUserInfo = async () => {
  try {
    console.log('fetchInfo')
    const response = await api.get('userInfo/userInfo')
    console.log(response)
    localStorage.setItem('username', response.data.username)
    localStorage.setItem('avatar', 'https://epp.buaase.cn' + response.data.avatar)
    localStorage.setItem('loginTime', response.data.registration_date)
    localStorage.setItem('favorites', response.data.collected_papers_cnt)
    localStorage.setItem('likes', response.data.liked_papers_cnt)
    return response
  } catch (error) {
    console.log(error)
    throw new Error(error.response.data.message)
  }
}
export const fetchChat = async () => {
  try {
    console.log('fetchChat')
    const response = api.get('userInfo/paperReading')
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const deleteChat = async (data) => {
  try {
    console.log('deleteChat')
    console.log(data)
    const response = api.delete('userInfo/delPaperReading', data)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const fetchDocument = async () => {
  try {
    console.log('fetchDocument')
    const response = api.get('userInfo/documents')
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const uploadDocument = async (formData) => {
  try {
    console.log('uploadDocument')
    console.log(formData)
    const response = await api.post('uploadPaper', formData)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const deleteDocument = async (params) => {
  try {
    console.log('deleteDocument')
    const response = api.post('removeUploadedPaper', params)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const fetchNotification = async (mode) => {
  try {
    console.log('fetchNotification')
    console.log(mode)
    const response = api.get('userInfo/notices', mode)
    console.log('response')
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const deleteNotification = async (data) => {
  try {
    console.log('deleteDocument')
    const response = api.delete('userInfo/delNotices', data)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const readNotification = async (data) => {
  try {
    console.log('readNotification')
    const response = api.post('userInfo/readNotices', data)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
export const fetchReportContent = async (params) => {
  try {
    console.log(params)
    console.log('fetchReportContent')
    const response = api.get('userInfo/getSummary', params)
    console.log(response)
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}

export const userVisitRecord = async () => {
  try {
    const response = await api.post('manage/recordVisit')
    return response
  } catch (error) {
    throw new Error(error.response.data.message)
  }
}
