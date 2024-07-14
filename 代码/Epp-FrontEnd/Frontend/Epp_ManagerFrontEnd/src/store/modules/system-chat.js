import {gettime} from '@/utils/time.js'
export default {
    namespaced: true,
    state: {
        systemChatList: [

        ],
        msgIndex: -1,
        msgPage: 1,
        $is_open_socket: false,
    },
    getters: {
        currentChatMsgs(state) {
            if (state.msgIndex == -1) {
                return []
            }
            let len = state.systemChatList[state.msgIndex].messages ? state.systemChatList[state.msgIndex].messages.length : 0
            if (len > 20) {
                return state.systemChatList[state.msgIndex].messages.slice(Math.max(0, len - 20 * state.msgPage), len)
            }
            return state.systemChatList[state.msgIndex].messages || []
        }
    },
    mutations: {
        setIndex(state, msgIndex) {
            state.msgIndex = msgIndex
        },
        setMsgPage(state, msgPage) {
            if (msgPage) {
                state.msgPage = msgPage
            } else {
                state.msgPage++
            }
        },
        setSystemChatList(state, systemChatList) {
            state.systemChatList = systemChatList
        },
        delSystemChatList(state, index) {
            state.systemChatList.splice(index, 1)
        },
        addSystemChatList(state, chat) {
            state.systemChatList.unshift(chat)
        },
        updateMsg(state) {
            state.systemChatList[state.msgIndex].noreadnum = 0
        },
        addSystemChatMessage(state, obj) {
            state.systemChatList[state.msgIndex].message = obj.message
            let len = state.systemChatList[state.msgIndex].messages.length
            if (len == 0) {
                obj.gstime = time.gettime.getChatTime(obj.gstime, 0)
            } else {
                obj.gstime = time.gettime.getChatTime(obj.gstime, state.systemChatList[state.msgIndex].messages[len - 1].created_at)
            }
            state.systemChatList[state.msgIndex].time = obj.time
            state.systemChatList[state.msgIndex].afterTime = + new Date(obj.sendTime)
            state.systemChatList[state.msgIndex].messages.push(obj)
        },
        sortSystemChatList(state) {
            state.systemChatList.sort((a, b) => {
                return b.afterTime - a.afterTime
            })
        },
        addNoreadMessage(state, index) {
            state.systemChatList[index].noreadnum = state.systemChatList[index] + 1
        },
        addSocket(state, soc) {
            state.socket = soc
        }
    },
    actions: {
        async setSocketV({state, commit}, uid) {
            if (!state.$is_open_socket) {
                // let socket = 
            }
        }
    }
} 