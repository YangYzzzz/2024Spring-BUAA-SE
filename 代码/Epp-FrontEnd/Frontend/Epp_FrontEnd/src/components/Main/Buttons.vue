<template>
  <div class="button-group">
    <button @click="goTo('literature')">文献调研</button>
    <button @click="goTo('paper')">论文上传</button>
    <button @click="goTo('personal')">个人中心</button>
  </div>
</template>

<script>
export default {
  name: 'NavigationButtons',
  methods: {
    goTo (page) {
      // 根据传入的参数跳转到不同的页面
      switch (page) {
      case 'literature':
        this.$router.push('/search')
        break
      case 'paper':
        this.$router.push('/upload')
        break
      case 'personal':
        this.$router.push('/personal')
        break
      default:
        break
      }
    }
  }
}
</script>

<style scoped>
.button-group {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  justify-content: space-between;
}

.button-group button {
  width: 280px;
  margin-left: 50px;
  margin-right: 25px;
  padding: 10px 20px; /* 调大按钮的大小 */
  font-size: 18px;
  background-color: #14aef5; /* 设置按钮背景色为浅绿色 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s; /* 添加按钮背景色过渡效果 */
  border: 3px solid #156dd1;
}

.button-group button:hover {
  background-color: #207ee9; /* 鼠标悬停时背景色变为绿色 */
}
</style>
