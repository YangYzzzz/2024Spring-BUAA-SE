import {request, METHOD} from "../utils/request";
import {BASE_URL_IP} from './api';

export const getWorkAll = (params) => {
    const url = `${BASE_URL_IP}/api/manage/papers`
    return request(url, METHOD.GET,params);
}

export const searchWork = (params) => {
    const url = `${BASE_URL_IP}/api/admin/search/result`
    return request(url, METHOD.POST, params);
}

export const getWork = (id) => {
    const url = `${BASE_URL_IP}/api/result/getinfo/${id}`
    return request(url, METHOD.GET);
}

export const WorkApply = (id) => {
    const url = `${BASE_URL_IP}/api/result/agree/${id}`
    return request(url, METHOD.GET)
}

export const WorkRefuse = (id) => {
    const url = `${BASE_URL_IP}/api/result/refuse/${id}`
    return request(url, METHOD.GET)
}

export const WorkDel = (params) => {
    const url = BASE_URL_IP + `/api/result/delete`
    return request(url, METHOD.POST, params)
}
  
export const WorkModify = (params) => {
    const url = BASE_URL_IP + `/api/admin/set/result`
return request(url, METHOD.POST, params)
}

export const getWorkUnaudited = (page) => {
    const url = `${BASE_URL_IP}/api/result/all/unaudited/${page}`
return request(url, METHOD.GET)
}