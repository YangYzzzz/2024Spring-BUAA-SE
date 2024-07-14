import {request, METHOD} from "../utils/request";
import {OrderAll,BASE_URL_IP} from './api'


export const getOrdertAll = () => {
    return request(OrderAll, METHOD.GET);
}

export const getOrder = (id, method) => {
    const url = `${BASE_URL_IP}/api/order/${id}`
    return request(url, method)
}


export const OrderDelete = (id, method) => {
    const url = `${BASE_URL_IP}/api/admin/order/${id}`;
    return request(url, method)
}
