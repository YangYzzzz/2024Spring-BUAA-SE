import {request, METHOD} from "../utils/request";
import {EnterpriseAll, BASE_URL_IP} from './api';

export const getEnterpriseAll = () => {
    return request(EnterpriseAll, METHOD.GET);
}

export const getEnterprise = (id, method) => {
    const url = `${BASE_URL_IP}/api/enterprise/getinfo/${id}`
    return request(url, method);
}

export const enterpriseApply = (id, method) => {
    const url = `${BASE_URL_IP}/api/enterprise/agree/${id}`
    return request(url, method)
}

export const enterpriseRefuse = (id, method) => {
    const url = `${BASE_URL_IP}/api/enterprise/refuse/${id}`

    return request(url, method)
}
