<template>
  <div class="my-container">
    <!-- 背景图片 -->
    <div class="background"></div>
     <!-- 大标题 -->
     <div class="title">Easy Paper Plus Manager</div>
    <!-- 图片框和登录注册组件 -->
    <div class="content">
      <!-- <div class="left">
        <ImageCarousel />
      </div> -->
      <div class="right">
        <LoginRegister />
      </div>
    </div>
  </div>
</template>

<script>
// import ImageCarousel from './ImageCarousel.vue'
import LoginRegister from './loginInput.vue'

export default {
  name: 'dashboard',
  components: {
    // ImageCarousel,
    LoginRegister
  }
}
</script>

<style scoped>
.my-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 2rem; /* 标题字体大小 */
  font-weight: bold; /* 标题粗体 */
  color: rgb(250, 250, 250); /* 标题颜色 */
  text-align: center; /* 文本居中 */
  padding: 5rem 0 1.5rem; /* 上下留出一些空白
 /* background-color: #f8f8f8; /* 背景色 */
  /*border-bottom: 1px solid #ccc; 底部边框线 */
  z-index: 1; /* 在背景图片之上 */
}

.background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('../../assets/img/library.jpg');
  background-size: cover;
  background-position: center;
  z-index: 0;
}

.content {
  flex: 1;
  display: flex;
  z-index: 1;
}

.right {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
