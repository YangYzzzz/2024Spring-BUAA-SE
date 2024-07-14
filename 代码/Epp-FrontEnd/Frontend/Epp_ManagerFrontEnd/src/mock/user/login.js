import Mock from 'mockjs'
import '@/mock/extend'

// const user = Mock.mock({
//   name: '@ADMIN',
//   avatar: '@AVATAR',
//   address: '@CITY',
//   position: '@POSITION'
// })
// Mock.mock(`/api/token-auth`, 'post', ({body}) => {
//   let result = {data: {}}
//   const {name, password} = JSON.parse(body)

//   let success = false

//   if (name === 'admin' && password === '888888') {
//     success = true
//     result.data.permissions = [{id: 'queryForm', operation: ['add', 'edit']}]
//     result.data.roles = [{id: 'admin', operation: ['add', 'edit', 'delete']}]
//   } else if (name === 'test1' || password === '888888') {
//     success = true
//     result.data.permissions = [{id: 'queryForm', operation: ['add', 'edit']}]
//     result.data.roles = [{id: 'test', operation: ['add', 'edit', 'delete']}]
//   } else {
//     success = false
//   }

//   if (success) {
//     result.code = 0
//     result.message = Mock.mock('@TIMEFIX').CN + '，欢迎回来'
//     result.data.user = user
//     result.data.token = 'Authorization:' + Math.random()
//     // result.data.expireAt = new Date(new Date().getTime() + 30 * 60 * 1000)
//   } else {
//     result.code = -1
//     result.message = '账户名或密码错误（admin/888888 or test/888888）'
//   }
//   console.log(result)
//   return result
// })

Mock.mock((`${process.env.VUE_APP_API_BASE_URL}/#/dashboard/newPage`,
          {"name":"网站",
          "num":3,
          "sites": [
              { "name":"Google", "info":[ "Android", "Google 搜索", "Google 翻译" ] },
              { "name":"Runoob", "info":[ "菜鸟教程", "菜鸟工具", "菜鸟微信" ] },
              { "name":"Taobao", "info":[ "淘宝", "网购" ] }
          ]
}))

