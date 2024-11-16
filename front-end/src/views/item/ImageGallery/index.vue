<template>
  <n-carousel :loop="true" :autoplay="true" :interval="3000" style="height: 400px;" show-arrow>
    <n-carousel-item v-for="(img, index) in images" :key="index">
      <n-image :src="img" width="100%" height="100%" object-fit="cover" />
    </n-carousel-item>
    
  </n-carousel>
</template>

<script>
export default {
  name: 'ImageGallery',
  props: {
    images: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
/* 确保轮播图填满容器并保持适当高度 */
.n-carousel {
  height: 400px;  /* 设置固定高度 */
  width: 400px;;
}

.n-image {
  object-fit: cover;  /* 保证图片充满容器且不失真 */
}
</style>
