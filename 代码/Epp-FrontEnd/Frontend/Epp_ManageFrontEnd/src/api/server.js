import request from '@/utils/request.js'

export const getWebServerStatus = () => {
    // 获取Web服务器信息
    return request({
        method: 'get',
        url: '/api/manage/serverStatus',
        params: {
            mode: 1
        }
    })
}

export const getModuleServerStatus = () => {
    // 获取模型服务器信息
    return request({
        method: 'get',
        url: '/api/manage/serverStatus',
        params: {
            mode: 2
        }
    })
}

export const getVisitStatistic = () => {
    // 获取服务器访问统计信息
    return request({
        method: 'get',
        url: '/api/manage/visitStatistic'
    })
}
