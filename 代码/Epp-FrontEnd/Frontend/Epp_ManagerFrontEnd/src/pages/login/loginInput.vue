<template>
  <div>
    <div class="top-section">
      <!-- <p v-if='!isLogged' @click="redirectTo">{{ isLogin ? '新用户？去注册' : '已有账号？去登录' }}</p> -->
      <p class="login-message">{{ message }}</p>
    </div>
    <div class="bottom-section">
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label>账号:</label>
          <input type="text" v-model="username" required>
        </div>
        <div class="input-group">
          <label>密码:</label>
          <input type="password" v-model="password" required>
        </div>
        <button v-if="!isLogged" type="submit">{{'登录'}}</button>
        <button v-else @click="startUsing">进入管理页面</button>
      </form>
    </div>
  </div>
</template>

<script>
import { login } from '@/services/user.js'

export default {
  data () {
    return {
//       isLogin: true,
      username: '',
      password: '',
      message: '请登录',
      isLogged: false
    }
  },
  methods: {
    async handleSubmit () {
      try {
          var params = {
            'managerName': this.username,
            'manpassowrd': this.password
          }
          var res = await login(params)
          console.log(res.message)
          this.message = res.data.message
          this.isLogged = true
      } catch (error) {
        console.log('error')
          this.message = '登录失败，请重新输入'
      }
    },
    startUsing () {
      this.$router.push('/dashboard')
    }
  }
}
</script>

<style scoped>
.top-section {
  width: 90%; /* 设置宽度为80% */
  margin: 0 auto; /* 水平居中 */
  padding: 0.8rem 0.8rem; /* 调小上面框的内边距 */
  text-align: center;
  cursor: pointer;
  background-color: #1485f5; /* 浅灰色背景 */
  color: rgb(252, 249, 249); /* 深灰色文本 */
  border-radius: 10px 10px 0 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影 */
  /* margin-top: -1rem; 上移一点，使其看起来从下面的框中冒出来 */
  /* z-index: 1; 提升层级，使其位于下面的框之上 */
}

.bottom-section {
  padding: 2rem;
  text-align: center;
  background-color: #fff; /* 白色背景 */
  color: #007bff; /* 蓝色文本 */
  border-radius: 10px; /* 圆角 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影 */
  /* margin-top: 1rem; 下移一点，与上面的框有间距 */
  position: relative; /* 相对定位，使 z-index 生效 */
}

.blue {
  background-color: rgb(17, 71, 247);
  color: white;
}

.white {
  background-color: white;
  color: rgb(17, 71, 247);
}

.input-group {
  margin-top: 1rem;
  display: flex; /* 使用Flex布局 */
  align-items: center; /* 垂直居中对齐 */
}

.input-group label {
  margin-right: 1rem;
  flex: 0 0 auto; /* 不要弹性伸缩 */
}

.input-group input {
  padding: 0.5rem;
  font-size: 1.2rem;
  flex: 1; /* 填充剩余空间 */
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: rgb(17, 71, 247);
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: rgb(3, 3, 80);
}

.login-message {
  margin-top: 1rem;
}
</style>
