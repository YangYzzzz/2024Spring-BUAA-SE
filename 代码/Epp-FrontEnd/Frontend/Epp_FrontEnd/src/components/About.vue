<template>
  <div class="fullscreen-container">
    <div class="carousel-container">
      <el-carousel trigger="click" height="600px">
        <el-carousel-item v-for="member in members" :key="member.id">
          <div class="member-item">
            <div class="member-photo">
              <img :src="member.image" alt="profile" class="img-container">
            </div>
            <div class="member-info">
              <h3>{{ member.name }}</h3>
              <p>{{ member.role }}</p>
              <p><i>{{ member.description }}</i></p>
              <el-button type="text" @click="showModal = true">点我打赏</el-button>
            </div>
          </div>
          <el-dialog :visible.sync="showModal" :modal="false">
              <img :src="member.getMoneyPic" alt="profile" class="payment-code">
          </el-dialog>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      members: [
        {
          id: 1,
          name: '周靖宇',
          role: '项目经理，AI工程师，后端工程师',
          description: '你们五个怎么什么都会',
          image: require('@/assets/userAvatar/zjy.png'),
          getMoneyPic: require('@/assets/paymentCode/zjy-money.jpg')
        },
        {
          id: 2,
          name: '杨博文',
          role: 'AI总工程师，后端工程师',
          description: '原神，鸣潮，明日方舟，崩坏3，星穹铁道，启动！',
          image: require('@/assets/userAvatar/ybw.jpg'),
          getMoneyPic: require('@/assets/paymentCode/jkm-money.jpg')
        },
        {
          id: 3,
          name: '金楷茗',
          role: '前端总工程师',
          description: '给大家拜个早年',
          image: require('@/assets/userAvatar/jkm.png'),
          getMoneyPic: require('@/assets/paymentCode/jkm-money.jpg')
        },
        {
          id: 4,
          name: '陈俊华',
          role: '后端总工程师',
          description: 'stay hungry, stay foolish',
          image: require('@/assets/userAvatar/cjh.png'),
          getMoneyPic: require('@/assets/paymentCode/jkm-money.jpg')
        },
        {
          id: 5,
          name: '黄一轩',
          role: '运维总工程师，前端工程师，后端工程师',
          description: '山里灵活的狗',
          image: require('@/assets/userAvatar/hyx.jpg'),
          getMoneyPic: require('@/assets/paymentCode/jkm-money.jpg')
        },
        {
          id: 6,
          name: '李雨萌',
          role: '前端工程师',
          description: '打赏3块，买个菠萝',
          image: require('@/assets/userAvatar/lym.png'),
          getMoneyPic: require('@/assets/paymentCode/jkm-money.jpg')
        }
      ],
      showModal: false
    }
  },
  methods: {
    showPaymentCode () {
      this.showModal = !this.showModal
    }
  }
}
</script>

<style scoped>
.fullscreen-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 使用视口高度来使容器全屏 */
  width: 100vw; /* 使用视口宽度来确保容器宽度为全屏 */
  background-image: url('../assets/personal-back.png');
}

.carousel-container {
  width: 80%; /* 根据需求调整宽度 */
  height: auto; /* 根据内容自动调整高度 */
}

.member-item {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.member-photo {
  flex: 1;
  display: flex;
  /* align-items: center; */
  /* justify-content: center; */
  /* background-color: #f0f0f0; 背景色，用于显示图像未覆盖的区域 */
}

.member-info {
  flex: 1;
  text-align: center;
  padding-left: 20px;
}

.img-container {
  width: 100%;  /* 图像尝试填满容器宽度 */
  height: 100%; /* 图像尝试填满容器高度 */
  object-fit: cover;  /* 缩放图像以覆盖整个容器，可能会裁剪 */
  object-position: center; /* 图像在容器中居中 */
  padding: 70px;
}

.payment-code {
  width: 20vw;
  height: 50vh;
  display: block;
  margin: 0 auto;
}
</style>
