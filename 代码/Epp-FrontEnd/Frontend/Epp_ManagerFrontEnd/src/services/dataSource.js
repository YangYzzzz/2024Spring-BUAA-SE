import { GOODS, GOODS_COLUMNS, PaperAll,UserAll, BASE_URL_IP} from "./api";
import { METHOD, request } from "@/utils/request";

export async function goodsList(params) {
  return request(GOODS, METHOD.GET, params);
}

export async function goodsColumns() {
  return request(GOODS_COLUMNS, METHOD.GET);
}

export const getkeywords = (params) => {
  const typeUrl = "Interpretation";
  const url = BASE_URL_IP + `/api/${typeUrl}/getkeywords`;
  return request(url, "get", params);
};

export const recommend = (params) => {
  const url = BASE_URL_IP +  "/api/recommend";
  return request(url, "get", params);
};

export const getvis = (params) => {
  const typeUrl = "Interpretation";
  const url = BASE_URL_IP + `/api/${typeUrl}/getvis`;
  return request(url, "get", params);
};

export const gettags = (params) => {
  const typeUrl = "Interpretation";
  const url = BASE_URL_IP + `/api/${typeUrl}/gettags`;
  return request(url, "get", params);
};

export const getInterpretationComments = (method, params) => {
  const url = BASE_URL_IP + "/api/comment";
  return request(url, method, params);
};

export const getUserInfo = (id) => {
  const url = BASE_URL_IP + "/api/user/profile";
  if (id) {
    return request(url, "get", { user_id: id });
  } else {
    return request(url, "get");
  }
};

export const InterpretationIdReq = (id, type, method, params) => {
  const typeUrl = type === 1 ? "Interpretation" : "Note";
  const url = BASE_URL_IP + `/api/${typeUrl}/${id}`;
  return request(url, method, params);
};

export const getLocalTime = (utcTime) => {
  if (utcTime === null || utcTime === undefined) {
    return '无'
  } else {
    let date = new Date(utcTime)
    const second = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
    const min = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()
    const hour = date.getHours() < 10 ? '0' + date.getHours() : date.getHours()
    // if (isHour) {
    //   return `${hour}:${min}:${second}`
    // }
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${hour}:${min}:${second}`
  }
}

export const getPaperAll = (id) => {
  if (id) {
    return request(PaperAll, "get", { user_id: id });
  } else {
    return request(PaperAll, "get");
  }
};

export const createProject = (params) => {
  const url = BASE_URL_IP + `/api/project/create`
  return request(url, 'post', params)
}

export const modifyProject = (params) => {
  const url = BASE_URL_IP + `/api/project/${params.id}`
  return request(url, 'post', params)
}

export const deleteProject = (params) => {
  const url = BASE_URL_IP + `/api/project/${params.id}`
  return request(url, 'delete', params)
}

export const addComment = (method, params) => {
  const url = BASE_URL_IP + '/api/comment/create'
  return request(url, method, params)
}

export const deleteComment = (method, params) => {
  const url = BASE_URL_IP + '/api/comment/delete'
  return request(url, method, params)
}

export const createDiscussionComment = (params) => {
  const url = BASE_URL_IP + `/api/discussion/create`
  return request(url, 'post', params)
}

export const deleteDiscussionComment = (method, params) => {
  const url =BASE_URL_IP + `/api/discussion/delete`
  return request(url, method, params)
}

export const getUserAll = (id) => {
  if (id) {
    return request(UserAll, "get", { user_id: id });
  } else {
    return request(UserAll, "get");
  }
};

export const getSelectUser = (params) => {
  const url = BASE_URL_IP + `/api/manage/users`
  return request(url, "get",params);
}

export const UserDel = (params) => {
  const url = BASE_URL_IP + `/api/user/delete`
  return request(url,"post", params)
}

export const UserModify = (params) => {
  const url = BASE_URL_IP + `/api/user/changeinfo`
  return request(url, "post", params)
}

export const searchUser = (params) => {
  const url = BASE_URL_IP + `/api/manage/users`
  return request(url, "get", params)
}

export const adminCreateUserAPI = (params) => {
  const url = BASE_URL_IP + `/api/admin/add/user`
  return request(url, METHOD.POST, params)
}

export const adminCreateExpertAPI = (params) => {
  const url = BASE_URL_IP + `/api/admin/add/expert`
  return request(url, METHOD.POST, params)
}

export const adminCreateCompanyAPI = (params) => {
  const url = BASE_URL_IP + `/api/admin/add/enterprise`
  return request(url, METHOD.POST, params)
}

export default {
  goodsList,
  goodsColumns,
  getkeywords,
  recommend,
  getvis,
  getPaperAll,
  gettags,
  InterpretationIdReq,
  getUserInfo,
  getInterpretationComments,
  getLocalTime,
  createProject,
  modifyProject,
  deleteProject,
  addComment,
  createDiscussionComment,
  deleteComment,
  deleteDiscussionComment,
  UserDel,
  UserModify,
  adminCreateCompanyAPI,
  adminCreateExpertAPI,
  adminCreateUserAPI
};
