import { createStore } from 'vuex'

export default createStore({
    state: {
        userInfo: {
            userID: '',
            username: '',
            avatar: ''
        },
        managerInfo: (() => {
            const storedManager = localStorage.getItem('manager')
            if (!storedManager) {
                return {
                    managerName: '',
                    managerPassword: ''
                }
            } else {
                const parsedManager = JSON.parse(storedManager)
                return parsedManager
            }
        })()
    },
    mutations: {
        setUserInfo(state, info) {
            // 登录设置
            state.userInfo = info
        },
        resetUserInfo(state) {
            // 重置，退出登录
            state.userInfo = {
                userID: '',
                username: '',
                avatar: ''
            }
        },
        setManagerInfo(state, info) {
            state.managerInfo = info
            localStorage.setItem('manager', JSON.stringify(state.managerInfo))
        },
        resetManagerInfo(state) {
            state.managerInfo = {
                managerName: '',
                managerPassword: ''
            }
            localStorage.setItem('manager', JSON.stringify(state.managerInfo))
        }
    },
    actions: {
        //执行动作，数据请求
    },
    getters: {
        isUserLogin(state) {
            return state.userInfo.userID != '' ? true : false
        },
        isManagerLogin(state) {
            return state.managerInfo.managerName != '' ? true : false
        }
    }
})
