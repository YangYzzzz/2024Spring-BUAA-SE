import { request, METHOD } from "../utils/request";
import { BASE_URL_IP } from "./api";

export const getSystemChatAll = () => {
    const url = `${BASE_URL_IP}/api/system_chat/getAll`;
    return request(url, METHOD.GET);
}

export const pushSystemChat = (params) => {
    const url = `${BASE_URL_IP}/api/system_chat/pushAdmin`
    console.log(params)
    return request(url, METHOD.POST, params);
}