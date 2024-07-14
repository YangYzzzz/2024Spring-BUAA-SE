import {request, METHOD} from "../utils/request";
import {ExpertAll,BASE_URL_IP} from './api'


export const getExpertAll = () => {
    return request(ExpertAll, METHOD.GET);
}

export const getExpert = (id, method) => {
    const url = `${BASE_URL_IP}/api/expert/getinfo/${id}`
    return request(url, method)
}

export const getScholarID = (method, params) => {
    const url = '/zhitu'
    return request(url, method, params)
}

export const expertApply = (id, method, params) => {
    const url = `${BASE_URL_IP}/api/expert/agree/${id}`
    return request(url, method, params)
}

export const expertRefuse = (id, method) => {
    const url = `${BASE_URL_IP}/api/expert/refuse/${id}`;
    return request(url, method)
}
