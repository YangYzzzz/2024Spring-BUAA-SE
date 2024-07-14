import { request, METHOD } from "@/utils/request";
import {PaperAll, BASE_URL_IP} from './api'

export const getReports = (params) => {
  const url = BASE_URL_IP + `/api/manage/commentReport`
  return request(url,"get",params)
}
export async function api_get_test(url) {
  return request(url, METHOD.GET);
}

export const getPaperAll = (id) => {
  if (id) {
    return request(PaperAll, "get", { user_id: id });
  } else {
    return request(PaperAll, "get");
  }
};

export const InterpretationIdReq = (id, type, method, params) => {
  const typeUrl = type === 1 ? 'Interpretation' : 'Note'
  const url = BASE_URL_IP + `/api/${typeUrl}/${id}`
  console.log(id,method)
  return request(url, method, params)
}

// export async function paperList() = (id) => {
//   return request(Paper, METHOD.GET, { user_id: id });
// }

export default {
  api_get_test,
  getPaperAll,
  InterpretationIdReq,
//   paperList
};
