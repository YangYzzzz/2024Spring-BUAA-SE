import TabsView from '@/layouts/tabs/TabsView'
import BlankView from '@/layouts/BlankView'
import PageView from '@/layouts/PageView'

// 路由配置
const options = {
    routes: [
        {
            path: '/login',
            name: '登录页',
            component: () => import('@/pages/login')
        },
        {
            path: '*',
            name: '404',
            component: () => import('@/pages/exception/404'),
        },
        {
            path: '/403',
            name: '403',
            component: () => import('@/pages/exception/403'),
        },
        {
            path: '/',
            name: '首页',
            component: TabsView,
            redirect: '/login',
            children: [
                {
                    path: 'dashboard',
                    name: '主面板',
                    meta: {
                        icon: 'dashboard,',
                    },
                    component: () => import('@/pages/dashboard/analysis'),BlankView,    
                },
				
                {
                    path: 'user',
                    name: '用户管理',/*左边的标签名称*/
                    meta: {
                        icon: 'form',/*标签旁的小图标*/
                        page: {
                            cacheAble: false
                        }
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'userList',
                            name: '用户列表',
                            component: () => import('@/pages/form/advance/UserForm'),
                        },
                    ]
                }, 

                // {
                //     path: 'reports',
                //     name: '举报审核',
                //     meta: {
                //         icon: 'profile'
                //     },
                //     component: PageView,
                //     children: [
                //         {
                //             path: 'resultList',
                //             name: '举报列表',
                //             component: () => import('@/pages/form/advance/ResultForm'),
                //         },
                //         // {
                //         //     path: 'chengguoCertificate',
                //         //     name: '成果审核',
                //         //     component: () => import('@/pages/chengguo-certificate/ChengguoList'),
                //         // }

                //     ]
                // },
                // {
                //     path: 'result',
                //     name: '文献管理',
                //     meta: {
                //         icon: 'profile'
                //     },
                //     component: PageView,
                //     children: [
                //         {
                //             path: 'resultList',
                //             name: '文献列表',
                //             component: () => import('@/pages/form/advance/reportsForm'),
                //         },
                //         // {
                //         //     path: 'chengguoCertificate',
                //         //     name: '成果审核',
                //         //     component: () => import('@/pages/chengguo-certificate/ChengguoList'),
                //         // }

                //     ]
                // },
                
                {
                    path: 'commentReport',
                    name: '文献管理',
                    meta: {
                        icon: 'profile'
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'list',
                            name: '文献列表',
                            component: () => import('@/pages/list/search/ArticleList'),
                        },           
                    ]
                },
                // {
                //     path: 'NeedOrder',
                //     name: "需求订单管理",
                //     meta: {
                //         icon: 'shopping-cart'
                //     },
                //     component: PageView,
                //     children: [
                //         {
                //             path: 'NeedForm',
                //             name: "需求订单列表",
                //             component: () => import('../pages/need-order/NeedForm')
                //         }
                //     ]
                // },
                {
                    path: 'reports',
                    name: '举报审核',
                    meta: {
                        icon: 'table',
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'reportsList',
                            name: '未处理',
                            component: () => import('../pages/feedback/feedbackList')
                        },
                        {
                            path: 'handledReportsList',
                            name: '已处理',
                            component: () => import('../pages/feedback/handledfeedbackList')
                        }
                    ]
                },
                // {
                //     path: 'system-chat',
                //     name: 'AI/人工客服回复',
                //     meta: {
                //         icon: 'table',
                //     },
                //     component: PageView,
                //     children: [
                //         {
                //             path: 'SystemChatList',
                //             name: '客服回复列表',
                //             component: () => import('../pages/system-chat/systemChatList'),
                //         }
                //     ]
                // },
            ]
        },
    ]
}


export default options
