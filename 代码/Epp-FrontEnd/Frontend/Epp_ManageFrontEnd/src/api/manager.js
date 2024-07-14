import request from '@/utils/request.js'

export const managerLogin = ({ managerName, managerPassword }) => {
    return request({
        method: 'post',
        url: '/api/managerLogin',
        data: {
            managerName: managerName,
            manpassowrd: managerPassword
        }
    })
}

export const managerLogout = () => {
    return request({
        method: 'get',
        url: '/api/managerLogout'
    })
}
