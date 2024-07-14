import {request, METHOD} from "../utils/request";
import {BASE_URL_IP} from './api'

export const getReport = (params) => {
    const url = `${BASE_URL_IP}/api/manage/commentReport`;
    return request(url,METHOD.GET,params)
}
export const getFeedbackAll = () => {
    const url = `${BASE_URL_IP}/api/feedback/getall`;
    return request(url, METHOD.GET);
}

export const replyFeedback = (params, method) => {
    const url = `${BASE_URL_IP}/api/manage/judgeCmtRpt`;
    return request(url, METHOD.POST, params);
}
