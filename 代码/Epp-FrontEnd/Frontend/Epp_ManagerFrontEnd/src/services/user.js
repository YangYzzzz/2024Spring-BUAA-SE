import {LOGIN, ROUTES} from '@/services/api'
import {request, METHOD, removeAuthorization} from '@/utils/request'
import {UserAll, BASE_URL_IP} from './api'
/**
 * 登录服务
 * @param name 账户名
 * @param password 账户密码
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function login(params) {
  return request(LOGIN, METHOD.POST, params)
}
// export const login = async (params) => {
//   try {
//     console.log(params)
//     const response = api.post('login', params)
//     console.log(response)
//     return response
//   } catch (error) {
//     throw new Error(error.response.data.message)
//   }
// }

export async function getRoutesConfig() {
  return request(ROUTES, METHOD.GET)
}

/**
 * 退出登录
 */
export function logout() {
  localStorage.removeItem(process.env.VUE_APP_ROUTES_KEY)
  localStorage.removeItem(process.env.VUE_APP_PERMISSIONS_KEY)
  localStorage.removeItem(process.env.VUE_APP_ROLES_KEY)
  removeAuthorization()
}

export const getUserAll = (id) => {
  if (id) {
    return request(UserAll, "get", { user_id: id });
  } else {
    return request(UserAll, "get");
  }
};

export const register = (method, params) => {
  const url = BASE_URL_IP + '/api/user/create'
  return request(url, method, params)
}

export default {
  login,
  logout,
  getRoutesConfig,
  getUserAll,
  register
}
