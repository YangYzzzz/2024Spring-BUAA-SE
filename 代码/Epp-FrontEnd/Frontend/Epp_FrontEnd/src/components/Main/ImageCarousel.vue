<template>
  <el-carousel :interval="4000" type="card" class="custom-carousel">
    <el-carousel-item>
      <img src="@/assets/dis1_1.png" alt="Image 1" class="custom-image">
    </el-carousel-item>
    <el-carousel-item>
      <img src="@/assets/dis2_2.png" alt="Image 2" class="custom-image">
    </el-carousel-item>
    <el-carousel-item>
      <img src="@/assets/dis3_3.png" alt="Image 3" class="custom-image">
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped>
.custom-carousel {
  width: 100%;
  border-radius: 10px;
}

.custom-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}
</style>
