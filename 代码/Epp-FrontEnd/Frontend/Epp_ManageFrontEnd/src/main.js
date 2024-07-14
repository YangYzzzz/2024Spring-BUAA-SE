import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import AnimatedNumber from 'animated-number-vue3'
import * as echarts from 'echarts'

import 'element-plus/theme-chalk/el-loading.css'
import 'element-plus/theme-chalk/el-message.css'

const app = createApp(App)
app.use(router).use(store).use(AnimatedNumber)

// 全局挂载 echarts
app.config.globalProperties.$echarts = echarts

app.mount('#app')
